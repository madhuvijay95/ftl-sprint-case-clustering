#######################################################################################################################
# Main file used for topic clustering. Arguments are:
# (1) number of clusters
# (2) name of input file containing a list of cases to train the clustering algorithm on
# (3) name of input file containing a list of cases to apply the clustering algorithm (trained on the cases from #2) to
# (4) name of output file (csv) to write cluster assignments to, each in the form (filename, year, cluster number)
# (5) name of output file to which to write lists of best words for each cluster
# (6) name of output file to which to write lists of best-match cases for each cluster
# (7) name of output file (csv) to write the W matrix (explained below) to; this can help find "best-match" cases later
# (8) name of output file (csv) to write the H matrix (explained below) to; this can help analyze each cluster later
# Note that arguments 3 through 8 are each optional. However, in practice, 3-6 are necessary, though #7-8 can likely be
# omitted unless you want to analyze the NMF output more in greater depth.
#
# Rough explanation: This file uses a non-negative matrix factorization (NMF) algorithm using the prevalence of each
# word in each case, while ignoring words that appear in more than 50% of the data set. The inputs are described above.
# Given a set of n cases that use a vocabulary of K words and have to be placed into c clusters, the output consists of:
# (a) a single unique cluster assignment for each case (which is written into file #4 from above), from 0 to c-1;

# (b)

# (b) an (n x c) matrix W (written into file #5 from above), in which the element at row i and column j represents how
#     well case i fits into cluster j;
# (c) a (c x K) matrix H (written into file #6 from above), in which the element at row i and column j represents how
#     well word j fits into cluster i (note that the 1st row of the output file contains a list of the words in order);
# (d) general output (written to standard output) detailing the 50 "best" words for each cluster as well as the size of
#      cluster in the test data.
#
# Backend explanation of algorithm:
# As stated above, the vocabulary for the algorithm consists of all words that did not
# appear in more than 50% of all of the cases. The data set can then be represented using an (n x K) matrix, where n is
# the number of cases, K is the vocabulary size, and the entry at row i and column j equals the number of times that
# word j shows up in case i.
# However, a problem with that setup is that words that are very common and cases that are very long would have a
# disproportionately large impact on the results. To avoid this a TF-IDF (term frequency - inverse document frequency)
# transformation is used to transform the matrix into one in which very common words are weighted lower and rows are
# scaled to have the same length.
# After this, the NMF clustering algorithm is applied to the new (n x K) matrix M. This algorithm attempts to factor M
# into the product of an (n x c) matrix W and a (c x K) matrix H such that W*H is approximately equal to M.
# Conceptually, each (1 x K) row of H now corresponds to a particular cluster and describes how frequently each word in
# the vocabulary shows up in that cluster. Each (1 x c) row of W corresponds to a case and represents the extent to
# which that case fits into each cluster.
# After the algorithm estimates W and H, we can extract the "best" words for each cluster as follows: Examine the row of
# H corresponding to that cluster, and choose the words whose weights in that row are the highest.
# Now, using the same H matrix from the training process above, the algorithm can cluster any new test case by turning
# it into a (1 x K) row representation t and finding the (1 x c) row vector r such that r*H is approximately equal to t.
# The c elements of r tell us how well the case fits into each of the c clusters, and we can assign r into a cluster by
# choosing the cluster for which the weight is highest.
#######################################################################################################################

import sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import xml.etree.ElementTree as ET
from helpers import body, text_iter, year, remove_quotes
from sklearn.decomposition import NMF
import bottleneck as bn
import csv

#start_time = time.time()
#print 'Time at start: %.3f' % (time.time() - start_time)
#sys.stdout.flush()

n_clusters = int(sys.argv[1])
train_filename = sys.argv[2]
test_filename = sys.argv[3] if len(sys.argv) > 3 else train_filename
cluster_output_filename = sys.argv[4] if len(sys.argv) > 4 else None
best_words_filename = sys.argv[5] if len(sys.argv) > 5 else None
best_match_cases_filename = sys.argv[6] if len(sys.argv) > 6 else None
W_output_filename = sys.argv[7] if len(sys.argv) > 7 else None
H_output_filename = sys.argv[8] if len(sys.argv) > 8 else None

with open(train_filename, 'rb') as input_file:
    train_case_list = list(input_file)
    train_case_list = map(lambda s : s.replace('\n','').replace('\r',''), train_case_list)
    train_case_list = map(remove_quotes, train_case_list)
#print 'Time after reading case list: %.3f' % (time.time() - start_time)
#sys.stdout.flush()

def get_text(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return text_iter(body(root)).replace(u'\xad','')

def get_data(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return filename, year(root), text_iter(body(root))

train_texts = map(get_text, train_case_list)
#print 'Time after getting train text from XML: %.3f' % (time.time() - start_time)
#sys.stdout.flush()

vectorizer = CountVectorizer(max_df = 0.5)
train_mat_init = vectorizer.fit_transform(train_texts)
del train_texts
vocab = vectorizer.vocabulary_
vocab_rev = {v:k for k,v in vocab.items()}
#print 'Time after CountVectorizer on train data: %.3f' % (time.time() - start_time)
#sys.stdout.flush()

tfidf_fit = TfidfTransformer().fit(train_mat_init)
train_mat = tfidf_fit.transform(train_mat_init)
del train_mat_init
#print 'Time after TFIDF on train data: %.3f' % (time.time() - start_time)
#sys.stdout.flush()

NMF_fit = NMF(n_components=n_clusters, init='nndsvda').fit(train_mat)
del train_mat
H = NMF_fit.components_
#W = NMF_fit.transform(train_mat)
num_best = 50
best_indices = map(lambda v : list(bn.argpartsort(-v,num_best)[0:num_best]), H)
for i in range(len(best_indices)):
    best_indices[i].sort(key = lambda j : -H[i,j])
best_words = [[vocab_rev[i] for i in lst] for lst in best_indices]

#print 'Time after NMF fit: %.3f\n' % (time.time() - start_time)
#sys.stdout.flush()

#print 'BEST WORDS FOR EACH CLUSTER:'
#for c, lst in enumerate(best_words):
#    print '%d' % c, lst
#print
if best_words_filename is not None:
    with open(best_words_filename, 'wb') as best_words_file:
        for c, lst in enumerate(best_words):
            best_words_file.write(int(c) + ' [' + ', '.join(map(lambda s : '\'' + s + '\'', lst)) + ']\n')

#print '\nTime after NMF output: %.3f' % (time.time() - start_time)
#sys.stdout.flush()

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

#print 'Time after NMF test transform: %.3f\n' % (time.time() - start_time)

#print 'NUMBER OF CASES PER CLUSTER:'
#cluster_sizes = [np.sum(np.array(test_clusters) == c) for c in range(n_clusters)]
#for c, sz in enumerate(cluster_sizes):
#    print '%d: %d' % (c, sz)
#print

results = zip(test_clusters, test_data)
results.sort(key = lambda (c, (f,y,t)) : 2000 * c + y) # sort by cluster, then by year
if cluster_output_filename is not None:
    with open(cluster_output_filename, 'wb') as output_file:
        writer = csv.writer(output_file)
        for c, (f,y,t) in results:
            writer.writerow((f, y, c))

if W_output_filename is not None:
    with open(W_output_filename, 'wb') as output_file:
        writer = csv.writer(output_file)
        for row, (f,y,t) in zip(test_W, test_data):
            writer.writerow((f,) + tuple(row))

if H_output_filename is not None:
    with open(H_output_filename, 'wb') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(tuple([vocab_rev[i].encode('utf-8') for i in range(len(vocab_rev.keys()))]))
        for row in H:
            writer.writerow(tuple(row))

#print '\nTime after all remaining output: %.3f\n' % (time.time() - start_time)

cluster_weights = zip(test_case_list, test_W)
n_cases = 20
if best_match_cases_filename is not None:
    with open(best_match_cases_filename, 'wb') as best_matches_file:
        for cluster_id in range(n_clusters):
            best_matches_file.write('FOR CLUSTER %d:\n' % cluster_id)
            cluster_weights.sort(key = lambda (case, weights) : -weights[cluster_id])
            clusters_ranked = map(lambda (c,w) : c, cluster_weights[0:n_cases])
            for case in clusters_ranked:
                best_matches_file.write(case + '\n')
            best_matches_file.write('\n')