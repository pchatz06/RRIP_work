import os
import re
from collections import defaultdict

DIRECTORY = './outputs_perceptron-next_line-ip_stride-lru-1core'  # Change this to your actual directory
INSTRUCTIONS = 150_000_000
mpki_data = defaultdict(list)
low_mpki_count = 0

def extract_input_number(filename):
    match = re.search(r'input(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

for filename in os.listdir(DIRECTORY):
    if not filename.endswith(".out"):
        continue
    full_path = os.path.join(DIRECTORY, filename)
    with open(full_path, 'r') as file:
        content = file.read()
        match = re.search(r'LLC TOTAL\s+ACCESS:\s+\d+\s+HIT:\s+\d+\s+MISS:\s+(\d+)', content)
        if match:
            misses = int(match.group(1))
            mpki = (misses / INSTRUCTIONS) * 1000
            parts = filename.split('.')
            benchmark_key = '.'.join(parts[:2])  # e.g., 502.gcc_r
            if "train" in filename:
                category = "train"
            elif "refrate" in filename:
                category = "refrate"
            elif "test" in filename:
                category = "test"
            else:
                category = "unknown"
            full_key = f"{benchmark_key}.{category}"
            input_num = extract_input_number(filename)
            mpki_data[full_key].append((filename, mpki, input_num))
            if mpki < 1:
                low_mpki_count += 1

# Print results sorted by input number
for key in sorted(mpki_data.keys()):
    #print(f"\n{key}:")
    for filename, mpki, input_num in sorted(mpki_data[key], key=lambda x: x[2]):
        print(f"  {filename}: MPKI: {mpki:.4f}")

print(f"\nTotal MPKI < 1: {low_mpki_count}")
