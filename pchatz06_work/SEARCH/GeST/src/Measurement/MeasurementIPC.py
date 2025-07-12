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
import random
from time import sleep
import subprocess
from Measurement.Measurement import Measurement


class MeasurementIPC(Measurement):
    '''
    classdocs
    '''

    def __init__(self, confFile):
        super().__init__(confFile)

    def init(self, root_dir, after_dir, bench_list):
        super().init(root_dir, after_dir)
        self.timeToMeasure = self.tryGetIntValue('time_to_measure')
        self.root_dir = root_dir
        self.after_dir = after_dir
        self.bench_list = bench_list

    def move(self, generation, myID):
        super().moveFile(generation, myID)

    def RunSimulations(self, generation):
        execution_command = "cd ../../SADRRIP ; python3 RunSimFromGeST.py " + str(generation) + " " + str(self.root_dir) + " " + str(self.after_dir) + " " + str(self.bench_list) + f" >> ../BENCH_DIR/{self.root_dir}/{self.after_dir}/trash.txt"
        subprocess.run(execution_command, shell=True)

        sleep(5)
        # print("Checking if job is finshed after 60 min")
        while True:
            output = subprocess.check_output("squeue -u pchatz06 | wc -l", shell=True)
            output = output.decode().replace("\n", "")
            # print(output)
            if output == "1":
                break
            else:
                # print("Jobs not finished there are still " + str(output) + "more jobs")
                sleep(5)

    def GetMeasurement(self, generation, myID):

        output_command = "cd ../../SADRRIP ; python3 ipc_parser.py " + str(generation) + " " + str(myID) + " " + str(self.root_dir) + " " + str(self.after_dir) + " " + str(self.bench_list)
        ipc = subprocess.check_output(output_command, shell=True)
        ipc = ipc.decode().replace("\n", "")
        # print("Average IPC of individuals is " + ipc)

        measurements = [];
        measurements.append(ipc);
        return measurements;


    def measure(self, generation, myID):

        exit("Exiting, something went wrong in Measurement Class!!!")
        