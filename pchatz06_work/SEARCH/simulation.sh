#!/bin/bash

trap "echo 'Terminating all child processes'; kill -- -$$" SIGINT SIGTERM EXIT

# Check arguments
if [[ "$#" -ne 4 ]]; then
    echo "Usage: $0 [benchmarks file path] [-local|-global|-localglobal] [mutation_rate (M5, M10, etc)] [crossover (Onepoint/Uniform)]"
    exit 1
fi

bench_path=$1
MODE=$2
ARG1=$3
ARG2=$4

# Read benchmarks into array
benchmarks=()
while IFS= read -r line || [[ -n "$line" ]]; do
    benchmarks+=("$line")
done < "$bench_path"

# Run local mode
if [[ "$MODE" == "-local" || "$MODE" == "-localglobal" ]]; then
    for bm in "${benchmarks[@]}"; do
        ./run.sh local "$bm" "$ARG1" "$ARG2" &
    done
    if [[ "$MODE" != "-localglobal" ]]; then
        wait  # Only wait if not -localglobal
    fi
fi

# Run global mode (all benchmarks as colon-separated string)
if [[ "$MODE" == "-global" || "$MODE" == "-localglobal" ]]; then
    all_benchmarks=$(IFS=:; echo "${benchmarks[*]}")
    ./run.sh global "$all_benchmarks" "$ARG1" "$ARG2"
fi