#!/usr/bin/python3

from models.player import Player, PlayerDirection
from models.maze_generator import MazeGenerator
from curses import window, wrapper, curs_set
from models.maze_config import MazeConfig
from models.renderer import Rendrer
from typing import List, Optional
from models.maze import Maze
from models.menu import Menu
from random import choice, randint, shuffle
from deb import pdeb
from sys import argv
import curses


def main(stdscr: window):
    curs_set(0)
    stdscr.keypad(True)
    curses.init_color(10, 90, 78, 129)

    # Color IDs 20-24
    curses.init_color(20, 0, 960, 1000)  # Neon Cyan
    curses.init_color(21, 1000, 0, 498)  # Electric Pink
    curses.init_color(22, 717, 580, 956)  # Soft Lavender
    curses.init_color(23, 1000, 800, 0)  # Electric Orange
    curses.init_color(24, 600, 0, 1000)  # Deep Violets (Foreground, Background)

    # Color IDs 25-29
    curses.init_color(25, 223, 1000, 78)  # Neon Green
    curses.init_color(26, 0, 647, 396)  # Forest Green
    curses.init_color(27, 600, 1000, 600)  # Mint
    curses.init_color(28, 0, 400, 200)  # Deep Moss
    curses.init_color(29, 800, 1000, 0)  # Lime

    # Color IDs 30-34
    curses.init_color(30, 533, 752, 815)  # Frost Blue
    curses.init_color(31, 937, 945, 960)  # Snow White
    curses.init_color(32, 749, 800, 862)  # Polar Ice
    curses.init_color(33, 500, 560, 650)  # Slate Gray
    curses.init_color(34, 1000, 580, 580)  # Muted Coral

    # Color IDs 35-39
    curses.init_color(35, 1000, 796, 568)  # Peach
    curses.init_color(36, 1000, 435, 380)  # Salmon
    curses.init_color(37, 1000, 900, 400)  # Gold
    curses.init_color(38, 568, 321, 568)  # Dusty Rose
    curses.init_color(39, 400, 200, 400)  # Deep Plum

    # Color IDs 40-44
    curses.init_color(40, 900, 900, 900)  # Near White
    curses.init_color(41, 600, 600, 600)  # Silver
    curses.init_color(42, 400, 400, 400)  # Steel
    curses.init_color(43, 250, 250, 250)  # Charcoal
    curses.init_color(44, 1000, 200, 0)  # Alert Red

    for i in range(25):
        # pair_id, foreground_color_id, background_id
        curses.init_pair(i + 1, 20 + i, 10)

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

    sections: List[str] = [
        "Generate",
        "Play",
        "Show/Hide",
        "Change colours",
        "Exit",
    ]

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
                            pdeb("Move Up")

                            player.move(PlayerDirection.UP, maze.get_cells())
                            rendrer.render_player(player, last_player_pos)

                        elif player_key == curses.KEY_DOWN:
                            pdeb("Move Down")
                            player.move(PlayerDirection.DOWN, maze.get_cells())
                            rendrer.render_player(player, last_player_pos)

                        elif player_key == curses.KEY_LEFT:
                            pdeb("Move Left")
                            player.move(PlayerDirection.LEFT, maze.get_cells())
                            rendrer.render_player(player, last_player_pos)

                        elif player_key == curses.KEY_RIGHT:
                            pdeb("Move Right")
                            player.move(PlayerDirection.RIGHT, maze.get_cells())
                            rendrer.render_player(player, last_player_pos)

                        if (player.y, player.x) == config.exit:
                            pdeb("Player reached the exit!")
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
                        current_color_id = choice([20, 25, 30, 35, 40])
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)

                # Exit
                case exit_index:
                    break

        # player logic

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
        pdeb(f"[Arguments error]: {e}")
        exit(1)

    # try:
    wrapper(main)
    # except KeyboardInterrupt:
    #     print("Exit the program")
    # except curses.error as e:
    #     print(f"[Curses error]: {e}")
    # except BaseException as e:
    #     print(f"[Error]: {e}")
