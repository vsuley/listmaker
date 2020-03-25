#!/usr/bin/env python3
from contentManager import ContentManager
from screenManager import ScreenManager
from storageManager import StorageManager
import sys
import time
import curses

class ListMaker:

    def main(self, filepath):
        self.store = StorageManager(filepath)
        self.cm = ContentManager(self.store)
        self.sm = ScreenManager()

        while True:
            self.sm.render(cm)
            key = sm.getkey()
            self.process_key(key)

    def process_ch(self, ch):
        pass


    def process_key(self, key):
        if key == 'KEY_UP':
            active_row = self.cm.traverse_up()
            self.sm.place_cursor(active_row)
            self.sm.refresh()
        elif key == 'KEY_DOWN':
            active_row = self.cm.traverse_down()
            self.sm.place_cursor(active_row)
            self.sm.refresh()
        elif key == 'KEY_LEFT':
            pass
        elif key == 'KEY_RIGHT':
            pass

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

