import re
import subprocess
import sys
import os
from time import sleep
from datetime import datetime



if len(sys.argv) != 4:
    print("Usage: python3 run_srrip.py policy_file benchmark_file output_name")
    print("Error: Incorrect number of arguments provided...")
    sys.exit(1)

policy = sys.argv[1]
bench_list = sys.argv[2]
name = sys.argv[3]

root_dir = "../Run_workloads_with_policy/" 
#after_dir = f"SRRIP_BEST_PERSONAL_{bench_list}"
# after_dir = "SRRIP_BEST_GLOBAL_VALIDATION"
after_dir = f"{name}"
# Change working directory to the script's directory
script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(script_dir)
os.makedirs(f"../Run_workloads_with_policy/{after_dir}/", exist_ok=True)
error = open(f"../Run_workloads_with_policy/{after_dir}/error.out", 'a')

# Create a bash file
sbatch = open(f"../Run_workloads_with_policy/{after_dir}/batch" + ".sh", 'w')




values = {}
section_found = False

# Open the individual file
with open(f"{policy}", 'r') as file:
    for line in file:
        # Get the number from each line
        if line.startswith('\t'):
            # extract number at the end of the line
            text = line.strip().split()[-1]
            key = line.split()[0]
            number = re.search(r"\d+", text).group()
            values[key] = number

# Using the dictionary create the plist
plist_keys = ["W_SPromClean", "W_Insert", "P_SPromClean", "P_Insert", "R_SPromClean", "R_Insert", "L_SPromClean", "L_Insert"]
plist = ""

for key in plist_keys:
    if key in values.keys():
        plist += values.get(key)
    else:
        plist += "0"
        error.write("A value for " + key + " was not found and the default 0 was used instead")


# Using the dictionary create the dirty_plist
dirty_plist_keys = ["W_SPromDirty", "W_Insert", "P_SPromDirty", "P_Insert", "R_SPromDirty", "R_Insert", "L_SPromDirty", "L_Insert"]
dirty_plist = ""

for key in dirty_plist_keys:
    if key in values.keys():
        dirty_plist += values.get(key)
    else:
        dirty_plist += "0"
        error.write("A value for " + key + " was not found and the default 0 was used instead")


# Using the dictionary create the demmask
demmask_keys = ["W_DemDirty", "W_DemClean", "P_DemDirty", "P_DemClean", "R_DemDirty", "R_DemClean", "L_DemDirty", "L_DemClean"]
demmask = ""

for key in demmask_keys:
    if key in values.keys():
        demmask += values.get(key)
    else:
        demmask += "0"
        error.write("A value for " + key + " was not found and the default 0 was used instead")

with open(bench_list, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

num_benchmarks = len(lines)
colon_separated = ":".join(lines)

with open(f"../Run_workloads_with_policy/{after_dir}/benchmarks.txt", 'w') as bfile:
    bfile.write(colon_separated)


batch_script = "RRIP_BATCH_RUN"
switch_script = "RRIP_RUN"
myID = 1 
batch_command = (
    f"sbatch --array=1-{num_benchmarks} "
    f"--output=/dev/null --error=/dev/null "
    f"--export=ALL,script={switch_script},"
    f"plist={plist}{plist},"
    f"dplist={dirty_plist}{dirty_plist},"
    f"demmask={demmask}{demmask},"
    f"id='{myID}-{num_benchmarks}',"
    f"root_dir={root_dir},"
    f"after_dir={after_dir} "
    f"{batch_script}\n"
)

# Write the command to the batch file we created 
sbatch.write(batch_command)

# Close the batch file
sbatch.close()

# Write in the error.out file the time the simumation/s have started, make the batch file executable and then run it
error.write("Simulations " + "started at " + datetime.now().strftime("%H:%M:%S") + "\n")
subprocess.call("chmod u+x " + f"../Run_workloads_with_policy/{after_dir}/batch" + ".sh", shell=True)
subprocess.call(f"../Run_workloads_with_policy/{after_dir}/batch" + ".sh", shell=True)

# Close the error file
error.close()
