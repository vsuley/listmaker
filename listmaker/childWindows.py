"""
Author: Vinayak Suley
URL: https://github.com/vsuley/listmaker
"""
from typing import List, Tuple
from contentRow import ContentRow
from entry import Entry
import curses
import sys


class AnnoWnd:
    """
    Class to help manage displaying of per-row annotations.
    """
    def __init__(self, lines: int, cols: int, begin_y: int, begin_x: int) -> None:
        self.wnd = curses.newwin(lines, cols, begin_y, begin_x)
        self.wnd.keypad(True)
        # Selection related annotation details
        self.selected_mrk = '>'
        self.selected_mrk_col = 3
        self.selected_mrk_row = 0
        # Moving related annotation details
        self.move_mrk_col = 0
        self.move_item_mrk = '●'
        self.move_dest_mrk = '◘'
        self.move_dest_row = None
        self.move_item_row = None
        self.collapse_mrk_col = 1


    def update_selected(self, sel_row: int, mode: str) -> None:
        """
        This method paints a pointer that helps to show the user which row the
        app currently considers 'selected'.

        Keyword arguments:
            sel_row: int -- The row to be highlighted
            mode: str -- 'normal', 'edit' or 'move'
        """
        if mode == 'edit':
            # self.selected_mrk = '}'#'►'
            self.selected_mrk = '►'
        else:
            self.selected_mrk = '>'
        x = self.selected_mrk_col
        # Erase previous annotation
        y = self.selected_mrk_row
        self.wnd.addstr(y, x, ' ')
        # Set new annotation
        y = self.selected_mrk_row = sel_row
        self.wnd.addstr(y, x, self.selected_mrk)
        self.wnd.refresh()


    def update_move_item(self, row: int) -> None:
        """This method paints a marker in the move annotations column
        to mark the position of the item being moved.

        Arguments:
            row -- The row number (0 based) where you want to paint
                   the mark
        """
        x = self.move_mrk_col
        y = self.move_item_row = row
        self.wnd.addstr(y, x, self.move_item_mrk)
        self.wnd.refresh()


    def update_move_dest(self, row: int) -> None:
        """This method paints a marker in the move annotations column
        to mark the position of where the item is being moved.

        Arguments:
            row -- Row being considered as a destination for move.
        """
        x = self.move_mrk_col
        y = self.move_dest_row = row
        self.wnd.addstr(y, x, self.move_dest_mrk)
        self.wnd.refresh()


    def clear_move(self) -> None:
        """This method clears any move related marks."""
        x = self.move_mrk_col
        if self.move_item_row:
            y = self.move_item_row
            self.wnd.addstr(y, x, ' ')
            self.move_item_row = None
        if self.move_dest_row:
            y = self.move_dest_row
            self.wnd.addstr(y, x, ' ')
            self.move_dest_row = None
        self.wnd.refresh()


class ContentWnd:
    """
    Class to help manage display of list content.
    """

    def __init__(self, lines: int, cols: int, begin_y: int, begin_x: int) -> None:
        self.wnd = curses.newwin(lines, cols, begin_y, begin_x)
        self.wnd.keypad(True)
        self.indent_size = 4

    def update_content(self, content_list: List[ContentRow]):
        self.wnd.clear()
        y = 0
        for content_row in content_list:
            text = content_row.entry.name
            x = content_row.indent_lvl * self.indent_size
            self.wnd.addstr(y, x, text)
            y += 1
        self.wnd.refresh()
   

    def getch(self):
        return self.wnd.getch()


    def getkey(self):
        return self.wnd.getkey()


    def move_cursor(self, target: Tuple[int, ContentRow]):
        y = target[0]
        cr = target[1]
        entry = cr.entry
        x = entry.curs + (cr.indent_lvl * self.indent_size)
        self.wnd.move(y, x)


    def update_line(self, target: Tuple[int, ContentRow]):
        y = target[0]
        cr = target[1]
        x = cr.indent_lvl * self.indent_size
        self.wnd.move(y, x)
        self.wnd.clrtoeol()
        self.wnd.addstr(y, x, cr.entry.name)
        self.wnd.move(y, x)
        self.wnd.refresh()


class StatusWnd:
    """
    Class to help manage the display of status information in a bar below the content.
    """


    def __init__(self, lines: int, cols: int, begin_y: int, begin_x: int) -> None:
        self.wnd = curses.newwin(lines, cols, begin_y, begin_x)
        self.wnd.addstr(0, 0, '-------------------------------------------------------------')
        self.wnd.border()
        self.wnd.refresh()


    def update_status(self, status: str, dirty: bool) -> None:
        """
        Updates status information in status sub-window.

        Mode is on the left hand side. Dirty status is on right hand side.
        """
        self.wnd.clear()

        # Mode information
        self.wnd.addstr(1, 2, status)

        # Dirty information
        start_pos: int = self.wnd.getmaxyx()[1] - 2 - len('DIRTY')
        if dirty:
            self.wnd.addstr(1, start_pos, 'DIRTY')

        self.wnd.border()
        self.wnd.refresh()


    def update_dirty(self, value: bool) -> None:
        """
        Displays dirty information on the right side of status bar.
        """

class NavWnd:
    def __init__(self, lines: int, cols: int, begin_y: int, begin_x: int) -> None:
        self.wnd = curses.newwin(lines, cols, begin_y, begin_x)
        self.wnd.keypad(True)

