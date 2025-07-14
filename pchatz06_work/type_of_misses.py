import os
import re
import time
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import sys
import math
import pickle
import pprint
import argparse

def createFolder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")

def main():
    parser = argparse.ArgumentParser(description="Plot graphs from data directories.")

    parser.add_argument("-global", dest="global_path", type=str, help="Path to global results")
    parser.add_argument("-local", dest="local_path", type=str, help="Path to local results")


    args = parser.parse_args()

    FLAG_GLOBAL = False
    FLAG_LOCAL = False

    DIR_GLOBAL = ""
    DIR_LOCAL = ""
    GENERATIONS = 50

    if args.global_path:
        FLAG_GLOBAL = True
        DIR_GLOBAL = args.global_path
    else:
        print("No global path provided")

    if args.local_path:
        FLAG_LOCAL = True
        DIR_LOCAL = args.local_path
    else:
        print("No local path provided")



    baseline_ipc = {
        "Blender": 0.661, "Bwaves": 1.016, "Cam4": 0.725, "cactuBSSN": 0.761,
        "Exchange": 1.127, "Gcc": 0.353, "Lbm": 0.652, "Mcf": 0.400,
        "Parest": 0.935, "Povray": 0.356, "Wrf": 0.823, "Xalancbmk": 0.395,
        "Fotonik3d": 0.621, "Imagick": 2.193, "Leela": 0.548, "Omnetpp": 0.246,
        "Perlbench": 0.448, "Roms": 1.079, "x264": 1.372, "Xz": 0.894
    }


    if FLAG_LOCAL:
        RESULTS_DIR = DIR_LOCAL
        SUFFIX = RESULTS_DIR.split("/")[-1]
        for benchmark, base_ipc in baseline_ipc.items():
            BENCH_PATH = "/" + str(benchmark)
            BENCH_RES_DIR = RESULTS_DIR + BENCH_PATH + "/Results/"

            individual_ids = []
            ipc_results = []

            llc_total_misses = []
            llc_load_misses = []
            llc_rfo_misses = []
            llc_prefetch_misses = []
            llc_writeback_misses = []
            for target_generation in range(1, GENERATIONS + 1):
                pattern = re.compile(r"-" + re.escape(str(target_generation)) + r"-(\d+)$")

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
                                            
                                        if "LLC TOTAL ACCESSES:" in line:
                                            parts = line.strip().split()
                                            try:
                                                total_misses = int(parts[7])
                                                llc_total_misses.append((individual_id, total_misses))
                                            except ValueError:
                                                print(f"Could not parse TOTAL MISSES value in {filepath}")
                                            
                                        if "LLC LOAD ACCESSES:" in line:
                                            parts = line.strip().split()
                                            try:
                                                load_misses = int(parts[7])
                                                llc_load_misses.append((individual_id, load_misses))
                                            except ValueError:
                                                print(f"Could not parse LOAD MISSES value in {filepath}")
                                            
                                        if "LLC RFO ACCESSES:" in line:
                                            parts = line.strip().split()
                                            try:
                                                rfo_misses = int(parts[7])
                                                llc_rfo_misses.append((individual_id, rfo_misses))
                                            except ValueError:
                                                print(f"Could not parse RFO MISSES value in {filepath}")
                                            
                                        if "LLC PREFETCH ACCESSES:" in line:
                                            parts = line.strip().split()
                                            try:
                                                prefetch_misses = int(parts[7])
                                                llc_prefetch_misses.append((individual_id, prefetch_misses))
                                            except ValueError:
                                                print(f"Could not parse PREFETCH MISSES value in {filepath}")
                                            
                                        if "LLC WRITEBACK ACCESSES:" in line:
                                            parts = line.strip().split()
                                            try:
                                                writeback_misses = int(parts[7])
                                                llc_writeback_misses.append((individual_id, writeback_misses))
                                            except ValueError:
                                                print(f"Could not parse WRITEBACK MISSES value in {filepath}")
                                            break
                            except Exception as e:
                                continue
                                #print(f"Error reading {filepath}: {e}")


            def normalize(lst):
                min_val = min(lst)
                max_val = max(lst)
                if max_val == min_val:
                    return [0.0] * len(lst)  # Avoid division by zero
                return [(x - min_val) / (max_val - min_val) for x in lst]

            def compute_correlation(xs, ys):
                n = len(xs)
                mean_x = sum(xs) / n
                mean_y = sum(ys) / n

                numerator = sum((x - mean_x)*(y - mean_y) for x, y in zip(xs, ys))
                denom_x = math.sqrt(sum((x - mean_x)**2 for x in xs))
                denom_y = math.sqrt(sum((y - mean_y)**2 for y in ys))

                if denom_x == 0 or denom_y == 0:
                    return 0.0  # avoid division by zero

                return numerator / (denom_x * denom_y)

            # Normalize all miss lists
            ipc_results = [x[1] for x in ipc_results]
            llc_total_misses = [x[1] for x in llc_total_misses]
            llc_load_misses = [x[1] for x in llc_load_misses]
            llc_rfo_misses = [x[1] for x in llc_rfo_misses]
            llc_prefetch_misses = [x[1] for x in llc_prefetch_misses]
            llc_writeback_misses = [x[1] for x in llc_writeback_misses]

            # llc_total_misses_norm = normalize(llc_total_misses)
            # llc_load_misses_norm = normalize(llc_load_misses)
            # llc_rfo_misses_norm = normalize(llc_rfo_misses)
            # llc_prefetch_misses_norm = normalize(llc_prefetch_misses)
            # llc_writeback_misses_norm = normalize(llc_writeback_misses)

            miss_lists = [
                ("Total Misses", llc_total_misses),
                ("Load Misses", llc_load_misses),
                ("RFO Misses", llc_rfo_misses),
                ("Prefetch Misses", llc_prefetch_misses),
                ("Writeback Misses", llc_writeback_misses)
            ]

            # miss_lists = [
            #     ("Total Misses", llc_total_misses_norm),
            #     ("Load Misses", llc_load_misses_norm),
            #     ("RFO Misses", llc_rfo_misses_norm),
            #     ("Prefetch Misses", llc_prefetch_misses_norm),
            #     ("Writeback Misses", llc_writeback_misses_norm)
            # ]


            fig, axs = plt.subplots(1, 5, figsize=(20, 4))
            fig.suptitle("IPC vs. LLC Miss Types")
            for i, (title, misses) in enumerate(miss_lists):
                x = misses
                y = ipc_results
                axs[i].scatter(misses, ipc_results)
                
                axs[i].set_xlabel("Misses")
                axs[i].tick_params(axis='x', rotation=25)
                axs[i].grid(True)
                # axs[i].set_ylim([0.5, 1.5])
                r = compute_correlation(x, y)
                axs[i].set_title(f"{title}, LC={r:.4f}, DP:{len(misses)}")
                #axs[i].text(0.5, -0.45, f"Linear_Correlation = {r:.2f}", transform=axs[i].transAxes, ha='center', fontsize=10)
                if i == 0:
                    axs[i].set_ylabel("IPC")
            

            plt.suptitle("IPC vs. Different LLC Miss Types")
            plt.tight_layout()



            folder_name = f"GRAPHS/Misses_Comparisson/{SUFFIX}"
            createFolder(folder_name)
            plt.savefig(f"GRAPHS/Misses_Comparisson/{SUFFIX}/{benchmark}.png")
            plt.close()
    
    if FLAG_GLOBAL:
        RESULTS_DIR = DIR_GLOBAL
        SUFFIX = RESULTS_DIR.split("/")[-1]
        
        for benchmark, base_ipc in baseline_ipc.items():
            BENCH_RES_DIR = RESULTS_DIR + "/Results/"

            individual_ids = []
            ipc_results = []

            llc_total_misses = []
            llc_load_misses = []
            llc_rfo_misses = []
            llc_prefetch_misses = []
            llc_writeback_misses = []
            for target_generation in range(1, GENERATIONS + 1):
                pattern = re.compile(r"-" + re.escape(str(target_generation)) + r"-(\d+)$")

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
                                            
                                        if "LLC TOTAL ACCESSES:" in line:
                                            parts = line.strip().split()
                                            try:
                                                total_misses = int(parts[7])
                                                llc_total_misses.append((individual_id, total_misses))
                                            except ValueError:
                                                print(f"Could not parse TOTAL MISSES value in {filepath}")
                                            
                                        if "LLC LOAD ACCESSES:" in line:
                                            parts = line.strip().split()
                                            try:
                                                load_misses = int(parts[7])
                                                llc_load_misses.append((individual_id, load_misses))
                                            except ValueError:
                                                print(f"Could not parse LOAD MISSES value in {filepath}")
                                            
                                        if "LLC RFO ACCESSES:" in line:
                                            parts = line.strip().split()
                                            try:
                                                rfo_misses = int(parts[7])
                                                llc_rfo_misses.append((individual_id, rfo_misses))
                                            except ValueError:
                                                print(f"Could not parse RFO MISSES value in {filepath}")
                                            
                                        if "LLC PREFETCH ACCESSES:" in line:
                                            parts = line.strip().split()
                                            try:
                                                prefetch_misses = int(parts[7])
                                                llc_prefetch_misses.append((individual_id, prefetch_misses))
                                            except ValueError:
                                                print(f"Could not parse PREFETCH MISSES value in {filepath}")
                                            
                                        if "LLC WRITEBACK ACCESSES:" in line:
                                            parts = line.strip().split()
                                            try:
                                                writeback_misses = int(parts[7])
                                                llc_writeback_misses.append((individual_id, writeback_misses))
                                            except ValueError:
                                                print(f"Could not parse WRITEBACK MISSES value in {filepath}")
                                            break
                            except Exception as e:
                                continue
                                #print(f"Error reading {filepath}: {e}")


            def normalize(lst):
                min_val = min(lst)
                max_val = max(lst)
                if max_val == min_val:
                    return [0.0] * len(lst)  # Avoid division by zero
                return [(x - min_val) / (max_val - min_val) for x in lst]

            def compute_correlation(xs, ys):
                n = len(xs)
                mean_x = sum(xs) / n
                mean_y = sum(ys) / n

                numerator = sum((x - mean_x)*(y - mean_y) for x, y in zip(xs, ys))
                denom_x = math.sqrt(sum((x - mean_x)**2 for x in xs))
                denom_y = math.sqrt(sum((y - mean_y)**2 for y in ys))

                if denom_x == 0 or denom_y == 0:
                    return 0.0  # avoid division by zero

                return numerator / (denom_x * denom_y)

            # Normalize all miss lists
            ipc_results = [x[1] for x in ipc_results]
            llc_total_misses = [x[1] for x in llc_total_misses]
            llc_load_misses = [x[1] for x in llc_load_misses]
            llc_rfo_misses = [x[1] for x in llc_rfo_misses]
            llc_prefetch_misses = [x[1] for x in llc_prefetch_misses]
            llc_writeback_misses = [x[1] for x in llc_writeback_misses]

            # llc_total_misses_norm = normalize(llc_total_misses)
            # llc_load_misses_norm = normalize(llc_load_misses)
            # llc_rfo_misses_norm = normalize(llc_rfo_misses)
            # llc_prefetch_misses_norm = normalize(llc_prefetch_misses)
            # llc_writeback_misses_norm = normalize(llc_writeback_misses)

            miss_lists = [
                ("Total Misses", llc_total_misses),
                ("Load Misses", llc_load_misses),
                ("RFO Misses", llc_rfo_misses),
                ("Prefetch Misses", llc_prefetch_misses),
                ("Writeback Misses", llc_writeback_misses)
            ]

            # miss_lists = [
            #     ("Total Misses", llc_total_misses_norm),
            #     ("Load Misses", llc_load_misses_norm),
            #     ("RFO Misses", llc_rfo_misses_norm),
            #     ("Prefetch Misses", llc_prefetch_misses_norm),
            #     ("Writeback Misses", llc_writeback_misses_norm)
            # ]


            fig, axs = plt.subplots(1, 5, figsize=(20, 4))
            fig.suptitle("IPC vs. LLC Miss Types")
            for i, (title, misses) in enumerate(miss_lists):
                x = misses
                y = ipc_results
                axs[i].scatter(misses, ipc_results)
                
                axs[i].set_xlabel("Misses")
                axs[i].tick_params(axis='x', rotation=25)
                axs[i].grid(True)
                # axs[i].set_ylim([0.5, 1.5])
                r = compute_correlation(x, y)
                axs[i].set_title(f"{title}, LC={r:.4f}, DP:{len(misses)}")
                #axs[i].text(0.5, -0.45, f"Linear_Correlation = {r:.2f}", transform=axs[i].transAxes, ha='center', fontsize=10)
                if i == 0:
                    axs[i].set_ylabel("IPC")
            

            plt.suptitle("IPC vs. Different LLC Miss Types")
            plt.tight_layout()



            folder_name = f"GRAPHS/Misses_Comparisson/{SUFFIX}"
            createFolder(folder_name)
            plt.savefig(f"GRAPHS/Misses_Comparisson/{SUFFIX}/{benchmark}.png")
            plt.close()


if __name__ == "__main__":
    main()