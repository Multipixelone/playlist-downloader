{
  description = "Multipixelone playlist downloader";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        # use git commit as version (i don't like this impl but i'll be brave)
        version = toString (self.shortRev or self.dirtyShortRev or self.lastModified or "unknown");
        pkgs = nixpkgs.legacyPackages.${system};
        # python definitions & modules
        pythonPackages = pkgs.python3Packages;
        pythonModules = with pythonPackages; [
          plexapi
          mutagen
          mediafile
        ];

        # packages
        mkScriptSrc =
          script:
          pkgs.lib.fileset.toSource {
            root = ./.;
            fileset = script;
          };
        playlist-download = pkgs.callPackage ./pkgs/playlist-download.nix {
          inherit pythonModules pythonPackages version;
          src = mkScriptSrc ./scripts/playlist-download.py;
        };
        playlist-copy = pkgs.callPackage ./pkgs/playlist-copy.nix {
          inherit pythonModules pythonPackages version;
          src = mkScriptSrc ./scripts/playlist-copy.py;
        };
        rb-scrob = pkgs.callPackage ./pkgs/rb-scrob.nix {
          inherit pythonModules pythonPackages version;
          src = mkScriptSrc ./scripts/rb-scrob.py;
        };
        md5-flac = pkgs.callPackage ./pkgs/md5-flac.nix {
          inherit pythonModules pythonPackages version;
          src = mkScriptSrc ./scripts/md5_flac.py;
        };

        # devEnv
        env = pkgs.mkShell {
          venvDir = "./.venv";
          buildInputs = [
            pythonModules
            pythonPackages.python
            pythonPackages.venvShellHook
            pkgs.autoPatchelfHook
          ];
          name = "playlist";
          DIRENV_LOG_FORMAT = "";
        };
      in
      {
        packages = {
          playlist-download = playlist-download;
          playlist-copy = playlist-copy;
          rb-scrob = rb-scrob;
          md5-flac = md5-flac;
          default = self.packages.${system}.playlist-download;
        };
        devShells.default = env;
      }
    );
}
