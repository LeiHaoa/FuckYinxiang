from lxml import etree
#import xml.etree.ElementTree as ET
import sys
sys.path.append('/Users/zhanghao/workspace/git/FuckYinxiang/lib')

def dfs_table(node, tableString):
  #print('processing:    ', node.tag)
  for child in node.getchildren():
    if child.tag == 'td':
      tableString += '|'
    if child.text:
      tableString += child.text
    if child.tag == 'en-media':
      print(child.attrib)
      tableString += str(child.attrib)
    tableString = dfs_table(child, tableString)
  return tableString
import io

def process_table_old(table):
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

def process_en_media(node):
  return str(node.attrib)+'\n'

def dfs_text(node, text):
  if node.text:
    text += node.text
  for child in node.getchildren():
    if child.text:
      text += child.text
    if child.tag == 'en-media':
      print(child.attrib)
      text += process_en_media(child)
    text = dfs_text(child, text)
  return text

def process_table(table):
  print("processing table new")
  table_content = ''
  #---- thead ----#
  head = table.find('thead')
  if head:
    for tr in head.findall('tr'):
      table_content += "|"
      for td in tr.findall('td'):
        table_content = dfs_text(td, table_content) + " |"
      table_content += "\n"
  #---- tbody ----#
  body = table.find('tbody')
  if body:
    for tr in body.findall('tr'):
      table_content += "|"
      for td in tr.findall('td'):
        #table_content = dfs_text(td, table_content) + " |"
        table_content += dfs(td, 7) + " |"
      table_content += "\n"
  print(table_content)
  return table_content

def process_ulist(ulist):
  return None
def dfs(node, count):
  result_text = ""
  #print("{}ntag: {}{}".format(''.join(['-']*count), node.tag, ''.join(['-']*count)))
  if node.text:
    #print('{} text: {}'.format(node.tag, node.text))
    result_text += node.text

  if node.tag == 'br':
    result_text += '\n'
  elif node.tag == 'span':
    print(node.attrib)
  elif node.tag == 'table':
    result_text += process_table(node)
    print(result_text)
    return result_text
  elif node.tag == 'ul':
    print("**************TODOOOOOOOOOOOOOOOOO 215******************")
    print(node.itertext())
    result_text += '\n'.join(node.itertext())
    return result_text
  elif node.tag == 'en-media':
    print("xxxxxxxxx", node.attrib)
    result_text += process_en_media(node)
    return result_text

  for child in node.getchildren():
    result_text += dfs(child, count - 1)

  return result_text

if __name__ == '__main__':
  import html2text
  h = html2text.HTML2Text()
  with open('/Users/zhanghao/workspace/git/FuckYinxiang/tmp_rich.xml', 'r') as f:
    h.image_to_alt = True
    print(h.handle(f.read()).replace("\n\n", '\n').replace('\n|\n', '|'))
  '''
  doc = etree.parse('/Users/zhanghao/workspace/git/FuckYinxiang/test_content.xml')
  print(dir(doc))
  result = dfs(doc.getroot(), 10)
  print('----------------------------------------------------------------------------------')
  
  print(result)
  #print(etree.tostring(doc.getroot()))
  '''
  '''
  with open('./tmp.xml') as f:
    xmlstr = f.read()
    doc = ET.fromstring(xmlstr)
    print(type(doc))
    dfs(doc, 10)
  '''
