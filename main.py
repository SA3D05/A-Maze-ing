from sys import argv
from curses import wrapper
from time import sleep
from utils import Maze
from deb import pdeb
import curses
from random import shuffle
import cells_place_holder


HEIGHT = int(argv[1])
WIDTH = int(argv[2])


def main(stdscr: curses.window) -> None:

    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    # stdscr.getch()

    height, width = stdscr.getmaxyx()
    maze_height = HEIGHT * 2 + 1
    maze_width = WIDTH * 2 + 1

    if maze_height > height or maze_width > width:
        pdeb(
            f"Terminal size too small for the maze ({maze_height}x{maze_width} required). Resize and try again."
        )

        stdscr.addstr(
            0,
            0,
            f"Terminal size too small for the maze ({maze_height}x{maze_width} required). Resize and try again.",
        )
        stdscr.refresh()
        stdscr.getch()
        raise Exception("Terminal size too small for the maze.")
    stdscr.addstr(
        0, WIDTH * 2 + 1, f"Terminal size: {height} rows high, {width} columns wide" * 2
    )
    stdscr.addstr(
        1,
        WIDTH * 2 + 1,
        f"Maze size: {maze_height} rows high, {maze_width} columns wide",
    )

    maze: Maze = Maze(
        cells_place_holder.cells_maze_3,
        HEIGHT,
        WIDTH,
        int((width / 2) - (maze_width / 2)),
        3,
    )

    pdeb("creating grid [...]")
    maze.gen_grid()
    # shuffle(maze.get_elements())
    # # render grid
    for element in maze.get_elements():
        stdscr.addch(element.y, element.x, element.sprite)
        stdscr.refresh()

    pdeb("complet grid [DONE]\n")
    # stdscr.getch()

    # pdeb("breaking walls [...]")
    # maze.brake_walls()
    # # render breaking wals

    # for element in maze.get_elements():
    #     sleep(0.001)
    #     stdscr.addch(element.y, element.x, element.sprite)
    #     stdscr.refresh()
    # pdeb("complet breking [DONE]\n")
    # stdscr.getch()

    # pdeb("fix corners [...]")
    # maze.handel_corners()

    # for element in maze.get_elements():
    #     stdscr.addch(element.y, element.x, element.sprite)
    #     stdscr.refresh()
    #     sleep(0.001)
    # pdeb("corners comlete [DONE]\n")

    pdeb("\npress any button to leve!\n")
    stdscr.getch()
    pdeb("byyyyyyyyyy!!")


try:
    wrapper(main)
except Exception as e:
    print(f"Error: {e}")
