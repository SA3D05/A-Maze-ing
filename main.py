#!/usr/bin/python3


from curses import window, wrapper, curs_set
import curses
from deb import pdeb
from model import Menu, Rendrer, MazeGenerator, MazeConfig, Maze
from cells_place_holder import cells_maze_10
from time import sleep
import sys

# by seddek:


# config = {}
# try:
#     with open("config.txt", "r") as fd:
#         for line in fd:
#             if "=" in line and not line.startswith("#"):
#                 key, value = line.strip().split("=", 1)
#                 config[key.strip().upper()] = value.strip()
#         WIDTH = int(config.get("WIDTH", 10))
#         HEIGHT = int(config.get("HEIGHT", 10))
#         is_perfect_str = config.get("PERFECT", "TRUE").strip().upper()
#         is_perfect = is_perfect_str == "TRUE"
# except (FileNotFoundError, PermissionError, KeyError, ValueError) as e:
#     print(f"[Error loading], using default config {e}")
#     WIDTH = 10
#     HEIGHT = 10
#     is_perfect = True


# def get_safe_coords(key, default_x, default_y, max_w, max_h):
#     raw_val = config.get(key)
#     if not raw_val:
#         return (default_x, default_y)

#     try:
#         # Split "0,0" into [0, 0]
#         parts = raw_val.split(",")
#         if len(parts) != 2:
#             raise ValueError

#         x, y = int(parts[0].strip()), int(parts[1].strip())

#         # Check if within maze bounds
#         if 0 <= x < max_w and 0 <= y < max_h:
#             return (x, y)
#         else:
#             print(f"[Warning]: {key} {x},{y} is out of bounds. Using default.")
#             return (default_x, default_y)

#     except (ValueError, IndexError):
#         print(f"[Warning]: {key} has invalid format in config. Using default.")
#         return (default_x, default_y)


# -----------------------------------------------------------------------


def main(stdscr: window):
    curs_set(0)
    stdscr.keypad(True)
    term_height, term_width = stdscr.getmaxyx()

    WIDTH = 10
    HEIGHT = 10

    maze_height = HEIGHT * 2 + 1
    maze_width = WIDTH * 2 + 1

    config: MazeConfig = MazeConfig(
        HEIGHT, WIDTH, (0, 0), (0, 0), "output.txt", True, 10, 30
    )

    menu = Menu(15, 100)

    sections = ["Start", "Re-generate", "Exit", "Change color", "debbar"]
    for section in sections:
        menu.add_section(section)

    rendrer = Rendrer(stdscr)

    rendrer.render_menu(menu)
    generator = MazeGenerator(WIDTH, HEIGHT, config)
    maze = Maze()

    playabel: bool = False
    while True:
        key = stdscr.getch()
        # pdeb("loop")
        if key == ord("q"):
            break
        elif key == ord("\n"):
            match menu.get_selected_index():
                case 0:
                    if not playabel:
                        playabel = True
                        maze.update_cells(generator.generate(False))
                        generator.gen_grid(maze)
                        generator.brake_walls(maze)
                        generator.handel_corners(maze.get_elements())
                        rendrer.render_maze(maze)
                        curses.flushinp()
                case 1:
                    maze.update_cells(generator.generate(False))
                    generator.gen_grid(maze)
                    generator.brake_walls(maze)
                    generator.handel_corners(maze.get_elements())
                    rendrer.render_maze(maze)
                    curses.flushinp()
                case 2:
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
    wrapper(main)
