"""
Author: Vinayak Suley
URL: https://github.com/vsuley/listmaker
"""
from typing import List, Tuple
from anytree import RenderTree
from entry import Entry
from contentRow import ContentRow
from storageManager import StorageManager


class ContentManager:
    '''This class manages the content for the listMaker
    '''

    def __init__(self, store: StorageManager):
        self.root = store.read()
        self.dirty = False
        if self.root is None:
            self.root = Entry('root', None)
            a = Entry('Topic 01', self.root)
            b = Entry('Subtopic', a)
            c = Entry('Topic 02', self.root)
            self.dirty = True
        if(self.root.children == None):
            a = Entry(' ', self.root)
            self.dirty = True
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
            

    def add_child(self) -> Tuple[List[ContentRow], int]:
        cr = self.content_list[self.selected_row]
        e = cr.entry
        child = Entry('', e)
        self.dirty = True
        self.render()
        self.selected_row = self.find_entry_pos(child)       
        return (self.content_list, self.selected_row)


    def add_sibling(self) -> Tuple[List[ContentRow], int]:
        cr = self.content_list[self.selected_row]
        e = cr.entry
        if e != self.root:
            p = e.parent
            child = Entry('', p)
            self.dirty = True
            self.render()
            self.selected_row = self.find_entry_pos(child)       
        return (self.content_list, self.selected_row)

    
    def delete_node(self) -> Tuple[List[ContentRow], int]:
        cr = self.content_list[self.selected_row]
        e = cr.entry
        p = e.parent
        if e == self.root:
            # Can't do
            return (self.content_list, self.selected_row)
        if len(e.children) > 0:
            # Reassign children to node's parent.
            for x in e.children:
                x.parent = p
        if self.selected_row == len(self.content_list) - 1:
            # If selection is at last row, we'll need to move it up
            self.selected_row -= 1
        # The following line removes the node
        e.parent = None
        self.dirty = True
        self.render()
        return (self.content_list, self.selected_row)


    def move_node(self, move_row: int) -> Tuple[List[ContentRow], int]:
        """
        Moves the specified row before currently selected position,
        this includes being able to move to a different parent. The
        row being moved will be made sibling to currently selected
        row. Cannot be moved to root. Cannot be moved to descendant.

        Return:
            A tuple where first element is a list of content rows
            and second element is the indiex of currently selected
            row.
        """
        sel_row = self.content_list[self.selected_row]
        sel_node = sel_row.entry
        move_row = self.content_list[move_row]
        move_node = move_row.entry
        if (sel_node in move_node.descendants) or sel_node == move_node or sel_node == self.root:
            return (self.content_list, self.selected_row)
        move_node.parent = None
        child_list = list(sel_node.parent.children)
        index = child_list.index(sel_node)
        child_list.insert(index, move_node)
        sel_node.parent.children = child_list
        self.dirty = True
        self.render()
        return (self.content_list, self.selected_row)


    def promote_node(self) -> Tuple[List[ContentRow], int]:
        """
        Promotes (unindents) the currently selected node. In effect,
        promotion is moving a node up a level so that its grandparent
        would now be its parent.

        Returns:
            A tuple where first element is a list of content rows
            and second element is the index of the currently selected
            row.
        """

        cr = self.content_list[self.selected_row]
        e = cr.entry
        p = e.parent
        if p == self.root or e == self.root:
            # Can't do
            return (self.content_list, self.selected_row)
        grandparent = p.parent
        e.parent = grandparent
        self.dirty = True
        self.render()
        return (self.content_list, self.selected_row)


    def demote_node(self) -> Tuple[List[ContentRow], int]:
        """
        Demotes (indents) the currently selected node. The logic in
        demote works a little different from promote because while
        they appear symmetric in terms of lines displayed, within the
        Tree space these are asymmetric operations. Demote will eval-
        uate the node in the line above and see if the selected node
        can be made a child of that

        Returns:
            A tuple where first element is a list of content rows
            and second element is the index of the currently selected
            row.
        """

        cr = self.content_list[self.selected_row]
        e = cr.entry
        p = e.parent
        if p == self.root or e == self.root:
            # Can't do
            return (self.content_list, self.selected_row)
        grandparent = p.parent
        e.parent = grandparent
        self.dirty = True
        self.render()
        return (self.content_list, self.selected_row)


    def get_selected_row(self) -> Tuple[int, ContentRow]:
        return (self.selected_row, self.content_list[self.selected_row])


    def traverse_right(self) -> Tuple[int, ContentRow]:
        self.content_list[self.selected_row].entry.curs_right()
        return (self.selected_row, self.content_list[self.selected_row])


    def traverse_left(self) -> Tuple[int, ContentRow]:
        self.content_list[self.selected_row].entry.curs_left()
        return (self.selected_row, self.content_list[self.selected_row])


    def backspace(self) -> Tuple[int, ContentRow]:
        if self.content_list[self.selected_row].entry.backspace():
            self.dirty = True
        return (self.selected_row, self.content_list[self.selected_row])


    def del_char(self) -> Tuple[int, ContentRow]:
        if self.content_list[self.selected_row].entry.del_char():
            self.dirty = True
        return (self.selected_row, self.content_list[self.selected_row])


    def insert(self, char) -> Tuple[int, ContentRow]:
        entry = self.content_list[self.selected_row].entry
        entry.insert(char)
        return (self.selected_row, self.content_list[self.selected_row])


    def delete(self) -> Tuple[List[ContentRow], int]:
        return (self.content_list, self.selected_row)


    def find_entry_pos(self, ent: Entry) -> int:
        pos = 0
        for x in self.content_list:
            if x.entry == ent:
                return pos
            pos += 1
        return -1


