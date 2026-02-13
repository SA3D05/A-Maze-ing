#!/usr/bin/python3

from curses import window, wrapper, curs_set
from typing import List
from random import choice
from mazegen import *
from sys import argv
import curses


def main(stdscr: window):
    curs_set(0)
    stdscr.keypad(True)

    curses.init_color(20, 200, 800, 1000)  # Sky Blue
    curses.init_color(21, 950, 950, 1000)  # Pure Ice White
    curses.init_color(22, 500, 950, 1000)  # Bright Teal
    curses.init_color(23, 700, 850, 1000)  # Periwinkle
    curses.init_color(24, 1000, 500, 600)  # Pastel Watermelon

    curses.init_color(25, 1000, 850, 600)  # Creamy Peach
    curses.init_color(26, 1000, 400, 400)  # Bright Coral
    curses.init_color(27, 1000, 950, 200)  # Laser Yellow
    curses.init_color(28, 1000, 600, 800)  # Bright Orchid
    curses.init_color(29, 1000, 300, 0)  # Burning Orange

    curses.init_color(30, 1000, 1000, 1000)  # Full White
    curses.init_color(31, 800, 850, 900)  # Bright Silver
    curses.init_color(32, 400, 600, 1000)  # Tech Blue
    curses.init_color(33, 1000, 400, 0)  # Safety Orange
    curses.init_color(34, 1000, 100, 300)  # Neon Red

    curses.init_color(35, 400, 1000, 200)  # Spring Green
    curses.init_color(36, 0, 1000, 600)  # Turquoise Green
    curses.init_color(37, 700, 1000, 700)  # Seafoam Mint
    curses.init_color(38, 600, 1000, 0)  # Bright Chartreuse
    curses.init_color(39, 900, 1000, 300)  # Lemon Lime

    curses.init_color(40, 0, 960, 1000)  # Electric Cyan
    curses.init_color(41, 1000, 200, 600)  # Bright Hot Pink
    curses.init_color(42, 800, 650, 1000)  # Vivid Lavender
    curses.init_color(43, 1000, 600, 200)  # Sunset Orange
    curses.init_color(44, 700, 300, 1000)  # Bright Violet

    curses.use_default_colors()

    for i in range(25):
        curses.init_pair(i + 1, 20 + i, -1)

    sections: List[str] = [
        "Generate",
        "With steps",
        "Play",
        "Show/Hide",
        "Change colours",
        "Exit",
    ]

    config: MazeConfig = MazeConfig()

    # use that if parsing comleet
    # try:
    #     config.parse_config("config.txt")
    # except Exception as e:
    #     print(f"[Config error]: {e}")
    #     exit(1)

    term_height, term_width = stdscr.getmaxyx()

    maze_height = config.height * 2 + 1
    maze_width = config.width * 2 + 1

    menu_yshift = int((term_height / 2) - (maze_height / 2))
    menu_xshift = int((term_width / 1.5))

    maze_yshift = int((term_height / 2) - (maze_height / 2))
    maze_xshift = int((term_width / 2) - (maze_width))

    # check if terminal size perfict for rendring without errors
    if maze_width + 2 > term_width / 2:  # if terminal pass maze + sections
        raise Exception("Terminal size not enugh to draw the maze!")

    if 3 * len(sections) + 4 > term_height:  # if terminal pass sections
        raise Exception("Terminal size not enugh to draw the maze!")

    if maze_height + 4 > term_height:  # if terminal pass maze
        raise Exception("Terminal size not enugh to draw the maze!")

    menu = Menu(menu_yshift, menu_xshift)
    rendrer = Rendrer(stdscr)
    generator = MazeGenerator(config)
    maze = Maze(maze_yshift, maze_xshift)

    current_color_id = 1
    show_hide = False
    duration = 0.001
    for section in sections:
        menu.add_section(section)
    rendrer.render_menu(menu)

    generator.gen_grid(maze)
    rendrer.render_maze(maze, duration, current_color_id, show_hide)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            raise Exception("Please do not resize the terminal or i will kill you")
        elif key == ord("\n"):
            match menu.get_selected_index():
                # generate
                case 0:
                    generator.generate(maze, config.is_perfect)
                    generator.gen_grid(maze)
                    generator.brake_walls(maze)
                    generator.handel_corners(maze.get_elements())
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)

                # generate with steps
                case 1:
                    rendrer.erase_maze(maze)
                    generator.generate(maze, config.is_perfect)
                    generator.gen_grid(maze)
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)
                    generator.brake_walls(maze)
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)
                    generator.handel_corners(maze.get_elements())
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)

                # play
                case 2:

                    old_show_hide = show_hide
                    show_hide = False
                    player = Player(
                        *config.entry,
                        maze.y_shift,
                        maze.x_shift,
                        "@",
                    )
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)
                    rendrer.render_player(player)
                    while True:
                        last_player_pos = (player.y, player.x)
                        player_key = stdscr.getch()
                        if player_key == curses.KEY_RESIZE:
                            raise Exception(
                                "Please do not resize the terminal or i will kill you"
                            )

                        elif player_key == ord("q") or player_key == ord("Q"):
                            break

                        elif player_key == curses.KEY_UP:

                            player.move(PlayerDirection.UP, maze.get_cells())
                            rendrer.render_player(player, last_player_pos)

                        elif player_key == curses.KEY_DOWN:
                            player.move(PlayerDirection.DOWN, maze.get_cells())
                            rendrer.render_player(player, last_player_pos)

                        elif player_key == curses.KEY_LEFT:
                            player.move(PlayerDirection.LEFT, maze.get_cells())
                            rendrer.render_player(player, last_player_pos)

                        elif player_key == curses.KEY_RIGHT:
                            player.move(PlayerDirection.RIGHT, maze.get_cells())
                            rendrer.render_player(player, last_player_pos)

                        if (player.y, player.x) == config.exit:
                            break
                        curses.flushinp()

                    show_hide = old_show_hide
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)

                # show/hide
                case 3:
                    show_hide = not show_hide
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)

                # change color
                case 4:
                    old_color = current_color_id
                    while current_color_id is old_color:
                        current_color_id = choice([1, 5, 10, 15, 20])
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)

                # Exit
                case 5:
                    break

        elif key == curses.KEY_DOWN:
            menu.move_down()
            rendrer.render_menu(menu)
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
        print(f"[Arguments error]: {e}")
        exit(1)

    try:
        wrapper(main)
    except KeyboardInterrupt:
        print("Exit the program")
    except curses.error as e:
        print(f"[Curses error]: {e}")
    except BaseException as e:
        print(f"[Error]: {e}")
