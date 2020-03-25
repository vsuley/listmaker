import curses
import sys

class ScreenManager(object):
    
    def __init__(self):
        self._screen = curses.initscr()
        self._screen.keypad(True)
        curses.noecho()
        self._orig_cursor = curses.curs_set(0)

        # default layout
        self.left_margin = 4
        self.indent_size = 4
        self.bcb_row = 0
        self.bcb_height = 3
        self.title_row = self.bcb_row + self.bcb_height
        self.title_height = 3
        self.active_col = 0

        # Conveniences
        self.content_start =  self.title_height + self.title_row

        # Starting values
        self.active_row = 0


    def __del__(self):
        curses.curs_set(self._orig_cursor)
        curses.echo()
        self._screen.keypad(False)
        curses.endwin()
        print('Screen manager says goodbye')


    def render(self, content_rows: list):
        row_num = self.content_start
        for r in content_rows:
            self._add_line(r.entry.name, row_num, r.indent_lvl)
            row_num += 1
        self.refresh()


    def refresh(self):
        self._screen.refresh()


    def update_active(self, row: int):
        # Clean previous glyph
        y = self.active_row + self.content_start
        x = self.active_col
        self._screen.addstr(y, x, ' ')
        # Update active row
        self.active_row = row
        # Apply glyph to new active row 
        y = self.active_row + self.content_start
        x = self.active_col
        self._screen.addstr(y, x, '>')

        
    def _add_line(self, name: str, row: int, indent_lvl: int):
        col = self.left_margin + indent_lvl * self.indent_size
        self._screen.addstr(row, col, name)
    

    def getkey(self):
        return self._screen.getkey()


    def getch(self):
        return self._screen.getch()

