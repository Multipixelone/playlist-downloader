from plexapi.myplex import MyPlexAccount
from os import environ
from pathlib import Path
from urllib.parse import quote

PLAYLISTS = [
    "00 monthly playlist",
    "01 amtrak",
    "02 vgm study",
    "03 jazz i dig",
    "04 in da electric jungle",
    "05 apocalypse",
    "06 mortenkaisen ult",
    "07 city pop",
    "08 breakcore vsinger",
    "99 last month liked",
    "14 u have to understand video game music is great",
    "50 good listening & learning",
    "rainlist",
    "snowy vgm",
    "vgm water",
    "y lastfm top all time",
    "y lastfm top six months",
    "mt madness",
    "mazda bitch strip",
]

PLAYLIST_DIR = environ.get("PLAYLIST_DIR", "/home/tunnel/Music/Playlists")
MUSIC_DIR = environ.get("MUSIC_DIR", "/media/Data/Music")
MOPIDY_PLAYLIST_DIR = environ.get(
    "MOPIDY_PLAYLISTS", "/home/tunnel/.local/share/mopidy/m3u"
)

account = MyPlexAccount()
plex = account.resource("alexandria").connect()

for playlist_name in PLAYLISTS:
    file_title = f"{playlist_name}.m3u8"
    playlist_file = Path(PLAYLIST_DIR) / file_title
    mopidy_playlist_file = Path(MOPIDY_PLAYLIST_DIR) / file_title
    ipod_playlist_file = Path(PLAYLIST_DIR) / ".ipod" / file_title
    mpd_playlist_file = Path(PLAYLIST_DIR) / ".mpd" / f"{playlist_name}.m3u"
    with (
        open(playlist_file, "w") as plist,
        open(mopidy_playlist_file, "w") as mlist,
        open(ipod_playlist_file, "w") as podlist,
        open(mpd_playlist_file, "w") as mpdlist,
    ):
        for file in plist, mlist, podlist:
            file.write("#EXTM3U\n")
        for track in plex.playlist(playlist_name):
            p = Path(track.locations[0])
            # get relative path of music (i hate this impl)
            stripped_path = Path(p.parent.parent.name) / p.parent.name / p.name
            quoted_path = quote((bytes(stripped_path)))
            plist.write(f"{Path(MUSIC_DIR) / stripped_path}\n")
            # podlist.write(f"{Path('/') / stripped_path}.opus\n")
            podlist.write(
                f"{Path('/') / p.parent.parent.name / p.parent.name / p.stem}.mpc\n"
            )
            mpdlist.write(f"{Path(stripped_path)}\n")
            mlist.write(f"local:track:{quoted_path}\n")
    print(
        f"wrote:\n{playlist_file}\n{ipod_playlist_file}\n{mopidy_playlist_file}\n{mpd_playlist_file}"
    )
