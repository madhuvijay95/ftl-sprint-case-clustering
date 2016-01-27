import sys
import numpy as np

threshold = float(sys.argv[2])
with open(sys.argv[1], 'rb') as input_file:
    for line in input_file:
        if np.random.random() < threshold:
            print line.replace('\n','')