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

    # --- 2. Load Configuration ---
    config: MazeConfig = MazeConfig()
    try:
        # Use the 'parse' method from your MazeConfig class
        config.parse(argv[1])
    except Exception:
        pass

    # --- 3. Dynamic UI Positioning ---
    term_height, term_width = stdscr.getmaxyx()
    maze_height = config.height * 2 + 1
    maze_width = config.width * 2 + 1

    # Center the maze on the screen
    maze_yshift = int((term_height / 2) - (maze_height / 2))
    maze_xshift = int((term_width / 2) - (maze_width / 2))
    
    # Position menu to the right of the maze
    menu_yshift = maze_yshift
    menu_xshift = maze_xshift + maze_width + 4

    # Sanity check for terminal size
    if maze_width + 30 > term_width or maze_height + 4 > term_height:
        raise Exception("Terminal size too small for this configuration!")

    # --- 4. Initialize Objects ---
    menu = Menu(menu_yshift, menu_xshift)
    rendrer = Rendrer(stdscr)
    generator = MazeGenerator(config)
    maze = Maze(maze_yshift, maze_xshift)

    sections = ["Generate", "With steps", "Play", "Show/Hide", "Change colours", "Exit"]
    for section in sections:
        menu.add_section(section)
    
    current_color_id = 1
    show_hide = False
    duration = 0.001

    rendrer.render_menu(menu)
    generator.gen_grid(maze) # Initial grid setup
    rendrer.render_maze(maze, duration, current_color_id, show_hide)

    # --- 5. Main Interaction Loop ---
    while True:
        key = stdscr.getch()
        
        if key == curses.KEY_RESIZE:
            continue
            
        elif key == ord("\n") or key == curses.KEY_ENTER:
            selected_idx = menu.get_selected_index()
            
            # CASE 0 & 1: GENERATION
            if selected_idx == 0 or selected_idx == 1:
                rendrer.erase_maze(maze)
                # RESET MAZE: This ensures old path elements are cleared
                maze = Maze(maze_yshift, maze_xshift)
                
                # A. Generate the logic and Dijkstra path
                generator.generate(maze, config.is_perfect)
                
                # B. Map logic to visual characters (including PATH '*')
                generator.gen_grid(maze)
                
                if selected_idx == 0: # Fast Generate
                    generator.brake_walls(maze)
                    generator.handel_corners(maze.get_elements())
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)
                else: # With steps
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)
                    generator.brake_walls(maze)
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)
                    generator.handel_corners(maze.get_elements())
                    rendrer.render_maze(maze, duration, current_color_id, show_hide)

            # CASE 2: PLAY MODE
            elif selected_idx == 2:
                old_show_hide = show_hide
                show_hide = False
                player = Player(*config.entry, maze.y_shift, maze.x_shift, "@")
                rendrer.render_maze(maze, duration, current_color_id, show_hide)
                rendrer.render_player(player)
                
                while True:
                    last_pos = (player.y, player.x)
                    p_key = stdscr.getch()
                    if p_key == ord("q") or p_key == ord("Q"): break

                    move_dir = None
                    if p_key == curses.KEY_UP: move_dir = PlayerDirection.UP
                    elif p_key == curses.KEY_DOWN: move_dir = PlayerDirection.DOWN
                    elif p_key == curses.KEY_LEFT: move_dir = PlayerDirection.LEFT
                    elif p_key == curses.KEY_RIGHT: move_dir = PlayerDirection.RIGHT

                    if move_dir:
                        player.move(move_dir, maze.get_cells())
                        rendrer.render_player(player, last_pos)

                    if (player.y, player.x) == config.exit: break
                    curses.flushinp()

                show_hide = old_show_hide
                rendrer.render_maze(maze, duration, current_color_id, show_hide)

            # CASE 3: SHOW/HIDE SOLUTION
            elif selected_idx == 3:
                show_hide = not show_hide
                rendrer.render_maze(maze, 0, current_color_id, show_hide)

            # CASE 4: CHANGE COLOR
            elif selected_idx == 4:
                current_color_id = choice([1, 6, 11, 16, 21])
                rendrer.render_maze(maze, 0, current_color_id, show_hide)

            # CASE 5: EXIT
            elif selected_idx == 5:
                break

        elif key == curses.KEY_DOWN:
            menu.move_down()
            rendrer.render_menu(menu)
        elif key == curses.KEY_UP:
            menu.move_up()
            rendrer.render_menu(menu)
            
        curses.flushinp()

if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        exit(1)
    wrapper(main)