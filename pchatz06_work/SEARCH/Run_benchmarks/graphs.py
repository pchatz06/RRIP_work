import matplotlib.pyplot as plt
import numpy as np
import os

# Title of the plot and output file
title = "speedup_comparison"

# Define IPCs as lists of tuples with ".out" in the keys
lru = {
    "Xalancbmk": 0.386926,
    "Cam4": 0.726485,
    "x264": 1.43352,
    "Gcc": 0.355163,
    "Wrf": 0.831513,
    "Lbm": 0.632519,
    "Exchange": 1.12309,
    "Leela": 0.547438,
    "Bwaves": 1.0125,
    "Povray": 0.364268,
    "Xz": 0.972789,
    "Perlbench": 0.451448,
    "Roms": 1.0212,
    "Fotonik3d": 0.799069,
    "Parest": 0.934336,
    "Mcf": 0.407402,
    "Imagick": 2.26801,
    "cactuBSSN": 0.761405,
    "Blender": 0.673227,
    "Omnetpp": 0.246087
}

best_global = {
    "Xalancbmk": 0.430458,
    "Cam4": 0.732574,
    "x264": 1.42565,
    "Gcc": 0.357265,
    "Wrf": 0.855918,
    "Lbm": 0.669897,
    "Exchange": 1.12309,
    "Leela": 0.547404,
    "Bwaves": 1.01249,
    "Povray": 0.364266,
    "Xz": 0.978514,
    "Perlbench": 0.45111,
    "Roms": 0.948083,
    "Fotonik3d": 0.806872,
    "Parest": 1.03834,
    "Mcf": 0.405614,
    "Imagick": 2.26751,
    "cactuBSSN": 0.755725,
    "Blender": 0.683457,
    "Omnetpp": 0.248399
}

personal_best_global = {
    "Blender": 0.684318,
    "Bwaves": 1.01249,
    "Cam4": 0.733839,
    "cactuBSSN": 0.76085,
    "Exchange": 1.12309,
    "Gcc": 0.357677,
    "Lbm": 0.670762,
    "Mcf": 0.405597,
    "Parest": 1.03881,
    "Povray": 0.364268,
    "Wrf": 0.852513,
    "Xalancbmk": 0.437395,
    "Fotonik3d": 0.809919,
    "Imagick": 2.26801,
    "Leela": 0.547438,
    "Omnetpp": 0.248524,
    "Perlbench": 0.451448,
    "Roms": 1.01333,
    "x264": 1.43082,
    "Xz": 0.979162
}

local_best = {
    "Blender": 0.684278,
    "Bwaves": 1.01249,
    "Cam4": 0.734113,
    "cactuBSSN": 0.762684,
    "Exchange": 1.12309,
    "Gcc": 0.358662,
    "Lbm": 0.683462,
    "Mcf": 0.412104,
    "Parest": 1.03613,
    "Povray": 0.364257,
    "Wrf": 0.858891,
    "Xalancbmk": 0.438637,
    "Fotonik3d": 0.810916,
    "Imagick": 2.26801,
    "Leela": 0.547438,
    "Omnetpp": 0.249192,
    "Perlbench": 0.451448,
    "Roms": 1.01222,
    "x264": 1.43792,
    "Xz": 0.979808
}

good_srrip = {
    "Xalancbmk": 0.431222,
    "Cam4": 0.733071,
    "x264": 1.42547,
    "Gcc": 0.35651,
    "Wrf": 0.835995,
    "Lbm": 0.675922,
    "Exchange": 1.12309,
    "Leela": 0.547394,
    "Bwaves": 1.01249,
    "Povray": 0.364266,
    "Xz": 0.977368,
    "Perlbench": 0.45111,
    "Roms": 0.950096,
    "Fotonik3d": 0.809281,
    "Parest": 1.03212,
    "Mcf": 0.405028,
    "Imagick": 2.26751,
    "cactuBSSN": 0.755655,
    "Blender": 0.68253,
    "Omnetpp": 0.247504
}


# Final benchmark order + average
benchmarks = [
    'Blender', 'Bwaves', 'Cam4', 'cactuBSSN', 'Exchange', 'Gcc', 'Lbm', 'Mcf', 'Parest', 'Povray',
    'Wrf', 'Xalancbmk', 'Fotonik3d', 'Imagick', 'Leela', 'Omnetpp', 'Perlbench', 'Roms', 'x264', 'Xz'
]

# Compute speedups
def compute_speedups(policy_dict):
    speedups = [policy_dict[b] / lru[b] for b in benchmarks]
    avg = sum(speedups) / len(speedups)
    return speedups + [avg]  # append average

values1 = compute_speedups(best_global)
values2 = compute_speedups(personal_best_global)
values3 = compute_speedups(local_best)
values4 = compute_speedups(good_srrip)

# Add 'Average' to benchmark labels
benchmarks += ['Average']

# Debug output
print("global_best:", values1)
print("global_personal_best:", values2)
print("local_best:", values3)
print("good srrip:", values4)

# X-axis setup
x = np.arange(len(benchmarks))
width = 0.2

# Create plot
plt.figure(figsize=(18, 6))
plt.bar(x - 1.5 * width, values4, width, label='good_SRRIP', color='skyblue')
plt.bar(x - 0.5 * width, values1, width, label='best_global_policy', color='pink')
plt.bar(x + 0.5 * width, values2, width, label='personal_best_global_policy', color='orange')
plt.bar(x + 1.5 * width, values3, width, label='local_best_policy', color='green')

# Formatting
plt.xlabel('Benchmark')
plt.ylabel('Speedup')
plt.title(f'{title}')
plt.xticks(x, benchmarks, rotation=45, ha='right')
plt.ylim(0.950, 1.200)
plt.yticks(np.arange(0.950, 1.201, 0.025))
plt.legend()
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.axhline(y=1.000, color='red', linestyle='--', linewidth=1.5)

# Save the plot
os.makedirs("GRAPHS", exist_ok=True)
plt.savefig(f"GRAPHS/{title}.png", dpi=300)
plt.close()
