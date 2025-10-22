from os import environ
from pathlib import Path
import shutil
from datetime import datetime
from mediafile import MediaFile, UnreadableFileError

MUSIC_DIR = environ.get("MUSIC_DIR", "/media/Data/Music")
IPOD_DIR = environ.get("IPOD_DIR", "/media/Data/Music")
RB_LOG_FILE = Path(IPOD_DIR) / ".rockbox" / "playback.log"
# RB_LOG_FILE = Path("./playback.log")
LOG_DIR = Path.home() / "Music" / "Rockbox"
LOG_FILE = Path(LOG_DIR) / f"scrobbler_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
HEADER = "#AUDIOSCROBBLER/1.1\n#TZ/UNKNOWN\n#CLIENT/Rockbox ipodvideo\n"


def threshold(length_ms: int):
    return length_ms / 100 * 50


def find_track(path: Path) -> Path:
    search_pattern = f"{path.stem}.*"
    matches = path.parent.glob(search_pattern)
    return next(matches)


with open(RB_LOG_FILE) as r, open(LOG_FILE, "w") as f:
    _ = f.write(HEADER)
    for line in r:
        li = line.strip()
        if not line.startswith("#"):
            split = li.split(":")
            # pull useful information out of split
            stamp = int(split[0])
            elapsed = int(split[1])
            len = int(split[2])
            cleaned_path = split[3].removeprefix("/<HDD0>").removeprefix("/")

            # track listened or not based on threshold
            rating = "L" if elapsed >= threshold(len) else "S"

            # use found flac file, otherwise pull from my transcoded music directory
            try:
                found_path = find_track(Path(MUSIC_DIR) / cleaned_path)
            except StopIteration:
                found_path = Path("/media/Data/TranscodedMusic") / cleaned_path

            # use MediaFile to pull metadata into dict
            try:
                media_file = MediaFile(found_path)
                metadata = {
                    "title": media_file.title,
                    "artist": media_file.artist,
                    "album": media_file.album,
                    "album_artist": media_file.albumartist,
                    "track": media_file.track,
                    "mb_id": media_file.mb_trackid,
                }
            except UnreadableFileError:
                print(f"Failed to read file with MediaFile: {found_path}")

            _ = f.write(
                f"{metadata['artist']}\t{metadata['album']}\t{metadata['title']}\t{metadata['track']}\t{len // 1000}\t{rating}\t{stamp}\t{metadata['mb_id']}\n"
            )
    print(LOG_FILE)
    _ = shutil.move(RB_LOG_FILE, Path(IPOD_DIR) / ".rockbox" / "playback_old.log")
