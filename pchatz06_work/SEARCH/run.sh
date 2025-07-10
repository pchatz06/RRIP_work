#!/bin/bash

# Usage check
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <search_type: local|global> <bench_list (colon-separated)> <mutation_rate (M5)> <crossover (Random/Onepoint)>"
    echo "bench_list= Blender:Bwaves:Cam4:cactuBSSN:Exchange:Gcc:Lbm:Mcf:Parest:Povray:Wrf:Xalancbmk:Fotonik3d:Imagick:Leela:Omnetpp:Perlbench:Roms:x264:Xz"
    exit 1
fi

# Arguments
search_type="$1"       # 'local' or 'global'
bench_list_raw="$2"    # e.g., Blender:Gcc:Wrf
mutation_rate="$3"
crossover="$4"

# Format current date-time
timestamp=$(date +"%d-%H-%M")

# Format suffix based on search type
if [ "$search_type" == "local" ]; then
    # Use bench list in the suffix
    bench_tag=$(echo "$bench_list_raw" | tr ':' '_')
    suffix="${timestamp}-${mutation_rate}-${crossover}-local_${bench_tag}"
elif [ "$search_type" == "global" ]; then
    # Count number of benchmarks
    IFS=':' read -r -a bench_array <<< "$bench_list_raw"
    suffix="${timestamp}-${mutation_rate}-${crossover}-global"
else
    echo "Invalid search type: $search_type (must be 'local' or 'global')"
    exit 1
fi

# Show what will run
echo "Search Type : $search_type"
echo "Benchmarks  : $bench_list_raw"
echo "Suffix      : $suffix"
echo "Running: python3 ./GeST/src/__init__.py \"$suffix\" \"$bench_list_raw\""

# Actually run the Python script
cd ./GeST/src/
python3 __init__.py "$suffix" "$bench_list_raw"
