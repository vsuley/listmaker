"""
Author: Vinayak Suley
"""
from typing import List, Tuple
import curses
from contentRow import ContentRow
from childWindows import NavWnd, AnnoWnd, ContentWnd, StatusWnd

class ScreenManager():
    """
    This class acts as the application's rendering interface. It is meant to encapsulate
    most or all of the window handling, layout, design and other display related actions.
    """


    def __init__(self):
        # Initializing COLS & LINES so pylint will stop complaining.
        # They get created by initscr, but the linting system is not
        # advanced enough to detect that.
        curses.COLS: int = 0
        curses.LINES: int = 0
        curses.initscr()
        # Layout basics
        self.indent_size = 4
        self.nav_height = 5
        self.annotations_width = 6
        self.status_height = 3
        # Navigation window
        self.nav_wnd = NavWnd(self.nav_height, curses.COLS, 0, 0)
        # Annotations window
        anno_height = curses.LINES - self.nav_height - self.status_height - 1
        anno_y = self.nav_height
        anno_x = 0
        self.anno_wnd = AnnoWnd(anno_height, self.annotations_width, anno_y, anno_x)
        # Main Content window
        content_width = curses.COLS - self.annotations_width
        content_height = curses.LINES - self.nav_height - self.status_height - 1
        content_y = self.nav_height
        content_x = self.annotations_width
        self.content_wnd = ContentWnd(content_height, content_width, content_y, content_x)
        # Status Window
        status_width = curses.COLS
        status_y = curses.LINES - self.status_height - 1
        self.status_wnd = StatusWnd(self.status_height, status_width, status_y, 0)
        # Curses settings
        curses.noecho()
        self._orig_cursor = curses.curs_set(0)


    def __del__(self):
        curses.curs_set(self._orig_cursor)
        curses.echo()
        curses.endwin()


    def update_content(self, content: Tuple[List[ContentRow], int]):
        """
        Update the main text content on screen.

        Useful whenever the content has been changed by contentManager.
        Call this method to refresh the list being displayed. Only
        affects the display, not the content being stored.
        """
        self.content_wnd.update_content(content[0])


    def show_cursor(self, target: Tuple[int, ContentRow]):
        curses.curs_set(1)
        self.content_wnd.move_cursor(target)


    def update_line(self, target: Tuple[int, ContentRow]):
        self.content_wnd.update_line(target)

    def hide_cursor(self):
        curses.curs_set(0)


    def getkey(self):
        return self.content_wnd.getkey()


    def getch(self):
        return self.content_wnd.getch()
