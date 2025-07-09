import re
import subprocess
import sys
import os
from time import sleep
from datetime import datetime


generation = sys.argv[1]
suffix = sys.argv[2]
bench_list = sys.argv[3]


error = open(f"../BENCH_DIR/{str(suffix)}_error.out", 'a')


# Get a list of all files in the directory
file_list = os.listdir(f'../BENCH_DIR/Individuals/{suffix}')


# Filter the list to include only files that start with "generation_"
file_list = [filename for filename in file_list if filename.startswith(generation + "_")]

# Sort the filenames based on the number after "_"
file_list.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

# Create a bash file
os.makedirs(f"../BENCH_DIR/{str(suffix)}", exist_ok=True)
sbatch = open(f"../BENCH_DIR/{str(suffix)}/Gen_" + str(generation) + ".sh", 'w')




for individual , filename in enumerate(file_list):
    values = {}
    section_found = False

    # Open the individual file
    with open(f"../BENCH_DIR/Individuals/{suffix}/" + filename, 'r') as file:
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


    num_benchmarks = len(bench_list.split(":"))
    with open(f"../BENCH_DIR/{str(suffix)}/benchmarks.txt", 'w') as bfile:
        bfile.write(bench_list)
    
    batch_script = "RRIP_BATCH_RUN"
    switch_script = "RRIP_RUN"
    # Get the ID that GeST gave to the individual
    myID = filename.split("_")[1].split(".")[0]
    # Command that allows us to run the simulations on the cluster
    batch_command = (
        f"sbatch --array=1-{num_benchmarks} "
        f"--output=/dev/null --error=/dev/null "
        f"--export=ALL,script={switch_script},"
        f"plist={plist}{plist},"
        f"dplist={dirty_plist}{dirty_plist},"
        f"demmask={demmask}{demmask},"
        f"id='{generation}-{myID}',"
        f"suffix={suffix} "
        f"{batch_script}\n"
    )

    # Write the command to the batch file we created 
    sbatch.write(batch_command)

# Close the batch file
sbatch.close()

# Write in the error.out file the time the simumation/s have started, make the batch file executable and then run it
error.write("Simulations for generation " + str(generation) + " started at " + datetime.now().strftime("%H:%M:%S") + "\n")
subprocess.call("chmod u+x " + f"../BENCH_DIR/{str(suffix)}/Gen_" + str(generation) + ".sh", shell=True)
subprocess.call(f"../BENCH_DIR/{str(suffix)}/Gen_" + str(generation) + ".sh", shell=True)

# Close the error file
error.close()
