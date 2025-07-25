'''
Copyright 2019 ARM Ltd. and University of Cyprus
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import os
import sys
import pickle
import pprint;
from Population import Population
from Individual import Individual
from Instruction import Instruction
from Operand import Operand
import re;

spec_benchmarks = [
    "Blender",
    "Bwaves",
    "Cam4",
    "cactuBSSN",
    "Exchange",
    "Gcc",
    "Lbm",
    "Mcf",
    "Parest",
    "Povray",
    "Wrf",
    "Xalancbmk",
    "Fotonik3d",
    "Imagick",
    "Leela",
    "Omnetpp",
    "Perlbench",
    "Roms",
    "x264",
    "Xz"
]
# for benchmark in spec_benchmarks:
path = f"/home/pchatz06/RRIP_work/pchatz06_work/SEARCH/BENCH_DIR/557.xz_r-25-14-45-M5-Onepoint-global/GeST_Results/"
files=[]
for root, dirs, filenames in os.walk(path): #takes as input the dir with the saved state
    for f in filenames:
        if((".pkl" in f) and ("rand" not in f)):
            files.append(f);
# print(files)
files.sort(key=lambda x:  int(x.split('.')[0]));
pop=Population([]);
allValues="";
allKeys="";
columns=[];
theBest=[];
print("best and average of each generation");
print("generation best average");
insHash={};
unique_individuals = set()
counter_gen = 1
best = ""
inst = [[] for _ in range(20)]
for f in files:
    input=open(path+f,"rb");
    pop=pickle.load(input);
    # print(pop)
    input.close();
    # best = pop.getFittest()
    # print(best.getFitness())
    for indiv in pop.individuals:
        #print(indiv.myId, indiv.getFitness(), end = " ")
        print(indiv.getFitness())
    #    print(counter_gen, indiv.getFitness())
        # print(str(indiv))
        # print(indiv.myId)
        # print(indiv.getUniqueKey())
        # print(indiv)
        # if indiv.getUniqueKey() in unique_individuals:
        #     print("HEREHREHREHRHERE")
        #     print(indiv.getUniqueKey())
        unique_individuals.add(indiv.getUniqueKey())
        
        # print(indiv.myId)
        count_ins = 0
        for ins in indiv.sequence:
        #        print(ins.operands[0])
           # inst[count_ins].append(str(ins.operands[0]))
            #print(str(ins.operands[0])[1], end=" ")
            count_ins = count_ins + 1
       # print(inst)
       # print()
    # print(pop.getSize())
    # print("Unique individuals:", len(unique_individuals)) 
    counter_gen = counter_gen + 1  
    #print(pop.getSize()) 
    # print(str(columns[-1])+" "+str(round(float(best.getFitness()),6))+" "+str(round(float(average),6))  );
# with open(f"../../SADRRIP/best_local_plocies/{benchmark}.txt", 'w') as pol:
#     pol.write(str(best))
# for i in range(20):
#    print(inst[i])
print(str(best))
print("end of generation best average");

