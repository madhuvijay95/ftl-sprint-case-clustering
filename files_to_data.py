#######################################################################################################################
# General goal: Take a list of file names for cases, and output a csv containing basic data (file name, case name, court
# name, year, and docket number) for each case.
#
# Takes 2 inputs:
# (1) An input file name, which contains a list of files names, each on one line.
# (2) An output file name (csv)
# After this runs, the output contains the following 5 fields (comma-separated), for each file name in the input file in
# order: (1) file name, (2) abbreviated case name, (3) court name, (4) year, and (5) docket number. The docket number is
# is left blank if not available, and fields 2 through 5 are all left blank if the file name is invalid.
# (So, if the input file contains some lines that are file names and some lines that aren't, then the output file will
# keep the non-file-name lines intact and will retrieve the data corresponding to each file-name line.
#######################################################################################################################

from helpers import remove_quotes
import sys
import xml.etree.ElementTree as ET
import csv

# Namespace used for parsing the XML files.
ns = {'default' : 'http://www.loc.gov/METS/', 'xlink' : 'http://www.w3.org/1999/xlink',
      'casebody' : 'http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1',
      'case' : 'http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case:v1'}

# Convert a file into the corresponding 5-tuple containing the data for that file.
# Return a 1-tuple with the file name if the file is invalid.
def file_to_data(filename):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        data = root.find('default:dmdSec', ns).find('default:mdWrap', ns).find('default:xmlData', ns).find('case:case', ns)
        decisiondate = data.find('case:decisiondate', ns).text

        year = int(decisiondate[0:4])
        name = data.find('case:name', ns).get('abbreviation').encode('utf-8').replace('\n','').replace('\r','')
        court = data.find('case:court', ns).text.encode('utf-8').replace('\n','').replace('\r','')
        docketnumber = data.find('case:docketnumber', ns).text
        docketnumber = docketnumber.encode('utf-8').replace('\n','').replace('\r','') if docketnumber is not None else ''
        return filename, name, court, year, docketnumber
    except IOError:
        return (filename,)

# Open the input file (the 1st argument), and turn it into a list of file names.
with open(sys.argv[1], 'rb') as input_file:
    case_list = list(input_file)
    case_list = map(lambda s : s.replace('\n','').replace('\r',''), case_list)
    case_list = map(remove_quotes, case_list)

# Retrieve data for each file.
data = map(file_to_data, case_list)

# Output the data to the output file (the 2nd argument).
with open(sys.argv[2], 'wb') as output_file:
    writer = csv.writer(output_file)
    for tup in data:
        writer.writerow(tup)