from lxml import etree
#import xml.etree.ElementTree as ET

plist = ['div']

def dfs_table(node, tableString):
  #print('processing:    ', node.tag)
  for child in node.getchildren():
    if child.tag == 'td':
      tableString += '|'
    if child.text:
      tableString += child.text
    tableString = dfs_table(child, tableString)
  return tableString

def process_table(table):
  print('processing table')
  #TODO add print table header 
  table = table.find('tbody')
  table_content = ''
  for c in table.getchildren():
    if c.tag == 'tr': #one line
      one_line = ''
      one_line = dfs_table(c, one_line)
      table_content += one_line + '\n'
  return table_content

def dfs(node, count):
  print("{}ntag: {}{}".format(''.join(['-']*count), node.tag, ''.join(['-']*count)))
  for child in node.getchildren():
    if child.tag == 'table':
      print(process_table(child))
      #print(etree.tostring(child))
    elif child.text:
      print('{} text: {}'.format(child.tag, child.text))
    else:
      pass
    dfs(child, count - 1)

if __name__ == '__main__':
  doc = etree.parse('/Users/zhanghao/workspace/git/FuckYinxiang/tmp.xml')
  print(dir(doc))
  dfs(doc.getroot(), 10)
  #print(etree.tostring(doc.getroot()))
  '''
  with open('./tmp.xml') as f:
    xmlstr = f.read()
    doc = ET.fromstring(xmlstr)
    print(type(doc))
    dfs(doc, 10)
  '''
