#!/usr/bin/env python3
import sys
import os
import curses
import traceback
import string
import logging
from enum import Enum
from datetime import date
from contentManager import ContentManager
from screenManager import ScreenManager
from storageManager import StorageManager

class Modes(Enum):
    EDIT = 1
    NORMAL = 2
    MOVE = 3

class ListMaker:
    def __init__(self):
        self.store = None
        self.cm = None
        self.sm = None
        self.mode = Modes.NORMAL
        self.state = dict()
        os.environ.setdefault('ESCDELAY', '25')
        logging.basicConfig(filename='app.log', level=logging.DEBUG)

    def main(self, filepath):
        """The Main method that kicks off the app loop."""
        try:
            self.store = StorageManager(filepath)
            self.cm = ContentManager(self.store)
            self.sm = ScreenManager()
            self.sm.status_wnd.update_status('Normal Mode')
            content = self.cm.render()
            self.sm.update_content(content)
            while True:
                if self.mode == Modes.NORMAL:
                    self.normal_loop()
                elif self.mode == Modes.EDIT:
                    self.edit_loop()
                elif self.mode == Modes.MOVE:
                    self.move_loop()
        finally:
            curses.endwin()
            logging.exception(date.today())
            print('Exception in application')
            print('-'*50)
            print('-'*50)


    def normal_loop(self):
        """This method handles the main-loop while app is in Normal mode."""
        sm = self.sm
        cm = self.cm
        key = self.process_input()
        if key in('KEY_DOWN', 'j'):
            sm.anno_wnd.update_selected(cm.traverse_down(), 'normal')
        elif key in('KEY_UP', 'k'):
            sm.anno_wnd.update_selected(cm.traverse_up(), 'normal')
        elif key == 'c':
            content = self.cm.add_child()
            self.sm.update_content(content)
            self.start_edit()
        elif key == 's':
            self.store.write(self.cm.root)
        elif key == 'e':
            self.start_edit()
        elif key == 'm':
            self.start_move()
        elif key in ('Enter', 'b'):
            content = self.cm.add_sibling()
            self.sm.update_content(content)
            self.start_edit()
        elif key == 'd':
            content = self.cm.delete_node()
            self.sm.update_content(content)
        elif key in ('[', '<'):
            content = self.cm.promote_node()
            self.sm.update_content(content)
        elif key in (']', '>'):
            content = self.cm.demote_node()
            self.sm.update_content(content)


    def edit_loop(self):
        """This method handles the main-loop while app is in Edit mode."""
        key = self.process_input()
        if key == 'KEY_LEFT':
            target = self.cm.traverse_left()
            self.sm.show_cursor(target)
        elif key == 'KEY_RIGHT':
            target = self.cm.traverse_right()
            self.sm.show_cursor(target)
        elif key == 'Escape':
            self.end_edit()
        elif key == 'KEY_BACKSPACE':
            target = self.cm.backspace()
            self.sm.update_line(target)
            self.sm.show_cursor(target)
        elif key == 'KEY_DC':
            target = self.cm.del_char()
            self.sm.update_line(target)
            self.sm.show_cursor(target)
        elif key == 'Enter':
            self.end_edit()
            self.sm.update_content(self.cm.add_sibling())
            self.start_edit()
        elif key in string.printable:
            target = self.cm.insert(key)
            self.sm.update_line(target)
            self.sm.show_cursor(target)


    def start_edit(self):
        self.mode = Modes.EDIT
        edit_target = self.cm.get_selected_row()
        self.sm.status_wnd.update_status('Edit Mode')
        self.sm.anno_wnd.update_selected(self.cm.selected_row, 'edit')
        self.sm.show_cursor(edit_target)


    def end_edit(self):
        self.mode = Modes.NORMAL
        self.sm.status_wnd.update_status('Normal Mode')
        self.sm.anno_wnd.update_selected(self.cm.selected_row, 'normal')
        self.sm.hide_cursor()


    def move_loop(self):
        """This method handles the main-loop while app is in move mode."""
        sm = self.sm
        cm = self.cm
        key = self.process_input()
        if key in('KEY_DOWN', 'j'):
            sm.anno_wnd.update_selected(cm.traverse_down(), 'normal')
        elif key in('KEY_UP', 'k'):
            sm.anno_wnd.update_selected(cm.traverse_up(), 'normal')
        elif key == 'Escape':
            self.end_move(execute=False)
        elif key == 'Enter':
            self.end_move(execute=True)


    def start_move(self):
        """This method puts the application in Move Mode.

        This involved painting the starting item's annotation,
        updating object mode state, updating status line.
        """
        self.mode = Modes.MOVE
        self.sm.status_wnd.update_status('Move Mode')
        self.sm.anno_wnd.update_move_item(self.cm.selected_row)
        self.state['move_row'] = self.cm.selected_row


    def end_move(self, execute: bool = False):
        """This method ends the move and goes back to normal mode.

        Arguments:
            execute -- If True, the move command will be executed. If
                       False, the move will be canceled and the content
                       tree will not be changed.
        """
        if execute:
            content = self.cm.move_node(self.state.pop('move_row'))
            self.sm.update_content(content)
        self.mode = Modes.NORMAL
        self.sm.status_wnd.update_status('Normal Mode')
        self.sm.anno_wnd.clear_move()


    def process_input(self):
        ch = self.sm.getch()
        result = self.process_ch(ch)
        if result == None:
            result = self.sm.getkey()
        return result


    def process_ch(self, ch) -> str:
        if ch == 27:
            # Escape key
            return 'Escape'
        elif ch == 8:
            # Backspace key
            return 'Backspace'
        elif ch == 10:
            # Enter key
            return 'Enter'
        else:
            curses.ungetch(ch)
        return None


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

