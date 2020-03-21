from anytree import NodeMixin, RenderTree
import sys

class Entry(NodeMixin):
    def __init__(self, 
                 name: str, 
                 parent = None, 
                 decorations: list = None, 
                 text: str = None,
                 children = None):
        self.name = name
        self.parent = parent
        if decorations:
            self.decorations = decorations
        if text:
            self.text = text
        if children:
            self.children = children


