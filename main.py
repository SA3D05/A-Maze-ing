#!/usr/bin/python3


from curses import window, wrapper, curs_set
from model import Menu, Rendrer, MazeGenerator, MazeConfig, Maze
from cells_place_holder import cells_maze_10
from time import sleep


def main(stdscr: window):
    curs_set(0)
    stdscr.keypad(True)
    term_height, term_width = stdscr.getmaxyx()

    WIDTH = 10
    HEIGHT = 10
    maze_height = HEIGHT * 2 + 1
    maze_width = WIDTH * 2 + 1

    config: MazeConfig = MazeConfig(
        HEIGHT, WIDTH, (0, 0), (0, 0), "output.txt", True, 10, 10
    )

    menu = Menu(15, 100)
    sections = ["Start", "Settings", "Exit", "Change color", "use animations"]

    for section in sections:
        menu.add_section(section)

    generator = MazeGenerator(config)
    maze: Maze = Maze(cells_maze_10, config.height, config.width)

    generator.gen_grid(maze)
    generator.brake_walls(maze)
    generator.handel_corners(maze.get_elements())

    rendrer = Rendrer(stdscr)

    rendrer.render_maze(maze)
    rendrer.render_menu(menu)

    sleep(5)


wrapper(main)
