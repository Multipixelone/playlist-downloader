{
  description = "Multipixelone playlist downloader";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      pythonPackages = pkgs.python3Packages;
      pythonModules = with pythonPackages; [
        plexapi
      ];
      version = toString (self.shortRev or self.dirtyShortRev or self.lastModified or "unknown");
      playlist-download = pkgs.callPackage ./playlist-download.nix {inherit pythonModules pythonPackages self version;};
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
    in {
      packages = {
        playlist-download = playlist-download;
        default = self.packages.${system}.playlist-download;
      };
      devShells.default = env;
    });
}
