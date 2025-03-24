import time
import threading
from unidecode import unidecode
from config import vlc_instance, streams, radio_names, now_playing_api, default_volume, session
from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import sys

# Inicializace přehrávače a LCD displeje
player = vlc_instance.media_player_new()
current_stream_index = 0
running = True
update_event = threading.Event()
last_song_info = ""
current_volume = default_volume

# Inicializace GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Inicializace LCD displeje
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=2, dotsize=8)
lcd.clear()

def display_info(song_info=""):
    """Zobrazí aktuální stanici, skladbu a hlasitost na LCD."""
    if song_info:
        lcd.clear()
        lcd.write_string(f"{radio_names[current_stream_index][:16]}")  # Zobrazí stanici (max 16 znaků)
        lcd.cursor_pos = (1, 0)
        lcd.write_string(song_info[:20] if song_info else "")  # Zobrazí první část skladby (max 20 znaků)
    
    lcd.cursor_pos = (0, 16)
    volume_display = f"{current_volume}%".rjust(4)  # Hlasitost zarovnaná na 4 znaky
    lcd.write_string(volume_display)  # Zobrazí hlasitost

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
    """Získá informace o aktuálně hrající skladbě"""
    global last_song_info

    radio_name = radio_names[current_stream_index]
    api_url, artist_key, title_key = now_playing_api.get(radio_name, ('', '', ''))

    if api_url:
        try:
            response = session.get(api_url, timeout=5)
            response.raise_for_status()

            now_playing_data = response.json()
            artist = now_playing_data.get(artist_key, "Neznámý interpret")
            title = now_playing_data.get(title_key, "Neznámá skladba")

            artist_clean = unidecode(artist)
            title_clean = unidecode(title)

            new_song_info = " - ".join(filter(None, [artist_clean, title_clean]))

            if new_song_info != last_song_info:
                last_song_info = new_song_info
                display_info(new_song_info)
        except Exception as e:
            print(f"Chyba při získávání dat: {e}")  # Výpis chyby pro ladění

def update_now_playing():
    """Pravidelně aktualizuje informace o skladbě, ale až po 15s od změny stanice."""
    while running:
        update_event.wait(15)  
        update_event.clear()
        get_now_playing()

# Spuštění vlákna pro aktualizaci názvu skladby
thread = threading.Thread(target=update_now_playing, daemon=True)
thread.start()

print("Program spuštěn.") 

if not sys.stdout.isatty():  # Skript je spuštěn jako služba
    time.sleep(20)

play_stream()

# Piny pro tlačítka
left_button = 17
right_button = 27
up_button = 22
down_button = 23

# Nastavení pinů jako vstupy s pull-up rezistory
GPIO.setup(left_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(right_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(up_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(down_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Uchovává čas posledního stisku tlačítek
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

# Přerušení (interrupts) – reagují na stisk tlačítka
GPIO.add_event_detect(left_button, GPIO.FALLING, callback=change_stream, bouncetime=300)
GPIO.add_event_detect(right_button, GPIO.FALLING, callback=change_stream, bouncetime=300)
GPIO.add_event_detect(up_button, GPIO.FALLING, callback=change_volume, bouncetime=300)
GPIO.add_event_detect(down_button, GPIO.FALLING, callback=change_volume, bouncetime=300)


try:
    while True:
        time.sleep(1)  # Hlavní smyčka
except KeyboardInterrupt:
    print("\nUkončuji program.")  
    running = False
    update_event.set()
    player.stop()
    lcd.clear()
    GPIO.cleanup()  
