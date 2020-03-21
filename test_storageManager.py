#!/usr/bin/env python3
from anytree import RenderTree
from entry import Entry
from pathlib import Path
from storageManager import *
import time

def test_noFile():
    filename = get_filename()
    sm = StorageManager(filename)
    e = os.path.isfile(filename)
    assert e == False


def test_write_empty():
    filename = get_filename()
    sm = StorageManager(filename)
    sm.write(None)
    e = os.path.isfile(filename)
    assert e == True
    os.remove(filename)
    

def test_read_empty():
    filename = get_filename()
    sm = StorageManager(filename)
    content = sm.read()
    assert content == None

    sm.write(None)
    content = sm.read()
    assert content == None
    os.remove(filename)


def test_read_write():
    root = get_data()
    print('Data about to be written: ')
    for pre, _, entry in RenderTree(root):
        print('%s%s' % (pre, entry.name))
    filename = get_filename()
    sm1 = StorageManager(filename)
    sm1.write(root)
    sm2 = StorageManager(filename)
    root2 = sm2.read()
    print('Data read in from the previously written file: ')
    for pre, _, entry in RenderTree(root2):
        print('%s%s' % (pre, entry.name))
    data = root2.children[0].children[0].name
    assert data == '01.01'
    os.remove(filename)


def test_overwrite():
    filename = get_filename()
    f = open(Path(filename), 'w')
    f.write('Garbage')
    f.close()
    before = get_data()
    sm = StorageManager(filename)
    sm.write(before)
    after = sm.read()
    data = after.children[0].children[0].name
    assert data == '01.01'
    os.remove(filename)

    
def get_filename():
    return time.ctime() + '.lm'


def get_data() -> Entry:
    root = Entry('root', None)
    a = Entry('Topic 01', root)
    b = Entry('Topic 02', root)
    Entry('01.01', a)
    Entry('01.02', a)
    Entry('02.01', b)
    return root

if __name__ == '__main__':
    test_overwrite()
