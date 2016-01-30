#######################################################################################################################
# Produces JSON output (which includes the number of cases, SC cases, cases with dissents, and SC cases with dissents,
# for each cluster and each year), using cluster assignments from topics.py.
#
# This file takes 4 arguments:
# (1) Name of a file name containing a list of the best words for each cluster, each on a separate line. (This should
#     be the same file that was passed in as argument #5 to topics.py.)
# (2) Name of a csv file containing the cluster assignments for the cases. (This should be the same file that was passed
#     in as argument #4 to topics.py)
# (3) Name of a json file to write the output to.
# (4) (optional) Name of a file containing a list of the file name for every case that has a dissent. This is an
#     optional argument: if this argument is provided, then this file will use the list of dissent cases to determine
#     whether each case has a dissent; if the argument is omitted, then this file will check the text of each case to
#     determine whether it has a disssent. (The latter takes much longer, so providing a file significantly reduces
#     the running time.)
# This file outputs a dictionary of the following form:
#      {"0" : {"cluster-id" : 0, "cluster-words" : [list of words], "case-counts" : {"1850" : 1, "1851" : 2, ...},
#              "dissent-counts" : {"1850" : 0, "1851" : 1, ...}, "SC-counts" : {"1850" : 1, "1851" : 0, ...}},
#       "1" : {"cluster-id" : 1, ...}, ...}
#######################################################################################################################

import json
import csv
import numpy as np
import sys
from helpers import remove_quotes
#import itertools
#from collections import Counter
import copy

best_words_filename = sys.argv[1]
clusters_filename = sys.argv[2]
output_filename = sys.argv[3]
dissents_case_list_filename = sys.argv[4] if len(sys.argv) > 4 else None

if dissents_case_list_filename is not None:
    with open(dissents_case_list_filename, 'rb') as dissents_case_list_file:
        dissents_case_list = list(dissents_case_list_file)
        dissents_case_list = map(lambda s : s.replace('\n','').replace('\r',''), dissents_case_list)
        dissents_case_list = map(remove_quotes, dissents_case_list)
else:
    dissents_case_list = None

def has_dissent(f):
    if dissents_case_list is None:
        return '<opinion type="dissent">' in open(f, 'rb').read()
    else:
        return f in dissents_case_list

def is_SC(f):
    return 'Cal/' in f or 'Cal. 2d' in f or 'Cal. 3d' in f or 'Cal. 4th' in f or 'Cal. Unrep' in f

with open(best_words_filename, 'rb') as topics_file:
    topic_list = map(lambda s : s.replace('\n','').replace('\r',''), list(topics_file)  )
fix_str = lambda s : s.replace('u\'','').replace('\'','').replace('[','').replace(']','').replace(',','')
word_lists = map(lambda lst : map(fix_str, lst.split(' ')[1:]), topic_list)

with open(clusters_filename, 'rb') as cluster_file:
    reader = csv.reader(cluster_file)
    cluster_data = [(f, int(y), int(t)) for f,y,t in reader]
cluster_data_SC = filter(lambda (f,y,t) : is_SC(f), cluster_data)
cluster_data_dissent = filter(lambda (f,y,t) : has_dissent(f), cluster_data)
cluster_data_SC_dissent = filter(lambda (f,y,t) : is_SC(f), cluster_data_dissent)
n_clusters = max(map(lambda (f,y,t) : t, cluster_data)) + 1
years_list = map(lambda (f,y,t) : y, cluster_data)
years = range(min(years_list), max(years_list) + 1)
#print 'done reading'
#sys.stdout.flush()

keys = ('cluster_id', 'cluster_words', 'case_counts', 'dissent_counts', 'SC_counts', 'SC_dissent_counts')
baseline = dict(zip(years, map(int, np.zeros(len(years)))))
dicts = {c : dict(zip(keys, (c, word_lists[c], copy.deepcopy(baseline), copy.deepcopy(baseline), copy.deepcopy(baseline), copy.deepcopy(baseline)))) for c in range(n_clusters)}
#print 'done with baseline'
#sys.stdout.flush()





#case_counts_dict = dict(Counter(map(lambda (f,y,c) : (c,y), cluster_data)))
#for c in range(n_clusters):
#    for y in dicts[c]['case_counts'].keys():
#        if (c,y) in case_counts_dict:
#            dicts[c]['case_counts'][y] = case_counts_dict[(c,y)]
#            #print (c,y,dicts[0]['case_counts'][1950])
#print 'done'

#dicts[0]['case_counts'][1950]
#d1['0']['case_counts']['1950']








#baseline_new = zip(itertools.product(years, range(n_clusters)), np.zeros(len(list(itertools.product(years, range(n_clusters))))))
#reduce(lambda old, (f,y,t) : [(tup,ct) for tup,ct in old if tup != (y,t)] + [((y,t), filter(lambda (tup,ct) : tup == (y,t), old)[0][1])], cluster_data, baseline_new)

#case_counts_data = [((y,c), len(filter(lambda (f,y2,c2) : y2 == y and c2 == c, cluster_data))) for y,c in itertools.product(years, range(n_clusters))]



#for f,y,t in cluster_data:
for n, (f,y,t) in enumerate(cluster_data):
    #print t
    old = dicts[24]['case_counts'][2009]#sum(dicts[24]['case_counts'].values())
    dicts[t]['case_counts'][y] = dicts[t]['case_counts'][y] + 1
    #print old, dicts[24]['case_counts'][2009]
    if has_dissent(f):
        dicts[t]['dissent_counts'][y] += 1
        if is_SC(f):
            dicts[t]['SC_dissent_counts'][y] += 1
            dicts[t]['SC_counts'][y] += 1
    elif is_SC(f):
        dicts[t]['SC_counts'][y] += 1
    #print old, sum(dicts[24]['case_counts'].values())
    #if n % 100 == 0:
    #    print n, dicts[24]['case_counts'][2009]
    #    sys.stdout.flush()
#print 'done iterating'
#sys.stdout.flush()
for c in range(n_clusters):
    for key in ['case_counts', 'dissent_counts', 'SC_counts', 'SC_dissent_counts']:
        dicts[c][key]['total'] = sum(dicts[c][key].values())
#print 'done totaling'
#sys.stdout.flush()

json.dump(dicts, open(output_filename, 'w'))