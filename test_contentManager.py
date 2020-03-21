#!/usr/bin/env python3
from contentManager import *
import time

def test_creation():
    filename = time.ctime() + '.lm'
    cm = ContentManager(filename)

def test_create_and_save():
    cm = ContentManager()
    filename = time.ctime() + '.lm'

if __name__ == '__main__':
    test_creation()
