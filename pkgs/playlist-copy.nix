{
  pythonPackages,
  pythonModules,
  version,
  src,
}:
pythonPackages.buildPythonApplication rec {
  inherit version src;
  pname = "playlist-copy";
  format = "other";

  propagatedBuildInputs = pythonModules;

  dontUnpack = true;
  doCheck = false;

  installPhase = ''
    install -Dm755 ${src}/scripts/playlist-copy.py $out/bin/${pname}
    sed -i '1s|^|#!/usr/bin/env python3\n|' $out/bin/${pname}
  '';
  meta.mainProgram = pname;
}
