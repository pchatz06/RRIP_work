#!/bin/bash

benchmarks=(
  Blender Bwaves Cam4 cactuBSSN Exchange Gcc Lbm Mcf
  Parest Povray Wrf Xalancbmk Fotonik3d Imagick Leela
  Omnetpp Perlbench Roms x264 Xz
)

for bench in "${benchmarks[@]}"; do
  echo "Running $bench..."
  python3 run_srrip.py personal_best_global_policy/${bench}.txt ${bench}
done
