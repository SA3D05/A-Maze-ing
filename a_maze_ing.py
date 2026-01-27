from cells_place_holder import cells_maze_10, cells_maze_3
from typing import List, Dict, Union, Any, Set
from random import shuffle
from curses import wrapper
from time import sleep
from utils import Maze
from sys import argv
from deb import pdeb
import curses


WIDTH = int(argv[1])
HEIGHT = int(argv[2])


def main(stdscr: curses.window) -> None:

    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    stdscr.getch()

    # get terminal size
    term_height, term_width = stdscr.getmaxyx()

    # calculate maze size
    maze_height = HEIGHT * 2 + 1
    maze_width = WIDTH * 2 + 1

    maze: Maze = Maze(
        cells_maze_10,
        HEIGHT,
        WIDTH,
        int((term_width / 2) - (maze_width / 2)),
        int((term_height / 2) - (maze_height / 2)),
        # 3,
        # 3,
        # 0,
        # 0,
    )

    pdeb("creating grid [...]")
    maze.gen_grid()
    shuffle(maze.get_elements())
    # render grid
    for element in maze.get_elements():
        sleep(0.001)
        stdscr.addch(element.y, element.x, element.sprite)
        stdscr.refresh()

    pdeb("complet grid [DONE]\n")
    stdscr.getch()

    pdeb("breaking walls [...]")
    maze.brake_walls()
    # render breaking wals

    for element in maze.get_elements():
        sleep(0.001)
        stdscr.addch(element.y, element.x, element.sprite)
        stdscr.refresh()
    pdeb("complet breking [DONE]\n")
    stdscr.getch()

    pdeb("fix corners [...]")
    maze.handel_corners()

    for element in maze.get_elements():
        stdscr.addch(element.y, element.x, element.sprite)
        stdscr.refresh()
        sleep(0.001)
    pdeb("corners comlete [DONE]\n")

    pdeb("\npress any button to leve!\n")
    stdscr.getch()
    pdeb("byyyyyyyyyy!!")


# try:
wrapper(main)
# except Exception as e:
#     print(f"Error: {e}\ntraceback:\n{e.__traceback__}")
