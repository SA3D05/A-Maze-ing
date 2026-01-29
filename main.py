from sys import argv
from curses import wrapper
from time import sleep
from utils import Maze
from deb import pdeb
import curses
from generator import MazeGenerator
from model import Cell as ModelCell


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
            f"Terminal size too small for the maze "
            f"({maze_height}x{maze_width} required). "
            "Resize and try again."
        )

        stdscr.addstr(
            0,
            0,
            (
                f"Terminal size too small for the maze "
                f"({maze_height}x{maze_width} required). "
                "Resize and try again."
                ),
                )
        stdscr.refresh()
        stdscr.getch()
        raise Exception("Terminal size too small for the maze.")
    stdscr.addstr(
        0,
        WIDTH * 2 + 1,
        (
            f"Terminal size: {height} rows high, "
            f"{width} columns wide"
            ) * 2,
            )

    stdscr.addstr(
        1,
        WIDTH * 2 + 1,
        f"Maze size: {maze_height} rows high, {maze_width} columns wide",
    )

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
    # convert generator.Cell (x,y,walls) -> model.Cell(y,x,up,down,left,right)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            gcell = gen_maze.cells[y][x]
            up_open = not gcell.walls[0]
            right_open = not gcell.walls[1]
            down_open = not gcell.walls[2]
            left_open = not gcell.walls[3]
            converted_cells.append(ModelCell(y, x, up_open, down_open,
                                             left_open, right_open))

    maze: Maze = Maze(
        converted_cells,
        HEIGHT,
        WIDTH,
        0,
        0,
    )

    pdeb("creating grid [...]")
    maze.gen_grid()
    # shuffle(maze.get_elements())
    # # render grid
    for element in maze.get_elements():
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


wrapper(main)
