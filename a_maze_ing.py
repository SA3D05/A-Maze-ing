from typing import List, Dict, Union, Any, Set
from random import shuffle
from curses import wrapper
from time import sleep
from utils import Maze
from sys import argv
from deb import pdeb
import curses
from generator import MazeGenerator
from model import Cell as ModelCell
from typing import List, Dict, Union, Any, Set
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

    # Generate maze via MazeGenerator and convert to model.Cell list
    class Config:
        width = WIDTH
        height = HEIGHT
        entry = (0, 0)
        exit = (WIDTH - 1, HEIGHT - 1)
        perfect = True
        algorithm = "prim"
        seed = None

    gen = MazeGenerator(Config(), verbose=False)
    gen_maze = gen.generate()

    converted_cells = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            gcell = gen_maze.cells[y][x]
            up_open = not gcell.walls[0]
            right_open = not gcell.walls[1]
            down_open = not gcell.walls[2]
            left_open = not gcell.walls[3]
            converted_cells.append(ModelCell(y, x, up_open, down_open, left_open, right_open))

    maze: Maze = Maze(
        converted_cells,
        HEIGHT,
        WIDTH,
        int((term_width / 2) - (maze_width / 2)),
        int((term_height / 2) - (maze_height / 2)),
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
