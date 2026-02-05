#!/usr/bin/python3


from curses import window, wrapper, curs_set
import curses
from deb import pdeb
from model import Menu, Rendrer, MazeGenerator, MazeConfig, Maze
from cells_place_holder import cells_maze_10
from time import sleep
from sys import argv

# by seddek:


# def get_safe_coords(key, default_x, default_y, max_w, max_h):
#     raw_val = config_info.get(key)
#     if not raw_val:
#         return (default_x, default_y)
#
#     try:
#         # Split "0,0" into [0, 0]
#         parts = raw_val.split(",")
#         if len(parts) != 2:
#             raise ValueError
#
#         x, y = int(parts[0].strip()), int(parts[1].strip())
#
#         # Check if within maze bounds
#         if 0 <= x < max_w and 0 <= y < max_h:
#             return (x, y)
#         else:
#             print(f"[Warning]: {key} {x},{y} is out of bounds. Using default.")
#             return (default_x, default_y)
#
#     except (ValueError, IndexError):
#         print(f"[Warning]: {key} has invalid format in config. Using default.")
#         return (default_x, default_y)


# -----------------------------------------------------------------------


def main(stdscr: window):
    curs_set(0)
    stdscr.keypad(True)
    term_height, term_width = stdscr.getmaxyx()

    pdeb(f"y: {term_height}, x: {term_width}")
    # maze_height = HEIGHT * 2 + 1
    # maze_width = WIDTH * 2 + 1

    config: MazeConfig = MazeConfig()

    try:
        config.parse_config("config.txt")
    except Exception as e:
        pdeb(f"[Config error]: {e}")
        exit(1)

    maze_height = config.height * 2 + 1
    maze_width = config.width * 2 + 1

    horizontal_shit = int((term_width / 2) + 2)
    vertical_shit = int((term_height / 2) - (maze_height / 2))

    menu = Menu(vertical_shit, horizontal_shit)

    sections = ["Generate", "Show/Hide", "Change colours", "Exit"]

    if maze_height > term_height:
        pdeb(f"maze hight = {maze_height}\nmaze width = {maze_width}\n")
        pdeb(f"term hight = {term_height}\nterm width = {term_width}")
        raise Exception("Terminal size not enugh to draw the maze!")
    if maze_width + 4 + 22 > term_width:
        pdeb(f"maze hight = {maze_height}\nmaze width = {maze_width}\n")
        pdeb(f"term hight = {term_height}\nterm width = {term_width}")
        raise Exception("Terminal size not enugh to draw the maze!")
    for section in sections:
        menu.add_section(section)

    rendrer = Rendrer(stdscr)

    rendrer.render_menu(menu)
    generator = MazeGenerator(config)
    maze = Maze(
        int((term_height / 2) - (maze_height / 2)),
        int((term_width / 2) - (maze_width) - 2),
    )

    while True:
        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            term_height, term_width = stdscr.getmaxyx()

            maze.y_shift = int((term_height / 2) - (maze_height / 2))
            maze.x_shift = int((term_width / 2) - (maze_width) - 2)

            horizontal_shit = int((term_width / 2) + 2)
            vertical_shit = int((term_height / 2) - (maze_height / 2))

            menu.vertical_shift = vertical_shit
            menu.horizontal_shift = horizontal_shit

            menu.sections.clear()

            for section in sections:
                menu.add_section(section)

            stdscr.clear()

            maze.update_cells(generator.generate(config.is_perfect))
            generator.gen_grid(maze)
            generator.brake_walls(maze)
            generator.handel_corners(maze.get_elements())
            rendrer.render_maze(maze)
            rendrer.render_menu(menu)
            curses.flushinp()

        if key == ord("\n"):
            match menu.get_selected_index():
                case 0:
                    maze.update_cells(generator.generate(config.is_perfect))
                    generator.gen_grid(maze)
                    generator.brake_walls(maze)
                    generator.handel_corners(maze.get_elements())
                    rendrer.render_maze(maze)
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

# if len(argv) < 2:
#             raise Exception("Missing 'config.txt'")
#         elif len(argv) > 2:
#             raise Exception("Too many arguments")
#         filename: str = argv[1]
#         if filename != "config.txt":
#             raise Exception("Only accept 'config.txt'")

#         i = 1
#         lines: list[str] = list()
#         info = dict()

#         with open(argv[1]) as file:
#             lines = [line for line in file]

#         for line in lines:

#             if line.startswith("#"):
#                 continue

#             if "=" not in line:
#                 raise ValueError(f"invalid line '{line}'")

#             if line.startswith("WIDTH"):

#                 print(line)
