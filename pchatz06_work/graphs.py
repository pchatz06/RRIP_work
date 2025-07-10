import os
import re
import time
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import sys

import pickle
import pprint;

sys.path.append(os.path.abspath("SEARCH/GeST/src"))

from Population import Population
from Individual import Individual
from Instruction import Instruction
from Operand import Operand

RESULTS_DIR = sys.argv[1]
SUFFIX = sys.argv[2]

# RESULTS_DIR = "/home/pchatz06/RRIP_work/pchatz06_work/SEARCH/BENCH_DIR/"
GENERATIONS = 100
# SUFFIX = "10-13-27-M5-Onepoint"

plot_all_individuals = True
plot_best_individuals = True
plot_99_percentile_individuals = True
plot_all_graph = True

baseline_ipc = {
    "Blender": 0.661, "Bwaves": 1.016, "Cam4": 0.725, "cactuBSSN": 0.761,
    "Exchange": 1.127, "Gcc": 0.353, "Lbm": 0.652, "Mcf": 0.400,
    "Parest": 0.935, "Povray": 0.356, "Wrf": 0.823, "Xalancbmk": 0.395,
    "Fotonik3d": 0.621, "Imagick": 2.193, "Leela": 0.548, "Omnetpp": 0.246,
    "Perlbench": 0.448, "Roms": 1.079, "x264": 1.372, "Xz": 0.894
}



def createFolder(name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")

def createPlots(speed_up_best_of_each_gen, speed_up_all_indivs, speed_up_99_percentile_individuals, benchmark, s_type):
    if plot_best_individuals:
        plt.plot(speed_up_best_of_each_gen, marker='o')
        plt.title("Speedup over Generations")
        plt.xlabel("Generation Index")
        plt.ylabel("Speedup Value")

        # Use plain style and no offset on y-axis
        plt.ticklabel_format(style='plain', axis='y')
        plt.gca().yaxis.get_major_formatter().set_useOffset(False)

        # Force x-axis to show integers, step of 1
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
        plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"GRAPHS/{SUFFIX}/{s_type}/Best_Individual_Of_Each_Generation/speed_up_per_gen_{benchmark}.png")
        plt.close()

    if plot_all_individuals:
        y_values = [point[0] for point in speed_up_all_indivs]
        x_values = [point[1] for point in speed_up_all_indivs]

        plt.plot(x_values, y_values, marker='o', linestyle='None')

        plt.title("Speedup over Generations")
        plt.xlabel("Generation Index")
        plt.ylabel("Speedup Value")

        # Y-axis formatting
        plt.ticklabel_format(style='plain', axis='y')
        plt.gca().yaxis.get_major_formatter().set_useOffset(False)

        # X-axis: integers spaced by 1
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
        plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"GRAPHS/{SUFFIX}/{s_type}/All_Individuals_Of_Each_Generation/speed_up_per_gen_{benchmark}.png")
        plt.close()

    if plot_99_percentile_individuals:
        y_values = [point[0] for point in speed_up_99_percentile_individuals]
        x_values = [point[1] for point in speed_up_99_percentile_individuals]

        plt.plot(x_values, y_values, marker='o', linestyle='None')

        plt.title("Speedup over Generations")
        plt.xlabel("Generation Index")
        plt.ylabel("Speedup Value")

        # Y-axis formatting
        plt.ticklabel_format(style='plain', axis='y')
        plt.gca().yaxis.get_major_formatter().set_useOffset(False)

        # X-axis: integers spaced by 1
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
        plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"GRAPHS/{SUFFIX}/{s_type}/99th_Percentile_Individuals_Of_Each_Generation/speed_up_per_gen_{benchmark}.png")
        plt.close()






speed_up_per_workload_of_best_global_policy = []
speed_up_per_workload_of_personal_best_global_policy = []
speed_up_per_workload_of_local_global_policy = []

folder_name = f"GRAPHS/{SUFFIX}/global/Best_Individual_Of_Each_Generation"
createFolder(folder_name)
folder_name = f"GRAPHS/{SUFFIX}/local/Best_Individual_Of_Each_Generation"
createFolder(folder_name)
folder_name = f"GRAPHS/{SUFFIX}/global/All_Individuals_Of_Each_Generation"
createFolder(folder_name)
folder_name = f"GRAPHS/{SUFFIX}/local/All_Individuals_Of_Each_Generation"
createFolder(folder_name)
folder_name = f"GRAPHS/{SUFFIX}/global/99th_Percentile_Individuals_Of_Each_Generation"
createFolder(folder_name)
folder_name = f"GRAPHS/{SUFFIX}/local/99th_Percentile_Individuals_Of_Each_Generation"
createFolder(folder_name)




BENCH_PATH = SUFFIX +"/global/GeST_Results"
BENCH_RES_DIR = os.path.join(RESULTS_DIR, BENCH_PATH)
BENCH_RES_DIR = BENCH_RES_DIR + "/"
print(BENCH_RES_DIR)
print("-------------")

speed_up_best_of_each_gen = []
speed_up_all_indivs = []
speed_up_99_percentile_individuals = []


files=[]
for root, dirs, filenames in os.walk(BENCH_RES_DIR): #takes as input the dir with the saved state
    for f in filenames:
        if((".pkl" in f) and ("rand" not in f)):
            files.append(f);

files.sort(key=lambda x:  int(x.split('.')[0]));
pop=Population([]);
best_global_avg = -1
generation_counter = 1
for f in files:
    input=open(BENCH_RES_DIR+f,"rb");
    pop=pickle.load(input);
    input.close();
    best=pop.getFittest();
    best_global_avg = best
    speed_up_best_of_each_gen.append(float(best.getFitness()));    
    for indiv in pop.individuals:
        speed_up_all_indivs.append([float(indiv.getFitness()), generation_counter])
    
    generation_counter = generation_counter + 1

threshold = max(speed_up_best_of_each_gen)*0.99

for gen in range(len(speed_up_best_of_each_gen)):
    count = 0
    for y, x in speed_up_all_indivs:
        if x == gen and y > threshold:
            speed_up_99_percentile_individuals.append([y, x])
            count += 1
        if count == 5:
            break

createPlots(speed_up_best_of_each_gen, speed_up_all_indivs, speed_up_99_percentile_individuals, "AVERAGE_SPEED_UP", "global")

for benchmark, base_ipc in baseline_ipc.items():
    BENCH_PATH = SUFFIX + "/global"
    DIR = os.path.join(RESULTS_DIR, BENCH_PATH)
    BENCH_RES_DIR = os.path.join(DIR, "Results/")

    print(BENCH_RES_DIR)
    print("-------------")

    speed_up_best_of_each_gen = []
    speed_up_all_indivs = []
    speed_up_99_percentile_individuals = []

    for target_generation in range(1, GENERATIONS + 1):
        pattern = re.compile(r"-" + re.escape(str(target_generation)) + r"-(\d+)$")
        # Store individual IDs
        individual_ids = []
        ipc_results = []
        

        for filename in os.listdir(BENCH_RES_DIR):
            if filename.startswith("results-"):
                match = pattern.search(filename)
                if match:
                    individual_id = int(match.group(1))
                    filepath = os.path.join(BENCH_RES_DIR, filename)
                    try:
                        with open(f"{filepath}/{benchmark}.out", "r") as file:
                            for line in file:
                                if "CPU 0 cumulative IPC:" in line:
                                    parts = line.strip().split()
                                    try:
                                        ipc_value = float(parts[4])
                                        ipc_results.append((individual_id, ipc_value))
                                    except ValueError:
                                        print(f"Could not parse IPC value in {filepath}")
                                    break
                    except Exception as e:
                        print(f"Error reading {filepath}: {e}")

        
        # Sort results by IPC descending
        # print(ipc_results)
        if ipc_results:
            ipc_results.sort(key=lambda x: x[1], reverse=True)

            # # Print sorted results
            # for ind_id, ipc in ipc_results:
            #     print(f"Individual {ind_id}: {ipc}")
            speed_up_best_of_each_gen.append(float(ipc_results[0][1])/float(base_ipc))

            for i in range(len(ipc_results)):
                speed_up_all_indivs.append([float(ipc_results[i][1])/float(base_ipc), target_generation])
                if ipc_results[i][0] == best_global_avg.myId:
                    if [benchmark, float(ipc_results[i][1])/float(base_ipc)] not in speed_up_per_workload_of_best_global_policy:
                        speed_up_per_workload_of_best_global_policy.append([benchmark, float(ipc_results[i][1])/float(base_ipc)])

    speed_up_per_workload_of_personal_best_global_policy.append([benchmark, max(speed_up_best_of_each_gen)])      
    threshold = max(speed_up_best_of_each_gen)*0.99

    for gen in range(len(speed_up_best_of_each_gen)):
        count = 0
        for y, x in speed_up_all_indivs:
            if x == gen and y > threshold:
                speed_up_99_percentile_individuals.append([y, x])
                count += 1
            if count == 5:
                break

    createPlots(speed_up_best_of_each_gen, speed_up_all_indivs, speed_up_99_percentile_individuals, benchmark, "global")

for benchmark, base_ipc in baseline_ipc.items():
    BENCH_PATH = SUFFIX + "/local_" + str(benchmark)
    DIR = os.path.join(RESULTS_DIR, BENCH_PATH)
    BENCH_RES_DIR = os.path.join(DIR, "Results/")

    print(BENCH_RES_DIR)
    print("-------------")

    speed_up_best_of_each_gen = []
    speed_up_all_indivs = []
    speed_up_99_percentile_individuals = []

    for target_generation in range(1, GENERATIONS + 1):
        pattern = re.compile(r"-" + re.escape(str(target_generation)) + r"-(\d+)$")
        # Store individual IDs
        individual_ids = []
        ipc_results = []
        

        for filename in os.listdir(BENCH_RES_DIR):
            if filename.startswith("results-"):
                match = pattern.search(filename)
                if match:
                    individual_id = int(match.group(1))
                    filepath = os.path.join(BENCH_RES_DIR, filename)
                    try:
                        with open(f"{filepath}/{benchmark}.out", "r") as file:
                            for line in file:
                                if "CPU 0 cumulative IPC:" in line:
                                    parts = line.strip().split()
                                    try:
                                        ipc_value = float(parts[4])
                                        ipc_results.append((individual_id, ipc_value))
                                    except ValueError:
                                        print(f"Could not parse IPC value in {filepath}")
                                    break
                    except Exception as e:
                        print(f"Error reading {filepath}: {e}")

        
        # Sort results by IPC descending
        # print(ipc_results)
        if ipc_results:
            ipc_results.sort(key=lambda x: x[1], reverse=True)

            # # Print sorted results
            # for ind_id, ipc in ipc_results:
            #     print(f"Individual {ind_id}: {ipc}")
            speed_up_best_of_each_gen.append(float(ipc_results[0][1])/float(base_ipc))

            for i in range(len(ipc_results)):
                speed_up_all_indivs.append([float(ipc_results[i][1])/float(base_ipc), target_generation])


    speed_up_per_workload_of_local_global_policy.append([benchmark, max(speed_up_best_of_each_gen)])
    threshold = max(speed_up_best_of_each_gen)*0.99

    for gen in range(len(speed_up_best_of_each_gen)):
        count = 0
        for y, x in speed_up_all_indivs:
            if x == gen and y > threshold:
                speed_up_99_percentile_individuals.append([y, x])
                count += 1
            if count == 5:
                break

    createPlots(speed_up_best_of_each_gen, speed_up_all_indivs, speed_up_99_percentile_individuals, benchmark, "local")


if speed_up_per_workload_of_best_global_policy and speed_up_per_workload_of_personal_best_global_policy and speed_up_per_workload_of_local_global_policy:
    # Extract names and values
    benchmarks = [item[0] for item in speed_up_per_workload_of_best_global_policy]
    values1 = [item[1] for item in speed_up_per_workload_of_best_global_policy]
    values2 = [item[1] for item in speed_up_per_workload_of_personal_best_global_policy]
    values3 = [item[1] for item in speed_up_per_workload_of_local_global_policy]

    # X axis positions
    x = np.arange(len(benchmarks))
    width = 0.25  # width of each bar

    # Create plot
    plt.figure(figsize=(16, 6))
    plt.bar(x - width, values1, width, label='best_global_policy', color='skyblue')
    plt.bar(x,         values2, width, label='personal_best_global_policy', color='orange')
    plt.bar(x + width, values3, width, label='local_best_policy', color='green')

    # Add labels and title
    plt.xlabel('Benchmark')
    plt.ylabel('Speedup')
    plt.title('Comparison of Benchmark Speedups')
    plt.xticks(x, benchmarks, rotation=45, ha='right')
    # plt.ylim(0.950, 1.200)  # Set y-axis limits
    # plt.yticks(np.arange(0.950, 1.201, 0.025))

    plt.ylim(0.800, 1.500)  # Set y-axis limits
    plt.yticks(np.arange(0.800, 1.501, 0.050))
    plt.legend()
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save plot
    plt.savefig(f"GRAPHS/{SUFFIX}/benchmark_comparison.png", dpi=300)
    plt.close()
