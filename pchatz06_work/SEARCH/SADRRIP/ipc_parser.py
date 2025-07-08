import os
import re
import sys


generation = sys.argv[1]
myID = sys.argv[2]
suffix = sys.argv[3]
bench_list = sys.argv[4]

Benchmarks = bench_list.split(":")

ipc_values = []

lru_baseline = {
"Blender": 0.661,
"Bwaves": 1.016,
"Cam4": 0.725,
"cactuBSSN": 0.761,
"Exchange": 1.127,
"Gcc": 0.353,
"Lbm": 0.652,
"Mcf": 0.400,
"Parest": 0.935,
"Povray": 0.356,
"Wrf": 0.823,
"Xalancbmk": 0.395,
"Fotonik3d": 0.621,
"Imagick": 2.193,
"Leela": 0.548,
"Omnetpp": 0.246,
"Perlbench": 0.448,
"Roms": 1.079,
"x264": 1.372,
"Xz": 0.894
}



# Get a list of all files in the directory
folder_list = os.listdir(f'../BENCH_DIR/{str(suffix)}/Results')

# Get the folder that has the unique id generation-myID at the end of the name
folder_list = [folder for folder in folder_list if folder.endswith("-" + generation + "-" + myID)]

# Extract the folder name from the list
folder = folder_list[0]


for benchmark in Benchmarks:

    full_filename = f"../BENCH_DIR/{str(suffix)}/Results/" + folder + "/" + benchmark + ".out"
#    print(full_filename)
    # Check if file exists
    if not os.path.isfile(full_filename):
        continue
    
    # Open the file and search fo the comulative IPC at the Finished CPU 
    with open(full_filename, 'r') as f:
        for line in f:
            if "Finished CPU" in line and "IPC:" in line:
                ipc_index = line.find("IPC:") + 5  # find index of IPC value
                ipc_value = float(line[ipc_index:].split()[0])  # extract IPC value as float
                lru_time = float(lru_baseline[benchmark])
                speedup = float(ipc_value/lru_time)
                ipc_values.append(speedup)  # add speedup value to list
#                print(f'LRU : {lru_time} IPC : {ipc_value} BENCHMARK : {benchmark} SPEEDUP: {speedup}')
#                print("BOSS")
                break


if ipc_values:
    avg_ipc = sum(ipc_values) / len(Benchmarks)
    print("{:.5f}".format(avg_ipc))
else:
    print("0")
