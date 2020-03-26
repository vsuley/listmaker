#!/usr/bin/env python3
from contentManager import ContentManager
from screenManager import ScreenManager
from storageManager import StorageManager
from enum import Enum
import sys
import os
import time
import curses
import traceback

class Modes(Enum):
    EDIT = 1
    NORMAL = 2

class ListMaker:
    
    
    def __init__(self):
        self.store = None
        self.cm = None
        self.sm = None
        self.mode = Modes.NORMAL 
        os.environ.setdefault('ESCDELAY', '25')
    
    def main(self, filepath):
        try:
            self.store = StorageManager(filepath)
            self.cm = ContentManager(self.store)
            self.sm = ScreenManager()
            self.sm.update_status('Normal Mode')
            while True:
                content = self.cm.render()
                self.sm.update_content(content)
                ch = self.sm.getch()
                self.process_ch(ch)
                key = self.sm.getkey()
                self.process_key(key)
        except:
            curses.endwin()
            print('Exception in application')
            print('-'*50)
            traceback.print_exc()
            print('-'*50)


    def process_ch(self, ch):
        sm = self.sm
        cm = self.cm
        if ch == 27:
           # Escape key
           if self.mode == Modes.EDIT:
               self.mode = Modes.NORMAL
               sm.update_status('Normal Mode')
        else:
            curses.ungetch(ch)


    def process_key(self, key):
        sm = self.sm
        cm = self.cm
        
        if (self.mode == Modes.NORMAL):
            if key == 'KEY_LEFT' or key == 'h':
                pass
            elif key == 'KEY_DOWN' or key == 'j':
                sm.update_selected(cm.traverse_down())
            elif key == 'KEY_UP' or key == 'k':
                sm.update_selected(cm.traverse_up())
            elif key == 'KEY_RIGHT' or key == 'l':
                pass
            elif key == 'c':
                self.add_child()
            elif key == 's':
                self.store.write(self.cm.root)
            elif key == 'e':
                self.mode = Modes.EDIT
                self.sm.update_status('Edit Mode')
            else:
                pass
        elif (self.mode == Modes.EDIT):
            pass

    def add_child(self):
        cm = self.cm
        sm = self.sm
        content = cm.add_child()
        sm.update_content(content)


if __name__ == '__main__':
    argv = sys.argv
    if(len(argv) < 2):
        print('Please provide the path of the file you want to edit, or path to new file.')
        sys.exit(-1)
    elif(len(argv) > 2):
        print('Program accepts only one argument, which should be the file you want to edit or create.')
        sys.exit(-1)
    lm = ListMaker()
    lm.main(argv[1])

