from plexapi.myplex import MyPlexAccount
from os import environ
from pathlib import Path
from urllib.parse import quote

PLAYLISTS = [
    "00 monthly playlist! :D",
    "50 good listening & learning",
    "02 vgm study",
    "01 amtrak",
    "y lastfm top all time",
    "y lastfm top six months",
]

PLAYLIST_DIR = environ.get("PLAYLIST_DIR", "/home/tunnel/Music/Playlists")
MUSIC_DIR = environ.get("MUSIC_DIR", "/media/Data/Music")
MOPIDY_PLAYLIST_DIR = "/home/tunnel/.local/share/mopidy/m3u"

account = MyPlexAccount()
plex = account.resource("alexandria").connect()

for playlist_name in PLAYLISTS:
    file_title = f"{playlist_name}.m3u8"
    playlist_file = Path(PLAYLIST_DIR) / file_title
    mopidy_playlist_file = Path(MOPIDY_PLAYLIST_DIR) / file_title
    ipod_playlist_file = Path(PLAYLIST_DIR) / ".ipod" / file_title
    with (
        open(playlist_file, "w") as plist,
        open(mopidy_playlist_file, "w") as mlist,
        open(ipod_playlist_file, "w") as podlist,
    ):
        for file in plist, mlist, podlist:
            file.write("#EXTM3U\n")
        for track in plex.playlist(playlist_name):
            p = Path(track.locations[0])
            # get relative path of music (i hate this impl)
            stripped_path = Path(p.parent.parent.name) / p.parent.name / p.name
            quoted_path = quote((bytes(stripped_path)))
            plist.write(f"{Path(MUSIC_DIR) / stripped_path.name}\n")
            podlist.write(f"{Path('/') / stripped_path}\n")
            mlist.write(f"local:track:{quoted_path}\n")
    print(f"wrote:\n{playlist_file}\n{ipod_playlist_file}\n{mopidy_playlist_file}\n")
