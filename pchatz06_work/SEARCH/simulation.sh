#!/bin/bash

trap "echo 'Terminating all child processes'; kill -- -$$" SIGINT SIGTERM EXIT

# Check arguments
if [[ "$#" -ne 3 ]]; then
    echo "Usage: $0 [-local|-global|-localglobal] [mutation_rate (M5, M10, etc)] [crossover (Onepoint/Uniform)]"
    exit 1
fi

MODE=$1
ARG1=$2
ARG2=$3

# Read benchmarks into array
benchmarks=()
while IFS= read -r line || [[ -n "$line" ]]; do
    benchmarks+=("$line")
done < benchmarks.txt

# Run local mode
if [[ "$MODE" == "-local" || "$MODE" == "-localglobal" ]]; then
    for bm in "${benchmarks[@]}"; do
        ./run.sh local "$bm" "$ARG1" "$ARG2" &
    done
fi

# Run global mode (all benchmarks as colon-separated string)
if [[ "$MODE" == "-global" || "$MODE" == "-localglobal" ]]; then
    all_benchmarks=$(IFS=:; echo "${benchmarks[*]}")
    ./run.sh global "$all_benchmarks" "$ARG1" "$ARG2"
fi