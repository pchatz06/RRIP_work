import os
from collections import defaultdict

# Change this to your directory with the benchmark files
benchmark_dir = "/mnt/beegfs/pchatz06/selected_traces"
output_dir = "./grouped_benchmarks_txt"


os.makedirs(output_dir, exist_ok=True)

# Dictionary to hold benchmark name => list of matching files
benchmark_files = defaultdict(list)

for fname in os.listdir(benchmark_dir):
    if not os.path.isfile(os.path.join(benchmark_dir, fname)):
        continue
    if "refrate" in fname:
        continue  # Skip files with "refrate" in the name
    parts = fname.split('.')
    if len(parts) < 2:
        continue
    benchmark = parts[1]  # Extract "gcc_r", "mcf_r", etc.
    benchmark_files[benchmark].append(fname)

# Write each benchmark's files to a separate text file
for bench, files in benchmark_files.items():
    out_path = os.path.join(output_dir, f"{bench}.txt")
    with open(out_path, "w") as f:
        for file in sorted(files):
            f.write(file + "\n")

print("Done. Filtered benchmark files saved to:", output_dir)
