{
  lib,
  pythonPackages,
  pythonModules,
  flac,
  makeWrapper,
  version,
  src,
}:
pythonPackages.buildPythonApplication rec {
  inherit version src;
  pname = "md5-flac";
  format = "other";

  nativeBuildInputs = [ makeWrapper ];
  propagatedBuildInputs = pythonModules;

  dontUnpack = true;
  doCheck = false;

  installPhase = ''
    install -Dm755 ${src}/scripts/md5_flac.py $out/bin/${pname}
    sed -i '1s|^|#!/usr/bin/env python3\n|' $out/bin/${pname}
  '';

  postFixup = ''
    wrapProgram $out/bin/${pname} --prefix PATH : ${lib.makeBinPath [ flac ]}
  '';

  meta.mainProgram = pname;
}
