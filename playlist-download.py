from plexapi.myplex import MyPlexAccount
from pathlib import Path

PLAYLIST_DIR = "/home/tunnel/Music/Playlists"
MOPIDY_DIR = "/home/tunnel/.local/share/mopidy/m3u"
IPOD_DIR = "/home/tunnel/Music/.ipod"
MUSIC_DIR = "/media/Data/Music"
PLAYLISTS = {
    "monthly playlist": 24562,  # noqa
    "forgotten faves": 48614,  # noqa
    "good listening and learning": 20340,  # noqa
    "slipped through": 26220,  # noqa
    "vgm study": 53423,  # noqa
    "amtrak": 26224,  # noqa
    "mackin mabel": 61577,  # noqa
    "summer jams": 61792,  # noqa
}  # noqa

account = MyPlexAccount()
plex = account.resource("alexandria").connect()

