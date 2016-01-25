import sys
import time
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import xml.etree.ElementTree as ET
from test_real import body, text_iter, year
from sklearn.decomposition import NMF
import bottleneck as bn
import csv

start_time = time.time()
print 'Time at start: %.3f' % (time.time() - start_time)
sys.stdout.flush()

n_clusters = int(sys.argv[1])
train_filename = sys.argv[2]
test_filename = sys.argv[3] if len(sys.argv) > 3 else train_filename
cluster_output_filename = sys.argv[4] if len(sys.argv) > 4 else None
W_output_filename = sys.argv[5] if len(sys.argv) > 5 else None
H_output_filename = sys.argv[6] if len(sys.argv) > 6 else None

def remove_quotes(filename):
    if filename[0] == '\'' and filename[-1] == '\'':
        return filename[1:(len(filename)-1)]
    else:
        return filename

with open(train_filename, 'rb') as input_file:
    train_case_list = list(input_file)
    train_case_list = map(lambda s : s.replace('\n','').replace('\r',''), train_case_list)
    train_case_list = map(remove_quotes, train_case_list)
print 'Time after reading case list: %.3f' % (time.time() - start_time)
sys.stdout.flush()

def get_text(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return text_iter(body(root)).replace(u'\xad','')

def get_data(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return filename, year(root), text_iter(body(root))

train_texts = map(get_text, train_case_list)
print 'Time after getting train text from XML: %.3f' % (time.time() - start_time)
sys.stdout.flush()

vectorizer = CountVectorizer(max_df = 0.5)
train_mat_init = vectorizer.fit_transform(train_texts)
del train_texts
vocab = vectorizer.vocabulary_
vocab_rev = {v:k for k,v in vocab.items()}
print 'Time after CountVectorizer on train data: %.3f' % (time.time() - start_time)
sys.stdout.flush()

tfidf_fit = TfidfTransformer().fit(train_mat_init)
train_mat = tfidf_fit.transform(train_mat_init)
del train_mat_init
print 'Time after TFIDF on train data: %.3f' % (time.time() - start_time)
sys.stdout.flush()

NMF_fit = NMF(n_components=n_clusters, init='nndsvda').fit(train_mat)
del train_mat
H = NMF_fit.components_
#W = NMF_fit.transform(train_mat)
num_best = 50
best_indices = map(lambda v : list(bn.argpartsort(-v,num_best)[0:num_best]), H)
for i in range(len(best_indices)):
    best_indices[i].sort(key = lambda j : -H[i,j])
best_words = [[vocab_rev[i] for i in lst] for lst in best_indices]

print 'Time after NMF fit: %.3f\n' % (time.time() - start_time)
sys.stdout.flush()

print 'BEST WORDS FOR EACH CLUSTER:'
for c, lst in enumerate(best_words):
    print '%d' % c, lst
print

print '\nTime after NMF output: %.3f' % (time.time() - start_time)
sys.stdout.flush()

with open(test_filename, 'rb') as input_file:
    test_case_list = list(input_file)
    test_case_list = map(lambda s : s.replace('\n','').replace('\r',''), test_case_list)
    test_case_list = map(remove_quotes, test_case_list)
test_data = map(get_data, test_case_list)
test_texts = [t for f,y,t in test_data]
#test_texts = map(get_text, test_case_list)
test_mat_init = vectorizer.transform(test_texts)
del test_texts
test_mat = tfidf_fit.transform(test_mat_init)
del test_mat_init
test_W = NMF_fit.transform(test_mat)
del test_mat
test_clusters = map(np.argmax, test_W)

print 'Time after NMF test transform: %.3f\n' % (time.time() - start_time)

print 'NUMBER OF CASES PER CLUSTER:'
cluster_sizes = [np.sum(np.array(test_clusters) == c) for c in range(n_clusters)]
for c, sz in enumerate(cluster_sizes):
    print '%d: %d' % (c, sz)
print

#print 'NUMBER OF ITERATIONS:', NMF_fit.n_iter_

results = zip(test_clusters, test_data)
results.sort(key = lambda (c, (f,y,t)) : 2000 * c + y) # sort by cluster, then by year
if cluster_output_filename is None:
    print 'CLUSTER ASSIGNMENT FOR EACH CASE:'
    for c, (f,y,t) in results:
        print '%90s' % f, y, c
else:
    with open(cluster_output_filename, 'wb') as output_file:
        writer = csv.writer(output_file)
        for c, (f,y,t) in results:
            writer.writerow((f, y, c))

if W_output_filename is None:
    print
    print test_W
else:
    with open(W_output_filename, 'wb') as output_file:
        writer = csv.writer(output_file)
        for row, (f,y,t) in zip(test_W, test_data):
            writer.writerow((f,) + tuple(row))

if H_output_filename is None:
    print
    print H
else:
    with open(H_output_filename, 'wb') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(tuple([vocab_rev[i].encode('utf-8') for i in range(len(vocab_rev.keys()))]))
        for row in H:
            writer.writerow(tuple(row))

print '\nTime after all remaining output: %.3f\n' % (time.time() - start_time)