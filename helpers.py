#######################################################################################################################
# A few useful helper functions, mostly for parsing the case XML files. Most of the functions here take an input of
# type "Element", from xml.etree.ElementTree. In general, inputs called "root" refer to the root node of an XML file
# for a case.
#######################################################################################################################

import xml.etree.ElementTree as ET

# Namespace used for parsing the XML files.
ns = {'default' : 'http://www.loc.gov/METS/', 'xlink' : 'http://www.w3.org/1999/xlink',
      'casebody' : 'http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1',
      'case' : 'http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case:v1'}

# Find the year of a case, given the root node of the file.
def year(root):
    data = root.find('default:dmdSec', ns).find('default:mdWrap', ns).find('default:xmlData', ns)
    decisiondate = data.find('case:case', ns).find('case:decisiondate', ns).text
    return int(decisiondate[0:4])

# Find the node corresopnding to the body of a case, given the root node of the file.
def body(root):
    file_groups = root.find('default:fileSec', ns).findall('default:fileGrp', ns)
    casebody = [node for node in file_groups if node.get('USE') == 'casebody'][0]
    return casebody.find('default:file', ns).find('default:FContent', ns).find('default:xmlData', ns).find('casebody:casebody', ns)

# Given any XML node, return a string containing all text under that node (in order) by recursively traversing the
# descendants of the node.
def text_iter(node):
    if len(list(node)) == 0:
        return node.text
    else:
        return reduce(lambda s1,s2 : s1 + ' ' + s2, map(text_iter, list(node)))

# (This functions is fairly unrelated from the functions above.)
# Given a string (corresponding to some file name), remove single quotes if the string is enclosed in single quotes.
# (This is useful because it was sometimes helpful to store case lists with single quotes around each file name.)
def remove_quotes(filename):
    if len(filename) == 0:
        return ''
    elif filename[0] == '\'' and filename[-1] == '\'':
        return filename[1:(len(filename)-1)]
    else:
        return filename

def get_text(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return text_iter(body(root)).replace(u'\xad','')

def get_data(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return filename, year(root), text_iter(body(root))