import vlc
import requests
import os

# Inicializace VLC s nižší cache pro rychlejší start
vlc_instance = vlc.Instance("--no-xlib", "--network-caching=300", "--aout=alsa")

# Seznam streamů a jejich názvů
streams = [
    'http://icecast1.play.cz/kiss128.mp3', # Kiss Radio
    'https://ice.actve.net/fm-evropa2-128', # Evropa 2
    'https://ice.abradio.cz/rockradio128.mp3', # Rock rádio 
    'https://icecast2.play.cz/radiobeat128.mp3', # Rádio Beat
    'https://ice.actve.net/dance-radio128.mp3', # Dance rádio 
    'https://ice.abradio.cz/fajnnorth128.mp3', # Fajn rádio
    'https://ice.radia.cz/cernahora128.mp3', # Hitrádio Černá Hora
    'https://ice.radia.cz/hit80128.mp3', # Hitrádio Osmdesátka
    'https://ice.actve.net/fm-frekvence1-128', # Frekvence 1
    'https://rs.slapnet.cz/brno-mix3' # Scan letiště BRNO
]

radio_names = [
    'Kiss rádio',
    'Evropa 2',
    'Rock rádio',
    'Rádio Beat',
    'Dance rádio',
    'Fajn Rádio',
    'Hitrádio Černá Hora',
    'Hitrádio Osmdesátka',
    'Frekvence 1',
    'Scan letiště BRNO'
]

# URL API pro získání aktuálně hrající skladby
now_playing_api = {
    'Kiss rádio': ('https://radia.cz/api/v1/radio/radio-kiss/songs/now.json', 'interpret', 'song'),
    'Evropa 2': ('https://rds.actve.net/v1/metadata/channel/evropa2', 'artist', 'title'),
    'Rock rádio': ('https://radia.cz/api/v1/radio/rock-radio/songs/now.json', 'interpret', 'song'),
    'Rádio Beat': ('https://radia.cz/api/v1/radio/radio-beat/songs/now.json', 'interpret', 'song'),
    'Dance rádio': ('https://rds.actve.net/v1/metadata/channel/danceradio', 'artist', 'title'),
    'Fajn Rádio': ('https://radia.cz/api/v1/radio/fajn-radio/songs/now.json', 'interpret', 'song'),
    'Hitrádio Černá Hora': ('https://radia.cz/api/v1/radio/cerna-hora/songs/now.json', 'interpret', 'song'),
    'Hitrádio Osmdesátka': ('https://radia.cz/api/v1/radio/hitradio-80tka/songs/now.json', 'interpret', 'song'),
    'Frekvence 1': ('https://rds.actve.net/v1/metadata/channel/frekvence1', 'artist', 'title'),
    'Scan letiště BRNO': ('', '', '')
}

# Výchozí hlasitost
default_volume = 80

# HTTP session pro optimalizaci requestů
session = requests.Session()

def clear_console():
    """Vymaže obsah konzole."""
    os.system('cls' if os.name == 'nt' else 'clear')
