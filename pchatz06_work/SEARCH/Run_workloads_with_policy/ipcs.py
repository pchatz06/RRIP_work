import os
import re

# Update these paths
out_dir = "./GOOD_SRRIP/Results/results-perceptron-next_line-ip_stride-drrip-flex-1core-3333323233333232-3333323233333232-10-1-0-0-0-0-0-0-4044404440444044-1-232"
# out_dir = "./outputs_perceptron-next_line-ip_stride-lru-1core"
gz_dir = "/mnt/beegfs/pchatz06/selected_traces"

ipc_pattern = re.compile(r"CPU 0 cumulative IPC:\s+([\d.]+)")
input_pattern = re.compile(r"\.input(\d+)")

results = []

for out_file in os.listdir(out_dir):
    if not out_file.endswith(".out"):
        continue

    prefix = out_file[:-4]  # strip ".out"
    out_path = os.path.join(out_dir, out_file)

    # Match .gz file with same prefix
    matching_gz = next(
        (f for f in os.listdir(gz_dir) if f.startswith(prefix) and f.endswith(".gz")),
        None
    )
    if not matching_gz:
        continue

    # Extract IPC
    ipc_value = None
    with open(out_path, "r") as f:
        for line in f:
            match = ipc_pattern.search(line)
            if match:
                ipc_value = float(match.group(1))
                break

    if ipc_value is not None:
        # Extract benchmark number and input number for sorting
        bench_match = re.match(r"^(\d+)", matching_gz)
        input_match = input_pattern.search(matching_gz)

        bench_num = int(bench_match.group(1)) if bench_match else 9999
        input_num = int(input_match.group(1)) if input_match else 9999

        results.append((bench_num, input_num, matching_gz, ipc_value))

# Sort by benchmark number, then input number
results.sort()

# Print the output
for _, _, filename, ipc in results:
    print(f"{filename}: {ipc}")
