import time
import keyboard
import threading
from config import vlc_instance, streams, radio_names, now_playing_api, default_volume, session, clear_console

# Inicializace přehrávače
player = vlc_instance.media_player_new()
current_stream_index = 0
running = True
update_event = threading.Event()
last_song_info = ""
current_volume = default_volume

def display_info(song_info=""):
    """Zobrazí aktuální stanici, skladbu a hlasitost."""
    clear_console()
    print(f"\n▶️ Hraje: {radio_names[current_stream_index]}")
    if song_info:
        print(song_info)
    print(f"\n🔊 Hlasitost: {current_volume}% ")

def play_stream():
    """ Přehraje aktuální stream a zobrazí aktuálně hrající skladbu. """
    global last_song_info

    stream_url = streams[current_stream_index]

    last_song_info = ""  
    media = vlc_instance.media_new(stream_url)
    player.set_media(media)
    player.play()
    player.audio_set_volume(current_volume)

    update_event.set()
    time.sleep(1)  
    get_now_playing()

def get_now_playing():
    """ Získá informace o aktuálně hrající skladbě a přepíše starý výpis. """
    global last_song_info

    radio_name = radio_names[current_stream_index]
    api_url, artist_key, title_key = now_playing_api.get(radio_name, ('', '', ''))

    if api_url:
        try:
            response = session.get(api_url, timeout=5)
            if response.status_code == 200:
                now_playing_data = response.json()
                artist = now_playing_data.get(artist_key, "Neznámý interpret")
                title = now_playing_data.get(title_key, "Neznámá skladba")

                new_song_info = f"\n🎵 Aktuálně hrající skladba:\n   🎤 Interpret: {artist}\n   🎶 Skladba: {title}"

                if new_song_info != last_song_info:
                    last_song_info = new_song_info
                    display_info(new_song_info)
            else:
                display_info("\n⚠️ Chyba při načítání dat o skladbě.")
        except Exception as e:
            display_info(f"\n❌ Chyba při volání API: {e}")
    else:
        display_info("\nℹ️ Pro tuto stanici nejsou dostupné informace.")

def update_now_playing():
    """ Pravidelně aktualizuje informace o skladbě, ale až po 15s od změny stanice. """
    while running:
        update_event.wait(15)  
        update_event.clear()
        get_now_playing()

# Spuštění vlákna pro aktualizaci názvu skladby
thread = threading.Thread(target=update_now_playing, daemon=True)
thread.start()

play_stream()

# Ovládání pomocí klávesnice 
try:
    while running:
        if keyboard.is_pressed("left"):
            current_stream_index = (current_stream_index - 1) % len(streams)
            play_stream()
            time.sleep(0.2)  

        elif keyboard.is_pressed("right"):
            current_stream_index = (current_stream_index + 1) % len(streams)
            play_stream()
            time.sleep(0.2)

        elif keyboard.is_pressed("up"):
            current_volume = min(player.audio_get_volume() + 10, 100)
            player.audio_set_volume(current_volume)
            display_info(last_song_info)
            time.sleep(0.1)

        elif keyboard.is_pressed("down"):
            current_volume = max(player.audio_get_volume() - 10, 0)
            player.audio_set_volume(current_volume)
            display_info(last_song_info)
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\n👋 Ukončuji program.")
    running = False
    update_event.set()
    player.stop()
