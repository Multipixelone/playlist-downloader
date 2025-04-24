from os import environ
from pathlib import Path
from urllib.parse import quote

PLAYLIST_DIR = environ.get("PLAYLIST_DIR", "/home/tunnel/Music/Playlists")
MUSIC_DIR = environ.get("MUSIC_DIR", "/media/Data/Music")
MOPIDY_PLAYLIST_DIR = "/home/tunnel/.local/share/mopidy/m3u"

print(PLAYLIST_DIR)
