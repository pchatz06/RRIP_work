import os
import sys

if len(sys.argv) != 2:
    print("Usage: python parse_ipc.py <output_directory>")
    sys.exit(1)

output_dir = sys.argv[1]

ipc_results = []

for filename in os.listdir(output_dir):
    if "output" in filename or filename.endswith(".out"):
        filepath = os.path.join(output_dir, filename)
        try:
            with open(filepath, "r") as file:
                for line in file:
                    if "CPU 0 cumulative IPC:" in line:
                        parts = line.strip().split()
                        try:
                            ipc_value = float(parts[4])
                            ipc_results.append((filename, ipc_value))
                        except ValueError:
                            print(f"Could not parse IPC value in {filepath}")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            continue

# Print results
for ipc_res in ipc_results:
    print(ipc_res)
