import time
import threading
from unidecode import unidecode
from config import vlc_instance, streams, radio_names, now_playing_api, default_volume, left_button, right_button, up_button, down_button, session
from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import sys

# Initializing the player and LCD display
player = vlc_instance.media_player_new()
current_stream_index = 0
running = True
update_event = threading.Event()
last_song_info = ""
current_volume = default_volume

# GPIO initialization
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initializing the LCD display
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=2, dotsize=8)
lcd.clear()

def display_info(song_info=""):
    """Displays the current station, song and volume on the LCD."""
    if song_info:
        lcd.clear()
        lcd.write_string(f"{radio_names[current_stream_index][:16]}")  # Displays the station (max 16 characters)
        lcd.cursor_pos = (1, 0)
        lcd.write_string(song_info[:20] if song_info else "")  # Displays the first part of the song (max 20 characters)
    
    lcd.cursor_pos = (0, 16)
    volume_display = f"{current_volume}%".rjust(4)  # Volume aligned to 4 characters
    lcd.write_string(volume_display)  # Displays the volume

def play_stream():
    global last_song_info

    stream_url = streams[current_stream_index]

    last_song_info = ""  
    player.stop()  
    time.sleep(0.1) 

    media = vlc_instance.media_new(stream_url)
    player.set_media(media)
    player.play()
    player.audio_set_volume(current_volume)

    update_event.set()
    time.sleep(1)  
    get_now_playing()

def get_now_playing():
    """Gets information about the currently playing song."""
    global last_song_info

    radio_name = radio_names[current_stream_index]
    api_url, artist_key, title_key = now_playing_api.get(radio_name, ('', '', ''))

    if api_url:
        try:
            response = session.get(api_url, timeout=5)
            response.raise_for_status()

            now_playing_data = response.json()
            artist = now_playing_data.get(artist_key, "Unknown")
            title = now_playing_data.get(title_key, "Unknown")

            artist_clean = unidecode(artist)
            title_clean = unidecode(title)

            new_song_info = " - ".join(filter(None, [artist_clean, title_clean]))

            if new_song_info != last_song_info:
                last_song_info = new_song_info
                display_info(new_song_info)
        except Exception as e:
            print(f"Error while retrieving data: {e}")  

def update_now_playing():
    """Updating song information."""
    while running:
        update_event.wait(15)  
        update_event.clear()
        get_now_playing()

# Start thread to update song title
thread = threading.Thread(target=update_now_playing, daemon=True)
thread.start()

print("Program started.") 

if not sys.stdout.isatty():  # The script is run as a service
    time.sleep(20)

play_stream()

# Setting pins as inputs with pull-up resistors
GPIO.setup(left_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(right_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(up_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(down_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Stores the time of the last key press
last_press_time = {17: 0, 27: 0, 22: 0, 23: 0} 

lock = threading.Lock() 

def change_stream(channel):
    global current_stream_index

    with lock: 
        current_time = time.time()
        if current_time - last_press_time[channel] < 0.5: 
            return

        last_press_time[channel] = current_time  

        if GPIO.input(channel) == 0:  
            if channel == left_button:
                current_stream_index = (current_stream_index - 1) % len(streams)
            elif channel == right_button:
                current_stream_index = (current_stream_index + 1) % len(streams)
            play_stream()

        time.sleep(0.2) 

def change_volume(channel):
    global current_volume
    if channel == up_button:
        current_volume = min(current_volume + 10, 100)  
    elif channel == down_button:
        current_volume = max(current_volume - 10, 0)  
    player.audio_set_volume(current_volume) 
    display_info()  

# Interrupts – respond to button presses
GPIO.add_event_detect(left_button, GPIO.FALLING, callback=change_stream, bouncetime=300)
GPIO.add_event_detect(right_button, GPIO.FALLING, callback=change_stream, bouncetime=300)
GPIO.add_event_detect(up_button, GPIO.FALLING, callback=change_volume, bouncetime=300)
GPIO.add_event_detect(down_button, GPIO.FALLING, callback=change_volume, bouncetime=300)


try:
    while True:
        time.sleep(1)  # Main loop
except KeyboardInterrupt:
    print("\nProgram ended.")  
    running = False
    update_event.set()
    player.stop()
    lcd.clear()
    GPIO.cleanup()  
