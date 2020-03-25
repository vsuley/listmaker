#!/usr/bin/env python3
from contentManager import ContentManager
from screenManager import ScreenManager
from storageManager import StorageManager
import sys
import time
import curses

class ListMaker:

    def main(self, filepath):
        try:
            self.store = StorageManager(filepath)
            self.cm = ContentManager(self.store)
            self.sm = ScreenManager()

            while True:
                content_rows = self.cm.render_list()
                self.sm.render(content_rows)
                key = self.sm.getkey()
                self.process_key(key)
        except:
            curses.endwin()
            print('Unexpected error: ', sys.exc_info())


    def process_key(self, key):
        sm = self.sm
        cm = self.cm
        if key == 'KEY_UP':
            sm.update_active(cm.traverse_up())
            sm.refresh()
        elif key == 'KEY_DOWN':
            sm.update_active(cm.traverse_down())
            sm.refresh()
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

