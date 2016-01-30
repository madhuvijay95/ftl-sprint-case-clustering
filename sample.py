#######################################################################################################################
# Inputs are (1) name of a file containing a list of cases and (2) decimal number representing the fraction of cases to
# be sampled.
# Creates a subsample of the cases (in which the proportion of cases showing up in the sample is specified by the second
# argument), and writes the subsample case list to standard output.
# Example: If case_list.txt contains a list of all the cases, then "python sample.py case_list.txt 0.15 > sample.txt"
# will choose a random subsample of roughly 15% of the cases from case_list.txt, and write that subsample to sample.txt.
#######################################################################################################################

import sys
import numpy as np

threshold = float(sys.argv[2])
with open(sys.argv[1], 'rb') as input_file:
    lst = [line.replace('\n','') for line in input_file]
    sample_lst = np.random.choice(lst, size=threshold*len(lst), replace=False)
    for line in sample_lst:
        print line

    #for line in input_file:
    #    if np.random.random() < threshold:
    #        print line.replace('\n','')