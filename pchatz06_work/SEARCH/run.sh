#!/bin/bash

# Usage check
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <search_type: local|global> <bench_list (colon-separated)>"
    echo "bench_list= Blender:Bwaves:Cam4:cactuBSSN:Exchange:Gcc:Lbm:Mcf:Parest:Povray:Wrf:Xalancbmk:Fotonik3d:Imagick:Leela:Omnetpp:Perlbench:Roms:x264:Xz"
    exit 1
fi

# Arguments
search_type="$1"       # 'local' or 'global'
bench_list_raw="$2"    # e.g., Blender:Gcc:Wrf

# Format current date-time
timestamp=$(date +"%d-%H-%M")

# Format suffix based on search type
if [ "$search_type" == "local" ]; then
    # Use bench list in the suffix
    bench_tag=$(echo "$bench_list_raw" | tr ':' '_')
    suffix="${timestamp}-local_${bench_tag}"
elif [ "$search_type" == "global" ]; then
    # Count number of benchmarks
    IFS=':' read -r -a bench_array <<< "$bench_list_raw"
    num_bench=${#bench_array[@]}
    suffix="${timestamp}-global-${num_bench}"
else
    echo "Invalid search type: $search_type (must be 'local' or 'global')"
    exit 1
fi

# Debug output
echo "Search Type : $search_type"
echo "Benchmarks  : $bench_list_raw"
echo "Suffix      : $suffix"

# Show what will run
echo "Search Type : $search_type"
echo "Benchmarks  : $bench_list_raw"
echo "Suffix      : $suffix"
echo "Running: python3 ./GeST/src/__init__.py \"$suffix\" \"$bench_list_raw\""

# Actually run the Python script
cd ./GeST/src/
python3 __init__.py "$suffix" "$bench_list_raw"
