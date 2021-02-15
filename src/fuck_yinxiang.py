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

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.NoteStore as NoteStore
from evernote.api.client import EvernoteClient

import xml.etree.ElementTree as ET

class FuckYinxiang:
  def __init__(self, auth_token):
    self.auth_token = auth_token
    sandbox=False
    china=True
    self.client = EvernoteClient(token=auth_token, sandbox=sandbox,china=china)

    self.user_store = self.client.get_user_store()
    version_ok = self.user_store.checkVersion(
      "Evernote EDAMTest (Python)",
      UserStoreConstants.EDAM_VERSION_MAJOR,
      UserStoreConstants.EDAM_VERSION_MINOR
    )
    print("Is my Evernote API version up to date? ", str(version_ok))
    if not version_ok:
      exit(1)
    self.note_store = self.client.get_note_store()

  def process_note(self, note_guid):
    note_all_data = self.note_store.getNote(self.auth_token, note_guid, True, True, True, True)
    content = note_all_data.content
    content = content.replace("&nbsp;", " ")
    print(content)
    exit()
    doc = ET.fromstring(content)
    print(doc.itertext())
    print('\n'.join(doc.itertext()))
    exit()
    ennote = doc.findall('en-note')
    print(type(ennote))
    print(ennote)
    for child in ennote:
      print(child.text)
    exit(0)
    for item in doc.find('en-note'):
      print(item)

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

if __name__ == '__main__':
  import sys 
  auth_token = sys.argv[1] 
  yx = FuckYinxiang(auth_token)
  note_guid = yx.get_note_guid_bytitle("caller type recall precision data runtime")
  if note_guid:
    yx.process_note(note_guid)
  print("Done")
