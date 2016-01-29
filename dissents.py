import time
import sys
import csv
from helpers import remove_quotes
#import xml.etree.ElementTree as ET
#import numpy as np
#from pyquery import PyQuery as pq
#from lxml import etree

ns = {'default' : 'http://www.loc.gov/METS/', 'xlink' : 'http://www.w3.org/1999/xlink',
      'casebody' : 'http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1',
      'case' : 'http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case:v1'}

#def has_dissent_old(case_filename):
#    root = ET.parse(case_filename).getroot()
#    opinions = list(root.iter('{' + ns['casebody'] + '}opinion'))
#    #opinions = filter(lambda node : node.tag == '{' + ns['casebody'] + '}opinion', descendants)
#    return reduce(lambda b, op : b or (op.get('type') == 'dissent'), opinions, False)

#def check_dissents_old(case_file_list):
#    dissents = filter(has_dissent_old, case_file_list)
#    for case in dissents:
#        print case

def has_dissent2(case_filename):
    return '<opinion type="dissent">' in open(case_filename, 'rb').read()

def check_dissents2(case_file_list):
    dissents = filter(has_dissent2, case_file_list)
    for case in dissents:
        print case

start_time = time.time()
with open(sys.argv[1], 'rb') as input_file:
    reader = csv.reader(input_file)
    dissent_cases = [row for row in reader if has_dissent2(remove_quotes(row[0]))]
    #for row in reader:
    #    case_filename = remove_quotes(row[0])
    #    if has_dissent2(case_filename):
    #        print row[0]
    #case_list = list(input_file)
    #case_list = map(lambda s : s.replace('\n','').replace('\r',''), case_list)
    #case_list = map(remove_quotes, case_list)
#print 'Time after reading and checking for dissents: %.3f' % (time.time() - start_time)

if len(sys.argv) > 2:
    with open(sys.argv[2], 'wb') as output_file:
        writer = csv.writer(output_file)
        for case in dissent_cases:
            writer.writerow(tuple(case))
else:
    for case in dissent_cases:
        print tuple(case)
#check_dissents2(case_list)
#print 'Time at end: %.3f' % (time.time() - start_time)
#print 'Time at end: %.3f' % (time.time() - start_time)