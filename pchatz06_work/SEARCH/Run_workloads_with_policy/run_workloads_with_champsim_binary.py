import os
import sys
import subprocess

# === Parse Arguments ===
if len(sys.argv) != 3:
    print("Usage: python script.py <binary_path> <benchmarks_file>")
    sys.exit(1)


binary_path = sys.argv[1]
benchmarks_file = sys.argv[2]
traces_dir = "/mnt/beegfs/pchatz06/selected_traces"

# === Extract binary name and build arguments ===
binary_name = os.path.basename(binary_path)  # e.g., perceptron-next_line-ip_stride-srrip-1core
binary_dir = os.path.dirname(binary_path)    # e.g., ../SADRRIP/bin
binary_base = os.path.splitext(binary_name)[0]  # Remove .exe if present

# Remove '-1core' suffix
if binary_base.endswith('-1core'):
    binary_base = binary_base[:-7]  # remove '-1core'

build_args = binary_base.split('-')  # e.g., ['perceptron', 'next_line', 'ip_stride', 'srrip']
build_args.append('1')               # Add core count

# === Prepare output directory ===
output_dir = f"outputs_{os.path.basename(binary_path)}"
os.makedirs(output_dir, exist_ok=True)

# === Check and build if binary doesn't exist ===
if os.path.exists(binary_path):
    print("ChampSim build exists!")
else:
    print("ChampSim build does not exist. Please build champsim first..")
    exit(-1)

# === Read benchmarks ===
with open(benchmarks_file, 'r') as file:
    benchmarks = [line.strip() for line in file if line.strip()]

workloads = []
for root, dirs, files in os.walk(traces_dir):
    for file in files:
        if file.endswith(".gz"):
            for bench in benchmarks:
                if bench in file:
                    workloads.append(os.path.join(root, file))

# === Generate commands ===
commands = []
for workload in workloads:
    out_file = os.path.join(output_dir, f"{str(os.path.basename(workload))[:-10]}.out")
    cmd = f"{binary_path} -warmup_instructions 100000000 -simulation_instructions 150000000 -traces {workload} >& {out_file}"
    commands.append(cmd)

# === Generate SLURM script ===
tcsh_command_array = ' '.join([f'"{cmd}"' for cmd in commands])
slurm_script = f"""#!/bin/tcsh
#SBATCH --job-name=srrip_eval
#SBATCH --account=local
#SBATCH --partition=COMPUTE
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=100M
#SBATCH --array=0-{len(commands) - 1}
#SBATCH --output=/dev/null
#SBATCH --error=/dev/null

set cmds = ( {tcsh_command_array} )
@ idx = $SLURM_ARRAY_TASK_ID + 1
set cmd = "$cmds[$idx]"
eval $cmd
"""

# === Write and submit the script ===
with open("submit_inline.tcsh", "w") as f:
    f.write(slurm_script)

# subprocess.run(["sbatch", "submit_inline.tcsh"])


