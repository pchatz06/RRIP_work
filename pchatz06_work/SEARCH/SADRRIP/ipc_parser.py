import os
import re
import sys


generation = sys.argv[1]
myID = sys.argv[2]
root_dir = sys.argv[3]
after_dir = sys.argv[4]
bench_list = sys.argv[5]


ipc_values = []

# Get a list of all files in the directory
folder_list = os.listdir(f'../BENCH_DIR/{root_dir}/{after_dir}/Results')

# Get the folder that has the unique id generation-myID at the end of the name
folder_list = [folder for folder in folder_list if folder.endswith("-" + generation + "-" + myID)]

# Extract the folder name from the list
folder = folder_list[0]

# Assume lru_baseline is available as in your snippet
# For demonstration, let's mock it
lru_baseline = {
    "gcc_r" : 0.453,
    "mcf_r" : 0.529,
    "cactuBSSN_r" : 0.8389,
    "namd_r" : 1.4088,
    "parest_r" : 0.8258,
    "lbm_r" : 0.8614,
    "omnetpp_r" : 0.2437,
    "wrf_r" : 1.1651,
    "cam4_r" : 0.7568,
    "fotonik3d_r" : 0.6822,
    "roms_r" : 0.9455,
    "xz_r" : 0.6539
}

INSTRUCTIONS = 150000000

# --- 1. Process Benchmarks ---
benchmarks_raw = bench_list.split(":")
benchmark_data = {} # To store all extracted data


for benchmark_full_name in benchmarks_raw:
    parts = benchmark_full_name.split('.')
    benchmark_name = parts[1]
    input_name = parts[3]
    region_name = parts[4]
    
    # Extract normalized weight
    try:
        
        match = re.search(r'w_\d+\.\d+_(\d+\.\d+)', benchmark_full_name)
        if match:
            normalized_weight_str =  match.group(1)
            normalized_weight = float(normalized_weight_str)
        else:
            print("Pattern not found.")
    except (ValueError, IndexError):
        print(f"Warning: Could not extract normalized weight for {benchmark_full_name}.")
        exit(-1)

    # Construct the output filename
    output_filename = f"{benchmark_full_name}.out"
    champsim_full_filename = f"../BENCH_DIR/{root_dir}/{after_dir}/Results/" + folder + "/" + output_filename

    ipc_value = None
    # Simulate opening and reading the file
    with open(champsim_full_filename, 'r') as f:
        for line in f:
            if "Finished CPU" in line and "IPC:" in line:
                ipc_index = line.find("IPC:") + 5
                try:
                    ipc_value = float(line[ipc_index:].split()[0])
                except (ValueError, IndexError):
                    print(f"Warning: Could not parse IPC value from line: '{line}' in file {output_filename}")
                break

    if ipc_value is None:
        print(f"Warning: IPC not found in {output_filename}. Skipping benchmark {benchmark_full_name}.")
        exit(-1)


    # Calculate CPI
    cpi_value = 1 / ipc_value

    # Store data
    if benchmark_name not in benchmark_data:
        benchmark_data[benchmark_name] = {}
    if input_name not in benchmark_data[benchmark_name]:
        benchmark_data[benchmark_name][input_name] = []

    benchmark_data[benchmark_name][input_name].append({
        "full_name": benchmark_full_name,
        "region": region_name,
        "normalized_weight": normalized_weight,
        "ipc": ipc_value,
        "cpi": cpi_value
    })

# --- 2. Calculate Weighted CPI for Each Input and Average CPI for Each Benchmark ---

final_results = {}

for benchmark_name, inputs_data in benchmark_data.items():
    total_benchmark_cpi = 0
    num_inputs_for_benchmark = 0

    final_results[benchmark_name] = {
        "inputs": {},
        "average_cpi": 0
    }

    for input_name, regions_data in inputs_data.items():
        total_input_weighted_cpi = 0
        total_input_instructions = 0 # To calculate total instructions for this input across regions

        final_results[benchmark_name]["inputs"][input_name] = {
            "weighted_cpi": 0,
            "regions": {}
        }

        for region_info in regions_data:
            normalized_weight = region_info["normalized_weight"]
            cpi_region = region_info["cpi"]
            region_name = region_info["region"]

            # Option 1: Weighted CPI for the input by summing (weight * CPI) of its regions
            weighted_cpi_per_region = normalized_weight * cpi_region
            total_input_weighted_cpi += weighted_cpi_per_region


            final_results[benchmark_name]["inputs"][input_name]["regions"][region_name] = {
                "cpi": cpi_region,
                "normalized_weight": normalized_weight,
                "weighted_cpi_contribution": weighted_cpi_per_region
            }

        # Assign the calculated weighted CPI for the input
        final_results[benchmark_name]["inputs"][input_name]["weighted_cpi"] = total_input_weighted_cpi

        # For average CPI of the benchmark, we need to sum up the CPIs of its inputs
        # "calculate the average CPI for each benchmark, by dividing the total CPI of the different inputs with the number of inputs."
        # This implies summing the *input's* CPIs (which we calculated as `total_input_weighted_cpi`)
        total_benchmark_cpi += total_input_weighted_cpi
        num_inputs_for_benchmark += 1

    if num_inputs_for_benchmark > 0:
        final_results[benchmark_name]["average_cpi"] = total_benchmark_cpi / num_inputs_for_benchmark

# --- 3. Display Results ---
# print("\n--- Processed Benchmark Data ---")

speedup = []
for benchmark_name, data in final_results.items():
    # print(f"\nBenchmark: {benchmark_name}")
    # for input_name, input_data in data["inputs"].items():
    #     print(f"  Input: {input_name}")
    #     print(f"    Total Weighted CPI for Input: {input_data['weighted_cpi']:.4f}")
    #     for region_name, region_data in input_data["regions"].items():
    #         print(f"      Region: {region_name}")
    #         print(f"        CPI: {region_data['cpi']:.4f}")
    #         print(f"        Normalized Weight: {region_data['normalized_weight']:.4f}")
    #         print(f"        Weighted CPI Contribution: {region_data['weighted_cpi_contribution']:.4f}")
    #     print(f"  Average CPI for Benchmark '{benchmark_name}': {data['average_cpi']:.4f}")
    speedup.append((1/float(data['average_cpi']))/(float(lru_baseline[benchmark_name])))

avg_speedup = sum(speedup)/len(speedup)
print("{:.5f}".format(avg_speedup))
