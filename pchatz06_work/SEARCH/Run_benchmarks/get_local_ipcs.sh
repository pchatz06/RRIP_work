#!/bin/bash

benchmarks=(
  Blender Bwaves Cam4 cactuBSSN Exchange Gcc Lbm Mcf
  Parest Povray Wrf Xalancbmk Fotonik3d Imagick Leela
  Omnetpp Perlbench Roms x264 Xz
)

for bench in "${benchmarks[@]}"; do
  result_dir="SRRIP_BEST_${bench}/Results"

  # Get all subdirectories in the result_dir
  dirs=($(find "$result_dir" -mindepth 1 -maxdepth 1 -type d))

  if [ "${#dirs[@]}" -eq 0 ]; then
    echo "Warning: No subdirectory found in $result_dir"
    continue
  else
    # Only one directory
    inner_dir="${dirs[0]}"
  fi

  # echo "Running for $bench (dir: $(basename "$inner_dir"))"
  python3 get_ipcs.py "$inner_dir"
done
