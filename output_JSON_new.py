import json
import csv
import numpy as np
import sys
from helpers import remove_quotes

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
#cluster_data_SC = filter(lambda (f,y,t) : is_SC(f), cluster_data)
#cluster_data_dissent = filter(lambda (f,y,t) : has_dissent(f), cluster_data)
#cluster_data_SC_dissent = filter(lambda (f,y,t) : is_SC(f), cluster_data_dissent)
n_clusters = max(map(lambda (f,y,t) : t, cluster_data)) + 1
years_list = map(lambda (f,y,t) : y, cluster_data)
years = range(min(years_list), max(years_list) + 1)
print 'done reading'
sys.stdout.flush()

keys = ('cluster_id', 'cluster_words', 'case_counts', 'dissent_counts', 'SC_counts', 'SC_dissent_counts')
baseline = dict(zip(years, np.zeros(len(years))))
dicts = {c : dict(zip(keys, (c, word_lists[c], baseline, baseline, baseline, baseline))) for c in range(n_clusters)}
print 'done with baseline'
sys.stdout.flush()

#for f,y,t in cluster_data:
for n, (f,y,t) in zip(range(len(cluster_data)), cluster_data):
    dicts[t]['case_counts'][y] += 1
    if has_dissent(f):
        dicts[t]['dissent_counts'][y] += 1
        if is_SC(f):
            dicts[t]['SC_dissent_counts'][y] += 1
            dicts[t]['SC_counts'][y] += 1
    elif is_SC(f):
        dicts[t]['SC_counts'][y] += 1
    if n % 1000 == 0:
        print n
        #print dicts
        sys.stdout.flush()
print 'done iterating'
sys.stdout.flush()
for c in range(n_clusters):
    for key in ['case_counts', 'dissent_counts', 'SC_counts', 'SC_dissent_counts']:
        dicts[c][key]['total'] = sum(dicts[c][key].values())
print 'done totaling'
sys.stdout.flush()

json.dump(dicts, open(output_filename, 'w'))