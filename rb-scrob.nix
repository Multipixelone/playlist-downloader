{
  pythonPackages,
  pythonModules,
  version,
}:
pythonPackages.buildPythonApplication rec {
  inherit version;
  pname = "rb-scrob";
  format = "other";
  src = ./.;

  propagatedBuildInputs = pythonModules;

  dontUnpack = true;
  doCheck = false;
  pytestCheckHook = false;

  installPhase = ''
    install -Dm755 ${src}/scripts/rb-scrob.py $out/bin/${pname}
    sed -i '1s|^|#!/usr/bin/env python3\n|' $out/bin/${pname}
  '';
  meta.mainProgram = "rb-scrob";
}
