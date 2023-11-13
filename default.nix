let
  sourcesTarball = fetchTarball "https://github.com/mutwo-org/mutwo-nix/archive/refs/heads/main.tar.gz";
  mutwo.reaper = import (sourcesTarball + "/mutwo.reaper/default.nix") {};
  mutwo.reaper-local = mutwo.reaper.overrideAttrs (
    finalAttrs: previousAttrs: {
       src = ./.;
    }
  );
in
  mutwo.reaper-local

