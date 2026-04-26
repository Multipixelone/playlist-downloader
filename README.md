<h1 align="center">playlist-downloader</h1>
<div align="center">

[![Build](https://img.shields.io/github/actions/workflow/status/Multipixelone/playlist-downloader/ci.yml?style=for-the-badge&logo=github&label=build&color=a6e3a1&labelColor=313244&logoColor=cdd6f4)](https://github.com/Multipixelone/playlist-downloader/actions)
[![License](https://img.shields.io/github/license/Multipixelone/playlist-downloader?style=for-the-badge&logo=creativecommons&color=b4befe&labelColor=313244&logoColor=cdd6f4)](LICENSE)
![Plex](https://img.shields.io/badge/plex-playlists-fab387?style=for-the-badge&logo=plex&labelColor=313244&logoColor=cdd6f4)
![Nix](https://img.shields.io/badge/nix-flakes-89b4fa?style=for-the-badge&logo=nixos&labelColor=313244&logoColor=cdd6f4)

</div>

My collection of [Plex](https://plex.tv/) playlist scripts for NixOS, packaged and built with Nix flakes.

## Scripts

- [`playlist-download`](./scripts/playlist-download.py) — download tracks from Plex playlists to local storage
- [`playlist-copy`](./scripts/playlist-copy.py) — copy playlists between Plex libraries or destinations
- [`rb-scrob`](./scripts/rb-scrob.py) — scrobble Rockbox playback logs back to listening services
- [`md5_flac`](./scripts/md5_flac.py) — verify and refresh MD5 checksums on FLAC files

## Development

```bash
nix flake check
nix build .#packages.x86_64-linux.default
```
