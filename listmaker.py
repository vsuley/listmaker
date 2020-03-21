#!/usr/bin/env python3
import sys
import time
from contentManager import ContentManager
from screenManager import ScreenManager
from storageManager import StorageManager

def main(filepath):
    store = StorageManager(filepath)
    cm = ContentManager(store)
    sm = ScreenManager()

    done = True
    while not done:
        cm.render(sm)
        wait_for_input()
    sys.exit(0)


def wait_for_input():
    time.sleep(1)


if __name__ == '__main__':
    argv = sys.argv
    if(len(argv) < 2):
        print('Please provide the path of the file you want to edit, or path to new file.')
        sys.exit(-1)
    elif(len(argv) > 2):
        print('Program accepts only one argument, which should be the file you want to edit or create.')
        sys.exit(-1)
    main(argv[1])

