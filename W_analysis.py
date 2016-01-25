import csv
import sys
#import bottleneck as bn
#import numpy as np

W_file = sys.argv[1]
n_cases = int(sys.argv[2])
cluster_id = int(sys.argv[3]) if len(sys.argv) > 3 else None

with open(W_file, 'rb') as input_file:
    reader = csv.reader(input_file)
    cluster_weights = [row for row in reader]
cluster_weights = map(lambda l : [l[0]] + map(float, l[1:]), cluster_weights)

if cluster_id is not None:
    cluster_weights.sort(key = lambda l : -l[cluster_id + 1])
    #cluster_weights = np.array(cluster_weights)[bn.argpartsort(map(lambda l : -l[cluster_id + 1], cluster_weights), n_cases)]
    clusters_ranked = map(lambda l : l[0], cluster_weights[0:n_cases])
    del cluster_weights
    for case in clusters_ranked:
        print case
else:
    for cluster_id in range(100):
        print 'FOR CLUSTER %d:' % cluster_id
        cluster_weights.sort(key = lambda l : -l[cluster_id + 1])
        #cluster_weights = np.array(cluster_weights)[bn.argpartsort(map(lambda l : -l[cluster_id + 1], cluster_weights), n_cases)]
        clusters_ranked = map(lambda l : l[0], cluster_weights[0:n_cases])
        for case in clusters_ranked:
            print case
        del clusters_ranked
        print