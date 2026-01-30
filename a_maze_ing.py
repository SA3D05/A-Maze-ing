from unittest import case
from cells_place_holder import cells_maze_10, cells_maze_3
from typing import List, Dict, Union, Any, Set
from random import shuffle
from curses import wrapper
from time import sleep
from utils import Maze
from sys import argv
from deb import pdeb
import curses
from model import MenuSection, Menu

WIDTH = int(argv[1])
HEIGHT = int(argv[2])


# • Re-generate a new maze and display it.
# • Show/Hide a valid shortest path from the entrance to the exit.
# • Change maze wall colours.
def render_elements(stdscr, elements):
    for element in elements:
        stdscr.addch(element.y, element.x, element.sprite)
        stdscr.refresh()


def rebuild(stdscr, menu, vertical_shit, horizontal_shit):
    for section in menu.get_sections():
        for element in section.get_elements():
            stdscr.addch(
                element.y,
                element.x,
                element.sprite if section.selected else " ",
            )

        stdscr.addstr(
            vertical_shit + 1,
            (horizontal_shit + 1) + (20 // 2) - (len(section.text) // 2),
            section.text,
        )
        vertical_shit += 3


def main(stdscr: curses.window) -> None:

    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.clear()
    stdscr.refresh()

    # get terminal size
    term_height, term_width = stdscr.getmaxyx()

    # calculate maze size
    maze_height = HEIGHT * 2 + 1
    maze_width = WIDTH * 2 + 1

    maze: Maze = Maze(
        cells_maze_10,
        HEIGHT,
        WIDTH,
        int((term_width / 2) - (maze_width) - 2),
        int((term_height / 2) - (maze_height / 2)),
    )

    tp = 3 * 4
    mz = (maze_height - tp) / 2
    horizontal_shit = int((term_width / 2) + 2)
    vertical_shit = int((term_height / 2) - mz)

    menu = Menu(vertical_shit, horizontal_shit)

    sections = [
        "Start",
        "Re-generate",
        "Show/Hide",
        "Exit",
    ]

    for text in sections:
        menu.add_section(text)

    stdscr.refresh()
    menu.build()
    rebuild(stdscr, menu, vertical_shit, horizontal_shit)

    maze.gen_grid()
    maze.brake_walls()
    maze.handel_corners()
    render_elements(
        stdscr,
        maze.get_elements(),
    )
    stdscr.getch()
    # randomize the elements
    # shuffle(maze.get_elements())

    # stdscr.addstr(0, 0, "creating grid [...]")
    # render_elements(stdscr, maze.get_elements())
    # stdscr.getch()

    # stdscr.addstr(1, 0, "breaking walls [...]")
    # stdscr.getch()

    stdscr.addstr(2, 0, "fix corners [...]")
    maze.handel_corners()
    empty = False
    # while True:
    #     key = stdscr.getch()
    #     if key == curses.KEY_UP:
    #         stdscr.addstr(2, 0, "You pressed UP   ")
    #         menu.move_up()
    #         rebuild(stdscr, menu, vertical_shit, horizontal_shit)
    #     elif key == curses.KEY_DOWN:
    #         stdscr.addstr(2, 0, "You pressed DOWN ")
    #         menu.move_down()
    #         rebuild(stdscr, menu, vertical_shit, horizontal_shit)
    #     elif key == curses.KEY_LEFT:
    #         stdscr.addstr(2, 0, "You pressed LEFT ")
    #     elif key == curses.KEY_RIGHT:
    #         stdscr.addstr(2, 0, "You pressed RIGHT")
    #     elif key == ord("\n"):
    #         stdscr.addstr(2, 0, "You pressed ENTER")
    #         match menu.get_selected_index():
    #             case 0:
    #                 maze.gen_grid()
    #                 maze.brake_walls()
    #                 maze.handel_corners()
    #                 render_elements(stdscr, maze.get_elements())
    #                 empty = False

    #             case 1:
    #                 for element in maze.get_elements():
    #                     stdscr.addch(element.y, element.x, " ")
    #                 render_elements(stdscr, maze.get_elements())
    #                 maze.gen_grid()
    #                 render_elements(stdscr, maze.get_elements())
    #                 maze.brake_walls()
    #                 maze.handel_corners()
    #                 render_elements(stdscr, maze.get_elements())
    #                 empty = False

    #             case 2:
    #                 empty = not empty
    #                 render_elements(stdscr, maze.get_elements(), empty)
    #             case 3:
    #                 break

    #             case _:
    #                 stdscr.addstr(3, 0, "Nothing")

    #     elif key == ord("q"):
    #         break


# try:
wrapper(main)
# except Exception as e:
#     print(f"Error: {e}\ntraceback:\n{e.__traceback__}")
