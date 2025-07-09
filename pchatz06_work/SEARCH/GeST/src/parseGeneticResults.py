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


path = "/home/pchatz06/RRIP_work/pchatz06_work/SEARCH/BENCH_DIR/GeST_Results/08-18-21-local_Gcc/" 
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
inst = [[] for _ in range(20)]
for f in files:
    input=open(path+f,"rb");
    pop=pickle.load(input);
    # print(pop)
    input.close();
    columns.append(f.split('.')[0]);
    best=pop.getFittest();
    #print(best)
    theBest.append(best);
    #print(best.getFitness())
    sum=0.0;
    count=0;
    
    for indiv in pop.individuals:
        print(counter_gen, indiv.getMeasurements())
    #    unique_individuals.add(str(indiv))
    #    count_ins = 0
    #    for ins in indiv.sequence:
    #        # print(ins.operands[0])
    #        inst[count_ins].append(str(ins.operands[0]))
    #        count_ins = count_ins + 1

    # print("Unique individuals:", len(unique_individuals)) 
    counter_gen = counter_gen + 1   
    # print(str(columns[-1])+" "+str(round(float(best.getFitness()),6))+" "+str(round(float(average),6))  );
#print (allKeys);
#for i in range(20):
#    print(inst[i])

print("end of generation best average");

