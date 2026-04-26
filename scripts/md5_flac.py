import sys
import os
import logging
import subprocess as sp
import argparse
from multiprocessing import pool
from hashlib import md5
from mutagen import flac

FLAC_PROG = "flac"

logger = logging.getLogger(__name__)
CHUNK_SIZE = 512 * 1024


def scantree(path: str, recursive=False):
    for entry in os.scandir(path):
        if entry.is_dir():
            if recursive:
                yield from scantree(entry.path, recursive)
        else:
            yield entry


def get_flac(path: str):
    try:
        return flac.FLAC(path)
    except flac.FLACNoHeaderError:  # file is not flac
        return
    except flac.error as e:  # file < 4 bytes
        if str(e).startswith("file said 4 bytes"):
            return
        else:
            raise e


def get_flacs_no_md5(path: str, recursive=False):
    for entry in scantree(path, recursive):
        flac_thing = get_flac(entry.path)
        if flac_thing is not None and flac_thing.info.md5_signature == 0:
            yield flac_thing


def get_md5(flac_path: str) -> str:
    md_five = md5()
    with sp.Popen(
        [
            FLAC_PROG,
            "-ds",
            "--stdout",
            "--force-raw-format",
            "--endian=little",
            "--sign=signed",
            flac_path,
        ],
        stdout=sp.PIPE,
        stderr=sp.DEVNULL,
    ) as decoding:
        for chunk in iter(lambda: decoding.stdout.read(CHUNK_SIZE), b""):
            md_five.update(chunk)

    return md_five.hexdigest()


def set_md5(flac_thing: flac.FLAC):
    md5_hex = get_md5(flac_thing.filename)
    flac_thing.info.md5_signature = int(md5_hex, 16)
    flac_thing.tags.vendor = "MD5 added"
    flac_thing.save()
    return flac_thing


def main(path: str, recursive=False, check_only=False):
    found = False
    if check_only:
        for flac_thing in get_flacs_no_md5(path, recursive=recursive):
            logger.info(flac_thing.filename)
            found = True
    else:
        with pool.ThreadPool() as tpool:
            for flac_thing in tpool.imap(
                set_md5, get_flacs_no_md5(path, recursive=recursive)
            ):
                logger.info(f"MD5 added: {flac_thing.filename}")
                found = True
    if not found:
        logger.info("No flacs without MD5 found")


def parse_args():
    parser = argparse.ArgumentParser(prog="Add MD5")
    parser.add_argument("dirpath")
    parser.add_argument(
        "-r", "--recursive", help="Include subdirs", action="store_true"
    )
    parser.add_argument(
        "-c",
        "--check_only",
        help="don't add MD5s, just print the flacs that don't have them.",
        action="store_true",
    )
    args = parser.parse_args()

    return args.dirpath, args.recursive, args.check_only


if __name__ == "__main__":
    logger.setLevel(10)
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    main(*parse_args())
