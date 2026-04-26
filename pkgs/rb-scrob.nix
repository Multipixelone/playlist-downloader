{
  pythonPackages,
  pythonModules,
  version,
  src,
}:
pythonPackages.buildPythonApplication rec {
  inherit version src;
  pname = "rb-scrob";
  format = "other";

  propagatedBuildInputs = pythonModules;

  dontUnpack = true;
  doCheck = false;

  installPhase = ''
    install -Dm755 ${src}/scripts/rb-scrob.py $out/bin/${pname}
    sed -i '1s|^|#!/usr/bin/env python3\n|' $out/bin/${pname}
  '';
  meta.mainProgram = pname;
}
