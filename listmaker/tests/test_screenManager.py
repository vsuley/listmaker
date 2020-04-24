#!/usr/bin/env python3

from screenManager import *
import time

def test_creation():
    sm = ScreenManager()
    sm.refresh()
    time.sleep(1)

def test_check():
    sm = ScreenManager()
    sm.display_check()
    sm.refresh()
    time.sleep(3)


def test_addline():
    sm = ScreenManager()
    sm.add_line('Topic 01', 1)
    sm.add_line('Subtopic 01', 2)
    sm.refresh()
    sm.reset_current()
    time.sleep(5)

if __name__ == '__main__':
    #test_creation()
    #test_check()
    test_addline()
