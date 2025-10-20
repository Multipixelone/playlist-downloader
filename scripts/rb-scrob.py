from os import environ
from pathlib import Path
from datetime import datetime
from mutagen.apev2 import APEv2

# MUSIC_DIR = environ.get("MUSIC_DIR", "/media/Data/Music")
MUSIC_DIR = "/volume1/Media/TranscodedMusic"
IPOD_DIR = environ.get("IPOD_DIR", "/media/Data/Music")
RB_LOG_FILE = Path(IPOD_DIR) / ".rockbox" / "playback.log"
LOG_DIR = Path.home() / "Music" / "Rockbox"
LOG_FILE = Path(LOG_DIR) / f"scrobbler_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
HEADER = f"#AUDIOSCROBBLER/1.1\n#TZ/UNKNOWN\n#CLIENT/Rockbox ipodvideo\n#Log file generated {datetime.now()}\n"


def threshold(length_ms: int):
    return length_ms / 100 * 50


with open(RB_LOG_FILE) as r, open(LOG_FILE, "w") as f:
    f.write(HEADER)
    print(f"opening {RB_LOG_FILE} for writing...")
    for line in r:
        li = line.strip()
        if not line.startswith("#"):
            split = li.split(":")
            stamp = split[0]
            elapsed = int(split[1])
            len = int(split[2])

            cleaned_path = split[3].removeprefix("/<HDD0>").removeprefix("/")
            file = APEv2(Path(MUSIC_DIR) / cleaned_path)
            rating = "L" if elapsed >= threshold(len) else "S"

            f.write(
                f"{file['artist']}\t{file['album']}\t{file['title']}\t{file['track']}\t{len // 1000}\t{rating}\t{stamp}\n"
            )
