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
      python = pkgs.python3.override {
        self = python;
      };
      app = pkgs.python3Packages.buildPythonApplication rec {
        inherit python;
        pname = "playlist-download";
        version = toString (self.shortRev or self.dirtyShortRev or self.lastModified or "unknown");
        format = "other";
        src = ./.;

        propagatedBuildInputs = pythonModules;

        dontUnpack = true;
        doCheck = false;
        pytestCheckHook = false;

        installPhase = ''
          install -Dm755 ${src}/playlist-download.py $out/bin/${pname}
          sed -i '1s|^|#!/usr/bin/env python3\n|' $out/bin/${pname}
        '';
        meta.mainProgram = "playlist-download";
      };
      env = pkgs.mkShell {
        venvDir = "./.venv";
        buildInputs = [
          python
          pythonModules
          pythonPackages.venvShellHook
          pkgs.autoPatchelfHook
        ];
        name = "playlist";
        DIRENV_LOG_FORMAT = "";
      };
    in {
      packages = {
        playlist-download = app;
        default = self.packages.${system}.playlist-download;
      };
      devShells.default = env;
    });
}
