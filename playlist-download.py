from plexapi.myplex import MyPlexAccount
from os import environ
from pathlib import Path

PLAYLIST_DIR = environ.get("PLAYLIST_DIR", "/home/tunnel/Music/Playlists")
MUSIC_DIR = environ.get("MUSIC_DIR", "/media/Data/Music")
PLAYLISTS = [
    "00 monthly playlist! :D",
    "50 good listening & learning",
    "02 vgm study",
    "01 amtrak",
    "y lastfm top all time",
    "y lastfm top six months",
]

account = MyPlexAccount()
plex = account.resource("alexandria").connect()

for playlist_name in PLAYLISTS:
    playlist_file = f"{PLAYLIST_DIR}/{playlist_name}.m3u"
    print(f"writing {playlist_file}")
    tracklist = []
    for track in plex.playlist(playlist_name):
        tracklist.append(track.locations[0])
    with open(playlist_file, "w") as f:
        f.write("#EXTM3U\n")
        for track in tracklist:
            p = Path(track)
            trackpath = f"{MUSIC_DIR}/{p.parent.name}/{p.name}"
            f.write(f"{trackpath}\n")
