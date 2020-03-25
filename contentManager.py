from entry import Entry
from anytree import RenderTree
from storageManager import StorageManager
import sys

class ContentManager:
    '''This class manages the content for the listMaker
    '''

    def __init__(self, store: StorageManager):
        self.root = store.read()
        if(self.root == None):
            self.root = Entry('root', None)
            a = Entry('Topic 01', self.root)
            b = Entry('Subtopic', a)
            c = Entry('Topic 02', self.root)
        if(self.root.children == None):
            a = Entry(' ', self.root)
        self.render_list()
        self.active_row = 0


    def render_list(self) -> list:
        cl = list()
        for pre, _, entry in RenderTree(self.root):
            indent_lvl = int(len(pre) / 4)
            row = ContentRow(entry, indent_lvl, False)
            cl.append(row)
        self.content_list = cl
        return self.content_list


    def traverse_up(self) -> int:
        if self.active_row > 0:
            self.active_row -= 1
        return self.active_row


    def traverse_down(self) -> int:
        last_row = len(self.content_list) - 1
        if self.active_row < last_row:
            self.active_row += 1
        return self.active_row
            

    def traverse_right(self) -> int:
        pass


    def traverse_left(self) -> int:
        pass


class ContentRow:
    '''Represents a single row of content'''

    def __init__(self, 
                 entry: Entry, 
                 indent_lvl: int,
                 temp: bool):
        self.entry = entry
        self.indent_lvl = indent_lvl
        self.temp = temp
