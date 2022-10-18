with import <nixpkgs> {};
with pkgs.python3Packages;

let

  mutwo-core-archive = builtins.fetchTarball "https://github.com/mutwo-org/mutwo.core/archive/97aea97f996973955889630c437ceaea405ea0a7.tar.gz";
  mutwo-core = import (mutwo-core-archive + "/default.nix");

in

  buildPythonPackage rec {
    name = "mutwo.reaper";
    src = fetchFromGitHub {
      owner = "mutwo-org";
      repo = name;
      rev = "16793da38f743bc5789fe61aada990ae815ced5b";
      sha256 = "sha256-AstM1sPYjcKFOOPaK0/UySMcA2R4BMNcfSUFCN4qLTA=";
    };
    propagatedBuildInputs = [ 
      mutwo-core
    ];
    doCheck = true;
  }
