### Descriptions of files
Each `.py` file in this repository contains much more detailed documentation in comments, but more general descriptions of the purposes of the files are provided here.

#### Core files
- [**`sample.py`**](sample.py): Takes a list of cases and a decimal between 0 and 1 representing a proportion, and outputs a random subsample of cases containing that proportion of the total case list.
- [**`topics.py`**](topics.py): Trains and applies a clustering algorithm, and outputs a cluster assignment for each case, and lists of the most representative words and cases for each cluster.
- [**`output_JSON_new.py`**](output_JSON_new.py): Takes the cluster output from `topics.py` and outputs a JSON file that can be used to track the prevalence of cases from each cluster over time.

#### Other general files
- [**`files_to_data.py`**](files_to_data.py): Retrieves and outputs various data (case name, court name, year, and docket number) for a given list of case XML files.
- [**`dissents.py`**](dissents.py): Takes a list of cases, checks whether each one has a dissenting opinion, and outputs a list of the subset of cases that have dissents in them.
- [**`helpers.py`**](helpers.py): Contains various functions that are used by the other files, especially for parsing the XML files of cases. (This file is just a centralized set of helper functions, and is not meant to be used by users.)

### Instructions for case clustering
The use of the files above to cluster cases is illustrated by example: the following sequence of Unix shell commands would take all cases in a subdirectory called California, cluster them into 100 clusters using `topics.py`, and produce JSON output using `output_JSON_new.py`. (All estimated times are based on a data set consisting of 126,418 cases from California.)

1. **`find California/ -type f | grep xml > case_list.txt`**
  * _Purpose/overview_: Creates a list of all XML files in the California/ directory, and writes this list to `case_list.txt`.
  * _Description_: The Unix command `find California/ -type f` outputs all files (`-type f`) in the California/ directory. The `grep xml` command filters that list so that it only includes XML files. Finally, `> case_list.txt` redirects the output to the file `case_list.txt` (instead of standard output.)
  * _Running time_: 11s
2. **`python sample.py case_list.txt 0.1 case_list_sample.txt`**
  * _Purpose/overview_: Chooses a random subsample of 10% of the case files (from `case_list.txt`), and writes that subsample to `case_list_sample.txt`. This is useful because it takes a long time to train the clustering algorithm, and it's much more convenient (and still reasonably accurate) to train on a subsample rather than on the whole data set.
  * _Description_: Further documentation is provided in `sample.py`; that program chooses a random sample (with replacement) of the lines from `case_list.txt`, using the second argument (which is 0.1 in this case) to determine the proportion of cases in the sample.
  * _Running time_: 0.5s
3. **`python topics.py 100 case_list_sample.txt case_list.txt clusters.csv best_words.txt best_cases.txt`**
  * _Purpose/overview_: Trains a clustering algorithm on the subsample in `case_list_sample.txt` to produce 100 clusters, and runs that algorithm on the entire data set in `case_list.txt`. Outputs cluster assignments (1 case per line) into `clusters.csv`, and outputs the best words and best-match cases for each cluster into `best_words.txt` and `best_cases.txt`, respectively.
  * _Description_: Uses an [NMF](https://en.wikipedia.org/wiki/Non-negative_matrix_factorization) algorithm for clustering cases. Implementation details (and more specific details about input arguments) are provided in `topics.py`. Currently, `topics.py` outputs the 50 best words and 20 best cases for each cluster; however, these parameters are easy to change. Beware if running on a personal computer, as the clustering algorithm takes up close to 5 GB of RAM and runs for hours. **[FINISH / CHECK OVER]**
  * _Running time_: **[FINISH]**
4. **`python dissents.py case_list.txt case_list_dissents.txt`**
  * _Purpose/overview_: Examines each case in `case_list.txt` to check whether it has a dissenting opinion. Outputs a list of all cases that have dissenting opinions to `case_list_dissents.txt`.
  * _Description_: Checks whether each case has a dissenting opinion by looking for the string '<opinion type="dissent">' in the XML file.
  * _Running time_: **[FINISH]**
5. **`python output_JSON_new.py best_words.txt clusters.csv output.json case_list_dissents.txt`**
  * _Purpose/overview_: Output a JSON file `output.json` containing data on the number of cases (as well as Supreme Court cases and cases with dissenting opinions, in particular) for each cluster in each year.
  * _Description_: Outputs a JSON that contains (for each cluster): the best-match words, the number of cases by year, the number of Supreme Court cases by year, the number of cases with dissenting opinions by year, and the number of SC cases with dissenting opinions by year. Uses `best_words.txt` for the lists of best words, `clusters.csv` for cluster assignments and counts, and `case_list_dissents.txt` (an optional argument that significantly improves the running time) for a list of cases with dissenting opinions.
  * _Running time_: **[FINISH]**


#### Other potentially useful commands

1. **`python files_to_data.py case_list.txt case_data.csv`**: Outputs a csv `case_data.csv`, which contains the file name, case name, court name, year, and docket number corresponding to each case in `case_list.txt`. _Running time_ (for all California cases): 47m24s.

**_FINISH THIS SECTION_**
