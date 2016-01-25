#from year_sort import file_to_year, remove_quotes
from test_real import year
import sys
import xml.etree.ElementTree as ET
import csv

ns = {'default' : 'http://www.loc.gov/METS/', 'xlink' : 'http://www.w3.org/1999/xlink',
      'casebody' : 'http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1',
      'case' : 'http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case:v1'}

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

def remove_quotes(filename):
    if len(filename) == 0:
        return ''
    elif filename[0] == '\'' and filename[-1] == '\'':
        return filename[1:(len(filename)-1)]
    else:
        return filename

with open(sys.argv[1], 'rb') as input_file:
    case_list = list(input_file)
    case_list = map(lambda s : s.replace('\n','').replace('\r',''), case_list)
    case_list = map(remove_quotes, case_list)

data = map(file_to_data, case_list)
with open(sys.argv[2], 'wb') as output_file:
    writer = csv.writer(output_file)
    for tup in data:
        writer.writerow(tup)