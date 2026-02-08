#!/usr/bin/python3

from curses import window, wrapper, curs_set
import curses

from deb import pdeb
from sys import argv
from random import choice

from models.maze import Maze
from models.maze_config import MazeConfig
from models.maze_generator import MazeGenerator
from models.menu import Menu
from models.renderer import Rendrer


def main(stdscr: window):
    curs_set(0)
    stdscr.keypad(True)
    curses.init_color(10, 90, 78, 129)

    # Define Cool Maze Wall Colors
    curses.init_color(11, 0, 960, 1000)  # Neon Cyan
    curses.init_color(12, 1000, 0, 498)  # Electric Pink
    curses.init_color(13, 717, 580, 956)  # Soft Lavender

    # Create Color Pairs (Foreground, Background)
    curses.init_pair(1, 11, 10)  # Cyan on Void
    curses.init_pair(2, 12, 10)  # Pink on Void
    curses.init_pair(3, 13, 10)  # Lavender on Void

    term_height, term_width = stdscr.getmaxyx()

    config: MazeConfig = MazeConfig()

    try:
        config.parse_config("config.txt")
    except Exception as e:
        pdeb(f"[Config error]: {e}")
        exit(1)

    maze_height = config.height * 2 + 1
    maze_width = config.width * 2 + 1

    menu = Menu(int((term_height / 2) - (maze_height / 2)), int((term_width / 1.5)))

    sections = ["Generate", "Show/Hide", "Change colours", "Exit"]

    if maze_width + 2 > term_width / 2:  # if terminal pass maze + sections
        raise Exception("Terminal size not enugh to draw the maze!")
    if 3 * len(sections) + 4 > term_height:  # if terminal pass sections
        raise Exception("Terminal size not enugh to draw the maze!")
    if maze_height + 4 > term_height:  # if terminal pass maze
        raise Exception("Terminal size not enugh to draw the maze!")

    for section in sections:
        menu.add_section(section)

    rendrer = Rendrer(stdscr)

    rendrer.render_menu(menu)
    generator = MazeGenerator(config)
    maze = Maze(
        int((term_height / 2) - (maze_height / 2)), int((term_width / 2) - (maze_width))
    )

    generator.gen_grid(maze)

    colors_id = [1, 2, 3]
    current_color_id = 1

    rendrer.render_maze(maze, 0.001, current_color_id)
    while True:
        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            raise Exception("Please do not resize the terminal or i will kill you")
        if key == ord("\n"):
            match menu.get_selected_index():
                case 0:
                    maze.update_cells(generator.generate(config.is_perfect))
                    generator.gen_grid(maze)
                    generator.brake_walls(maze)
                    generator.handel_corners(maze.get_elements())
                    rendrer.render_maze(maze, 0.0003, current_color_id)
                    curses.flushinp()
                case 2:
                    old_color = current_color_id
                    while current_color_id is old_color:
                        current_color_id = choice(colors_id)
                    rendrer.render_maze(maze, 0.0003, current_color_id)
                    curses.flushinp()

                case 3:
                    break

        elif key == curses.KEY_DOWN:
            menu.move_down()
            rendrer.render_menu(menu)
            curses.flushinp()
        elif key == curses.KEY_UP:
            menu.move_up()
            rendrer.render_menu(menu)
            curses.flushinp()


if __name__ == "__main__":

    try:
        if len(argv) < 2:
            raise KeyboardInterrupt("Missing config file")
        elif len(argv) > 2:
            raise Exception("Too many arguments")
    except Exception as e:
        pdeb(f"[Arguments error]: {e}")
        exit(1)

    try:
        wrapper(main)
    except KeyboardInterrupt:
        print("Exit the program")
    except curses.error as e:
        print(f"[Curses error]: {e}")
    except BaseException as e:
        print(f"[Error]: {e}")
