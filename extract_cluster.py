import csv
import sys

cluster_filename = sys.argv[1]
cluster_id = sys.argv[2]

with open(cluster_filename, 'rb') as input_file:
    reader = csv.reader(input_file)
    i = 0
    for line in reader:
        if line[2] == cluster_id:
            print line[0]