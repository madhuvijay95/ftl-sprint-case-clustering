# ftl-sprint-case-clustering
Work on clustering court cases (in XML format), done for Jack Cushman's Free the Law Wintersession Sprint in January 2016.

### Instructions for case clustering
**_FINISH THIS SECTION_**

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
