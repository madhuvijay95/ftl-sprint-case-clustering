# ftl-sprint-case-clustering
Work on clustering court cases (in XML format), done for Jack Cushman's Free the Law Wintersession Sprint in January 2016.

### Descriptions of files
Each `.py` file in this repository contains much more detailed documentation in comments, but more general descriptions of the purposes of the files are provided here.

#### Core files
- **`sample.py`**: **[FINISH]**
- **`topics.py`**: **[FINISH]**
- **`output_JSON_new.py`**: **[FINISH]**

#### Other general files
- **`files_to_data.py`**: Retrieves and outputs various data (case name, court name, year, and docket number) for a given list of case XML files.
- **`dissents.py`**: Takes a list of cases, checks whether each one has a dissenting opinion, and outputs a list of the subset of cases that have dissents in them.
- **`helpers.py`**: Contains various functions that are used by the other files, especially for parsing the XML files of cases. (This file is just a centralized set of helper functions, and is not meant to be used by users.)

### Instructions for case clustering
The use of the files above to cluster cases is illustrated by example: the following sequence of Unix shell commands would take all cases in a subdirectory called California, cluster them using `topics.py`, and produce JSON output using `output_JSON_new.py`. (All estimated times are based on a data set consisting of 126,418 cases from California.)

1. **`find -type f California | grep xml > case_list.txt`**
  * **Purpose/overview**: **[FINISH]**
  * **Detailed description**: **[FINISH]**
  * **Running time: **[FINISH]**
2. 

**_FINISH THIS SECTION_**
