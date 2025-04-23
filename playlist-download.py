from plexapi.myplex import MyPlexAccount
from pathlib import Path

PLAYLIST_DIR = "/home/tunnel/Music/Playlists"
MOPIDY_DIR = "/home/tunnel/.local/share/mopidy/m3u"
IPOD_DIR = "/home/tunnel/Music/.ipod"
MUSIC_DIR = "/media/Data/Music"
PLAYLISTS = {
    "00 monthly playlist! :D": 24562,
    "50 good listening & learning": 20340,
    "02 vgm study": 53423,
    "01 amtrak": 26224,
    "y lastfm top all time": 0,
    "y lastfm top six months": 1,
}

account = MyPlexAccount()
plex = account.resource("alexandria").connect()

for playlist_name in PLAYLISTS:
    playlist_file = f"{PLAYLIST_DIR}/{playlist_name}.m3u"
    tracklist = []
    for track in plex.playlist(playlist_name):
        tracklist.append(track.locations[0])
    with open(playlist_file, "w") as f:
        f.write("#EXTM3U\n")
        for track in tracklist:
            p = Path(track)
            trackpath = f"{MUSIC_DIR}/{p.parent.name}/{p.name}"
            f.write(f"{trackpath}\n")

    exit()
