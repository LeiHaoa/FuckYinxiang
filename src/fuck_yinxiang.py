#
# A simple Evernote API demo script that lists all notebooks in the user's
# account and creates a simple test note in the default notebook.
#
# Before running this sample, you must fill in your Evernote developer token.
#
# To run (Unix):
#   export PYTHONPATH=../../lib; python EDAMTest.py
#

import os
os.environ['PYTHONPATH'] = '/Users/zhanghao/workspace/git/FuckYinxiang/lib'
import sys
sys.path.append('/Users/zhanghao/workspace/git/FuckYinxiang/lib')
#from PIL import Image
import io

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.NoteStore as NoteStore
from evernote.api.client import EvernoteClient

import xml.etree.ElementTree as ET
from lxml import etree
from io import StringIO, BytesIO
from convert import *
import html2text

class FuckYinxiang:
  def __init__(self, auth_token):
    self.auth_token = auth_token
    sandbox=False
    china=True
    self.client = EvernoteClient(token=auth_token, sandbox=sandbox,china=china)

    self.user_store = self.client.get_user_store()
    print("version: ", UserStoreConstants.EDAM_VERSION_MINOR, UserStoreConstants.EDAM_VERSION_MAJOR)
    version_ok = self.user_store.checkVersion(
      "Evernote EDAMTest (Python)",
      UserStoreConstants.EDAM_VERSION_MAJOR,
      UserStoreConstants.EDAM_VERSION_MINOR
    )
    print("Is my Evernote API version up to date? ", str(version_ok))
    if not version_ok:
      exit(1)
    self.note_store = self.client.get_note_store()
    self.export_dir = "/Users/zhanghao/workspace/"

  def process_note(self, note_guid):
    note_all_data = self.note_store.getNote(self.auth_token, note_guid, True, True, True, True)
    
    if note_all_data.resources:
      #makdir to store media data
      resource_dir = os.path.join(self.export_dir, note_all_data.title)
      if not os.path.exists(resource_dir):
        os.mkdir(resource_dir)
      print(dir(note_all_data))

      for x in note_all_data.resources:
        file_content = x.data.body
        media_hash = hashlib.md5(file_content).hexdigest()
        file_type = x.mime
        file_name = x.attributes.fileName
        if file_type == "image/png":
          pass
          image = Image.open(io.BytesIO(x.data.body))
          image.save(os.path.join(resource_dir, "{}.png".format(media_hash)))
    
    content = note_all_data.content
    print(type(content))
    content = content.replace("&nbsp", " ")
    content = content.replace('\n\n', '\n')
    
    h = html2text.HTML2Text()
    rich_table = True #rich table (paper sumer)
    if rich_table:
      content = content.replace('\n|\n', '|')
    md = h.handle(content)
    print(md)
    '''
    #doc = ET.fromstring(content)
    #print(type(content))
    with open('./test_content_onlytext.xml', 'w') as f:
      f.write(content.decode('utf-8'))
      print('write done')
    doc = etree.XML(content)
    print("-------------------------------------------------------")
    print(dfs(doc, 10))
    '''

  def get_note_guid_bytitle(self, note_title):
    for notebook in self.note_store.listNotebooks():
      notebookGuid = notebook.guid
      notefilter = NoteStore.NoteFilter()
      notefilter.notebookGuid = notebookGuid
      for note in self.note_store.findNotes(self.auth_token, notefilter, 0, 999).notes:
        #print(note.title)
        if note.title == note_title: 
          return note.guid
    return None

  def process_all_notebook(self, notebook_title):
    for notebook in self.note_store.listNotebooks():
      if notebook.name == notebook_title:
        notefilter = NoteStore.NoteFilter()
        notefilter.notebookGuid = notebookGuid
        for note in self.note_store.findNotes(self.auth_token, notefilter, 0, 999).notes:
          process_note(note.guid)

if __name__ == '__main__':
  import sys 
  auth_token = sys.argv[1] 
  yx = FuckYinxiang(auth_token)
  #note_guid = yx.get_note_guid_bytitle("caller type recall precision data runtime")
  note_guid = yx.get_note_guid_bytitle("notebook ssh远程连接服务器")
  print("note guid: ", note_guid)
  if note_guid:
    yx.process_note(note_guid)
  print("Done")
