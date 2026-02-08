import time
import curses
from models.maze import Maze
from models.menu import Menu


class Rendrer:
    def __init__(self, stdscr: curses.window) -> None:
        self.stdscr: curses.window = stdscr

    def render_maze(self, maze: Maze, duration: float, color_id: int):

        for element in maze.get_elements():
            self.stdscr.addch(
                element.y, element.x, element.sprite, curses.color_pair(color_id)
            )

            self.stdscr.refresh()
            time.sleep(duration)

    def render_menu(self, menu: Menu):
        for section in menu.get_sections():
            for element in section.get_elements():
                self.stdscr.addch(
                    element.y,
                    element.x,
                    element.sprite if section.selected else " ",
                )

            self.stdscr.addstr(
                section.v_shift + 1,
                (section.h_shift + 1) + (20 // 2) - (len(section.text) // 2),
                section.text,
            )
        self.stdscr.refresh()
