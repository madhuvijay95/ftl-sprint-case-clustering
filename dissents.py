#######################################################################################################################
# Takes a list of case file names, checks whether each one has a dissenting opinion, and outputs the susbet of cases
# that have dissents. Takes 2 arguments: (1) an input file name, in which each line contains the file name for a case,
# and (2) an output file name, which the program writes to. Each case is judged to contain a dissenting opinion if and
# only if the file contains the string '<opinion type="dissent">'.
#######################################################################################################################

import time
import sys
import csv
from helpers import remove_quotes

ns = {'default' : 'http://www.loc.gov/METS/', 'xlink' : 'http://www.w3.org/1999/xlink',
      'casebody' : 'http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1',
      'case' : 'http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case:v1'}

def has_dissent(case_filename):
    return '<opinion type="dissent">' in open(case_filename, 'rb').read()

start_time = time.time()
with open(sys.argv[1], 'rb') as input_file:
    reader = csv.reader(input_file)
    dissent_cases = [row for row in reader if has_dissent(remove_quotes(row[0]))]

if len(sys.argv) > 2:
    with open(sys.argv[2], 'wb') as output_file:
        writer = csv.writer(output_file)
        for case in dissent_cases:
            writer.writerow(tuple(case))
else:
    for case in dissent_cases:
        print tuple(case)