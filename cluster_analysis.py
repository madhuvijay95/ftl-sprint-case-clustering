import sys
import numpy as np
import csv
#import itertools

with open(sys.argv[1], 'rb') as input_file:
    reader = csv.reader(input_file)
    data = [dict(file = row[0], year = int(row[1]), cluster = int(row[2])) for row in reader]

n_clusters = max(map(lambda d : d['cluster'], data)) + 1
clusters = range(n_clusters)
years = map(lambda d : d['year'], data)
years = range(min(years), max(years) + 1)
ts = {c : list(np.zeros(len(years))) for c in clusters}
for d in data:
    ts[d['cluster']][d['year'] - min(years)] += 1

with open(sys.argv[2], 'wb') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(tuple(years))
    for c in clusters:
        writer.writerow(tuple(ts[c]))