from anytree import NodeMixin, RenderTree
import sys

class Entry(NodeMixin):
    def __init__(self, 
                 name: str, 
                 parent = None, 
                 decorations: list = None, 
                 text: str = None,
                 children = None,
                 curs: int = 0):
        self.name = name
        self.parent = parent
        if decorations:
            self.decorations = decorations
        if text:
            self.text = text
        if children:
            self.children = children
        self.curs = curs


    def insert(self, char):
        self.name = self.name[:self.curs] + \
                    char + self.name[self.curs:]
        self.curs += len(char)


    def backspace(self) -> bool:
        """
        Executes a 'backspace' keystroke on entry's text.

        Encapsulates the logic for whether the commands is valid at this
        time or not.

        Returns:
            True if text was modified. 
            False if command is invalid and no text was modified.
        """
        if self.curs == 0:
            return False
        self.name = self.name[:self.curs - 1] + self.name[self.curs:]
        self.curs -= 1
        return True


    def del_char(self) -> bool:
        """
        Executes a 'delete character' command on the entry's text.

        Encapsualates logic for whether the command is valid at this time
        or not.

        Returns:
            'True' if text was modified.
            'False' if command is invalid and text was not modified.
        """
        if len(self.name) == 0:
            return False
        self.name = self.name[:self.curs] + self.name[self.curs + 1:]
        if self.curs > len(self.name) - 1:
            self.curs = len(self.name)
        return True

    def curs_right(self):
        if self.curs == len(self.name) - 1:
            return
        self.curs += 1


    def curs_left(self):
        if self.curs == 0:
            return
        self.curs -= 1


