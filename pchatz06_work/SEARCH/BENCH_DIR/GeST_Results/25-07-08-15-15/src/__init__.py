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
import Instruction
import Operand
from random import Random
from Algorithm import Algorithm
from Individual import Individual
import sys
import os

print(os.getcwd())

configurationFile = "../configurationFiles/configuration_RRIP.xml"

suffix = sys.argv[1]
bench_list = sys.argv[2]

rand = Random(42)  # to use a fixed seed give an int argument

algorithm = Algorithm(configurationFile, suffix, bench_list, rand)
algorithm.createInitialPopulation()
algorithm.measureGeneration()

while algorithm.areWeDone() != True:
    algorithm.evolvePopulation()
    algorithm.measureGeneration()

fittest = algorithm.getFittest();
print("Fittest individual is:\n " + fittest.__str__() + "with measurement equal to " + str(fittest.getMeasurements()));
