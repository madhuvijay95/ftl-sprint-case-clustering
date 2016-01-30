# ftl-sprint-case-clustering
Work on clustering court cases (in XML format), done for Jack Cushman's Free the Law Wintersession Sprint in January 2016.

### Descriptions of files
Each `.py` file in this repository contains much more detailed documentation in comments, but more general descriptions of the purposes of the files are provided here.

#### Core files
- **`sample.py`**: Takes a list of cases and a decimal between 0 and 1 representing a proportion, and outputs a subsample of cases containing that proportion of the total case list.
- **`topics.py`**: Trains and applies a clustering algorithm, and outputs a cluster assignment for each case, and lists of the most representative words and cases for each cluster.
- **`output_JSON_new.py`**: **[FINISH]**

#### Other general files
- **`files_to_data.py`**: Retrieves and outputs various data (case name, court name, year, and docket number) for a given list of case XML files.
- **`dissents.py`**: Takes a list of cases, checks whether each one has a dissenting opinion, and outputs a list of the subset of cases that have dissents in them.
- **`helpers.py`**: Contains various functions that are used by the other files, especially for parsing the XML files of cases. (This file is just a centralized set of helper functions, and is not meant to be used by users.)

### Instructions for case clustering
The use of the files above to cluster cases is illustrated by example: the following sequence of Unix shell commands would take all cases in a subdirectory called California, cluster them into 100 clusters using `topics.py`, and produce JSON output using `output_JSON_new.py`. (All estimated times are based on a data set consisting of 126,418 cases from California.)

1. **`find California -type f | grep xml > case_list.txt`**
  * _Purpose/overview_: **[FINISH]**
  * _Detailed description_: **[FINISH]**
  * _Running time_: 12s
2. **`python sample.py case_list.txt 0.1 > case_list_sample.txt`**
  * _Purpose/overview_: **[FINISH]**
  * _Detailed description_: **[FINISH]**
  * _Running time_: **[FINISH]**
3. **`python topics.py 100 case_list_sample.txt case_list.txt clusters.csv best_words.txt best_cases.txt`**
  * _Purpose/overview_: **[FINISH]**
  * _Detailed description_: **[FINISH]**
  * _Running time_: **[FINISH]**
4. **`python dissents.py case_list.txt case_list_dissents.txt`**
  * _Purpose/overview_: **[FINISH]**
  * _Detailed description_: **[FINISH]**
  * _Running time_: **[FINISH]**
5. **`python output_JSON_new.py best_words.txt clusters.csv output.json case_list_dissents.txt`**
  * _Purpose/overview_: **[FINISH]**
  * _Detailed description_: **[FINISH]**
  * _Running time_: **[FINISH]**

**_FINISH THIS SECTION_**
