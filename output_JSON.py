import json
import csv
import numpy as np

with open('topic_output_100_newer.txt', 'rb') as topics_file:
    topic_list = map(lambda s : s.replace('\n','').replace('\r',''), list(topics_file)[1:101])
fix_str = lambda s : s.replace('u\'','').replace('\'','').replace('[','').replace(']','').replace(',','')
word_lists = map(lambda lst : map(fix_str, lst.split(' ')[1:]), topic_list)

with open('clusters_100_newer_analysis.csv', 'rb') as clusters_file:
    reader = csv.reader(clusters_file)
    counts_data = [line for line in reader]
    years = map(int, counts_data[0])
    counts_data = np.array(map(lambda row : map(lambda x : int(np.round(float(x))), row), counts_data[1:]))
    counts_data = np.array(map(lambda row : dict(zip(years, row), total = sum(row)), counts_data))
    #print counts_data[0]
with open('clusters_100_newer_dissent_analysis.csv', 'rb') as clusters_file:
    reader = csv.reader(clusters_file)
    dissents_data = [line for line in reader]
    dissents_years = map(int, dissents_data[0])
    dissents_data = np.array(map(lambda row : map(lambda x : int(np.round(float(x))), row), dissents_data[1:]))
    dissents_data = np.array(map(lambda row : dict(zip(dissents_years, row), total = sum(row)), dissents_data))
    for year in years:
        if year not in dissents_years:
            for c in range(100):
                dissents_data[c][year] = 0
    #print dissents_data[0]
with open('clusters_100_newer_SC_analysis.csv', 'rb') as clusters_file:
    reader = csv.reader(clusters_file)
    SC_data = [line for line in reader]
    SC_years = map(int, SC_data[0])
    SC_data = np.array(map(lambda row : map(lambda x : int(np.round(float(x))), row), SC_data[1:]))
    SC_data = np.array(map(lambda row : dict(zip(SC_years, row), total = sum(row)), SC_data))
    for year in years:
        if year not in SC_years:
            for c in range(100):
                SC_data[c][year] = 0
    #print SC_data[0]
with open('clusters_100_newer_SC_dissent_analysis.csv', 'rb') as clusters_file:
    reader = csv.reader(clusters_file)
    SC_dissent_data = [line for line in reader]
    SC_dissent_years = map(int, SC_dissent_data[0])
    SC_dissent_data = np.array(map(lambda row : map(lambda x : int(np.round(float(x))), row), SC_dissent_data[1:]))
    SC_dissent_data = np.array(map(lambda row : dict(zip(SC_dissent_years, row), total = sum(row)), SC_dissent_data))
    for year in years:
        if year not in SC_dissent_years:
            for c in range(100):
                SC_dissent_data[c][year] = 0
    #print SC_dissent_data[0]
all_data = zip(range(100), word_lists, counts_data, dissents_data, SC_data, SC_dissent_data)
keys = ('cluster_id', 'cluster_words', 'case_counts', 'dissent_counts', 'SC_counts', 'SC_dissent_counts')
dicts = map(lambda tup : dict(zip(keys, tup)), all_data)
#dicts = map(lambda tup : dict(cluster_id = tup[0], cluster_words = tup[1], case_counts = tup[2],
#                              dissent_counts = tup[3], SC_counts = tup[4], SC_dissent_counts = tup[5]), all_data)
output_dict = dict(zip(map(str, range(100)), dicts))
#print json.dumps(output_dict)
json.dump(output_dict, open('output.json', 'w'))