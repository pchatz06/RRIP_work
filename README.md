*IMPORTANT*

Change the paths in ALL files accordingly, should be good to just remove mzako001 and put your own UCY username.
In some scripts, I write the path with fittest result as Fittest_Results and in some Fittest_Results_MiddleCrossover, because I used both methods and changed midway. Use one path instead of those 2, to create that path with the fittest results, run the file extract_fittest.py

Thesis --> Mcf benchmark only
Others have the benchmark in the path name
Thesis_All is for running all benchmarks and evaluating on average

createMetricsAll.py Creates a clear encoding of each individual and its generation/speedup. Important for some of the scripts

Graph of figure 5.1 

1. Run FirstGraph.py (make sure to run extract_fittest.py and that it saves to Fittest_Results path).


Graph of figure 5.2 (Distribution for each function)

1. Run compare_workload.py. This generates a file names 'similarity.txt' in every path in Fittest_Results.
2. Run plots_similarity.py. This generates some graphs, one of which is the one in figure 5.2.

Matrix of figure 5.3

1. Run findIdenticalPolicies.py, the output will tell you which policies are identical and in which benchmark path.
2. Create a matrix plot (like a confusion matrix) on the results. I got no lines printed on the output, meaning no identical policies and I manually constructed the matrix since the results were obvious to manually create, and for validation I copied a policy from 1 benchmark workload to another with then name copy.txt. I got the following output:

Policy popularity by configuration:
===================================

Thesis_Cam4/Fittest_Results_MiddleCrossover/45_2219_1DOT011650_1DOT011650_2170_2172.txt: appears in 2 Fittest_Results directories
Thesis_Parest/Fittest_Results_MiddleCrossover/copy.txt: appears in 2 Fittest_Results directories


Graph of figure 5.4 (Random vs middle crossover)

1. Run random_vs_middle_crossover.py. Take the output (Should write the best speedup per benchmark for both cases, and put in a simple python plot).


Graph of figure 5.5

1. Run createStrongIndividuals.sh, this creates the path also specified in Algorithm.py (important), and adds 3 files from Fittest_Results directory found inside a benchmark path (like Thesis_Blender). In that path the fittest individuals should be located.

2. Change seedDir in configuration_RRIP.xml to "test". Algorithm.py is configured so it goes to /home/mzako001/Individuals (created from step 1. and take the individuals). Important to also change the population configuration to the number of individuals constructed.

3. Run random_init_vs_fittest_init.py, this tells the highest score found in both runs (Essentially I firstly ran the genetic algo with strong individuals, then randomly and separated the Results according to the time the individual txt files were created).

4. I just put those 2 values printed from step 3 in a quick python program.



Popularity algorithm:

1. Run popularityFittestConfig.py, to run the algorithm. The results on popularity are saved in file popularityFittest_debug_middle.txt
