#!/usr/bin/python3

from models.player import Player, PlayerDirection
from models.maze_generator import MazeGenerator
from curses import window, wrapper, curs_set
from models.maze_config import MazeConfig
from models.renderer import Rendrer
from utils import init_colors, sections
from models.maze import Maze
from models.menu import Menu
from random import choice
from typing import List
from sys import argv
import curses


def main(stdscr: window):
    curs_set(0)
    stdscr.keypad(True)

    init_colors()

    term_height, term_width = stdscr.getmaxyx()

    config: MazeConfig = MazeConfig()

    try:
        config.parse_config("config.txt")
    except Exception as e:
        print(f"[Config error]: {e}")
        exit(1)

    maze_height = config.height * 2 + 1
    maze_width = config.width * 2 + 1

    menu = Menu(int((term_height / 2) - (maze_height / 2)), int((term_width / 1.5)))

    exit_index = len(sections) - 1
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

    current_color_id = 1
    show_hide = False
    duration = 0.0003

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
                    curses.flushinp()

                # play
                case 1:
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
                case 2:
                    show_hide = not show_hide
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)

                # change color
                case 3:
                    old_color = current_color_id
                    while current_color_id is old_color:
                        current_color_id = choice([1, 5, 10, 15, 20])
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)

                # Exit
                case exit_index:
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

    # try:
    wrapper(main)
    # except KeyboardInterrupt:
    #     print("Exit the program")
    # except curses.error as e:
    #     print(f"[Curses error]: {e}")
    # except BaseException as e:
    #     print(f"[Error]: {e}")
