from contentManager import *
import curses
import sys

class ScreenManager(object):
    
    def __init__(self):
        self._screen = curses.initscr()
        self._screen.keypad(True)
        curses.noecho()

        # default layout
        self.indent_size = 4
        self.bcb_row = 0
        self.bcb_height = 3
        self.title_row = self.bcb_row + self.bcb_height
        self.title_height = 3
        self.content_start =  self.title_height + self.title_row
        self.curr_row = self.content_start


    def __del__(self):
        curses.echo()
        self._screen.keypad(False)
        curses.endwin()


    def render(self, cm: ContentManager):
        l = cm.render_list()
        for row in l:
            entry = row.entry
            self.add_line(entry.name, row.indent_lvl)
        self.refresh()
        self.reset_current()

    def refresh(self):
        self._screen.refresh()


    def add_line(self, line: str, indent_lvl: int):
        col = indent_lvl * self.indent_size
        row = self.curr_row
        self._screen.addstr(row, col, line)
        self.curr_row += 1
    

    def reset_current(self):
        self.curr_row = self.content_start


    def display_check(self):
        self._screen.addstr(0, 0, 'x')

