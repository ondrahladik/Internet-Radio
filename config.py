import vlc
import requests

# Initialize VLC with lower cache for faster startup
vlc_instance = vlc.Instance("--no-xlib", "--network-caching=300", "--aout=alsa")

# List of streams
streams = [
    'http://icecast1.play.cz/kiss128.mp3', # Kiss Radio
    'https://ice.actve.net/fm-evropa2-128', # Evropa 2
    'https://ice.abradio.cz/rockradio128.mp3', # Rock radio 
    'https://icecast2.play.cz/radiobeat128.mp3', # Radio Beat
    'https://ice.actve.net/dance-radio128.mp3', # Dance radio 
    'https://ice.abradio.cz/fajnnorth128.mp3', # Fajn radio
    'https://ice.radia.cz/cernahora128.mp3', # Hitradio Cerna Hora
    'https://ice.radia.cz/hit80128.mp3', # Hitradio Osmdesatka
    'https://rozhlas.stream/radiozurnal.mp3', # CRo Radiozurnal
    'https://ice.actve.net/fm-frekvence1-128', # Frekvence 1
    'https://rs.slapnet.cz/brno-mix3' # Letiste BRNO
]

# Station names
radio_names = [
    'Kiss radio',
    'Evropa 2',
    'Rock radio',
    'Radio Beat',
    'Dance radio',
    'Fajn Radio',
    'Hit Cerna Hora',
    'Hit Osmdesatka',
    'CRo Radiozurnal',
    'Frekvence 1',
    'Letiste BRNO'
]

# API URL to get the currently playing song 
# (Station name, API URL in json, Key for the performer, Key for song title)
now_playing_api = {
    'Kiss radio': ('https://radia.cz/api/v1/radio/radio-kiss/songs/now.json', 'interpret', 'song'),
    'Evropa 2': ('https://rds.actve.net/v1/metadata/channel/evropa2', 'artist', 'title'),
    'Rock radio': ('https://radia.cz/api/v1/radio/rock-radio/songs/now.json', 'interpret', 'song'),
    'Radio Beat': ('https://radia.cz/api/v1/radio/radio-beat/songs/now.json', 'interpret', 'song'),
    'Dance radio': ('https://rds.actve.net/v1/metadata/channel/danceradio', 'artist', 'title'),
    'Fajn Radio': ('https://radia.cz/api/v1/radio/fajn-radio/songs/now.json', 'interpret', 'song'),
    'Hit Cerna Hora': ('https://radia.cz/api/v1/radio/cerna-hora/songs/now.json', 'interpret', 'song'),
    'Hit Osmdesatka': ('https://radia.cz/api/v1/radio/hitradio-80tka/songs/now.json', 'interpret', 'song'),
    'CRo Radiozurnal': ('https://radia.cz/api/v1/radio/cesky-rozhlas-radiozurnal/songs/now.json', 'interpret', 'song'),
    'Frekvence 1': ('https://rds.actve.net/v1/metadata/channel/frekvence1', 'artist', 'title'),
    'Letiste BRNO': ('https://cs.ok1kky.cz/api/turany/info.json', 'info1', 'info2')
}

# Default volume
default_volume = 80

# Pins for buttons
left_button = 17
right_button = 27
up_button = 22
down_button = 23

# HTTP session for request optimization
session = requests.Session()