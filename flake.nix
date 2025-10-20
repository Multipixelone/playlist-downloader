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
        ];

        # packages
        playlist-download = pkgs.callPackage ./playlist-download.nix {
          inherit pythonModules pythonPackages version;
        };
        playlist-copy = pkgs.callPackage ./playlist-copy.nix {
          inherit pythonModules pythonPackages version;
        };
        rb-scrob = pkgs.callPackage ./rb-scrob.nix {
          inherit pythonModules pythonPackages version;
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
          default = self.packages.${system}.playlist-download;
        };
        devShells.default = env;
      }
    );
}
