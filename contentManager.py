from typing import List, Tuple
from entry import Entry
from contentRow import ContentRow
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
        self.selected_row = 0
        self.render()


    def render(self) -> Tuple[List[ContentRow], int]:
        cl = list()
        for pre, _, entry in RenderTree(self.root):
            indent_lvl = int(len(pre) / 4)
            row = ContentRow(entry, indent_lvl)
            cl.append(row)
        self.content_list = cl
        return (self.content_list, self.selected_row)


    def traverse_up(self) -> int:
        if self.selected_row > 0:
            self.selected_row -= 1
        return self.selected_row


    def traverse_down(self) -> int:
        last_row = len(self.content_list) - 1
        if self.selected_row < last_row:
            self.selected_row += 1
        return self.selected_row
            

    def traverse_right(self) -> int:
        pass


    def traverse_left(self) -> int:
        pass


    def add_child(self) -> Tuple[List[ContentRow], int]:
        cr = self.content_list[self.selected_row]
        e = cr.entry
        child = Entry('new Child', e)
        self.render()
        #pos = self.find_entry_pos(child)       
        self.selected_row = 0
        return (self.content_list, self.selected_row)

    
    def find_entry_pos(self, ent: Entry) -> int:
        row = (x for x in self.content_list if x.entry == ent)
        pos = self.content_list.index(row)
        return pos


