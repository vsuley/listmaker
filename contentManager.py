from entry import Entry
from anytree import RenderTree
from storageManager import StorageManager
from screenManager import ScreenManager
import sys

class ContentManager:
    '''This class manages the content for the listMaker'''

    def __init__(self, store: StorageManager):
        self.root = store.read()
        if(self.root == None):
            self.root = Entry('root', None)
            a = Entry('Topic 01', root)
            b = Entry('Subtopic', a)
            c = Entry('Topic 02', root)


    def render(sm: ScreenManager):
      start = self.root
