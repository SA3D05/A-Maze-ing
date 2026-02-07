import curses
from curses import wrapper
from cells_place_holder import MazeGenerator
from utils import Maze
from gen_path import dijkstra
import random
from file_manager import save_maze
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.txt")

config = {}
try:
    with open(CONFIG_PATH, "r") as fd:
        for line in fd:
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                config[key.strip().upper()] = value.strip()

        WIDTH = int(config.get("WIDTH", 10))
        HEIGHT = int(config.get("HEIGHT", 10))

        is_perfect_str = config.get("PERFECT", "TRUE").strip().upper()
        is_perfect = (is_perfect_str == "TRUE")

        raw_seed = config.get("SEED")

        if raw_seed and raw_seed.strip():
            random.seed(raw_seed)
            current_seed = raw_seed
        else:
            random.seed(None)
            current_seed = "Random/System Time"

except (FileNotFoundError, PermissionError, KeyError, ValueError) as e:
    print(f"[Error loading], using default config {e}")
    is_perfect = True
    exit(1)

print(f"Configuration Loaded: {WIDTH}x{HEIGHT} (Seed: {current_seed})")


def get_safe_coords(key, default_x, default_y, max_w, max_h):
    raw_val = config.get(key)
    if not raw_val:
        return (default_x, default_y)

    try:
        # Split "0,0" into [0, 0]
        parts = raw_val.split(',')
        if len(parts) != 2:
            raise ValueError

        x, y = int(parts[0].strip()), int(parts[1].strip())

        # Check if within maze bounds
        if 0 <= x < max_w and 0 <= y < max_h:
            return (x, y)
        else:
            raise ValueError

    except (ValueError, IndexError):
        print(f"[Warning]: {key} {x},{y} has invalid format in config.txt")
        exit(1)


entry = get_safe_coords("ENTRY", 0, 0, WIDTH, HEIGHT)
exit = get_safe_coords("EXIT", WIDTH - 1, HEIGHT - 1, WIDTH, HEIGHT)


def render_elements(stdscr, elements):
    """Draws the maze sprites to the terminal screen."""

    for element in elements:
        try:
            stdscr.addch(element.y, element.x, element.sprite)
        except curses.error:
            pass
    stdscr.refresh()


def main(stdscr: curses.window) -> None:
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.clear()

    term_height, term_width = stdscr.getmaxyx()
    generator = MazeGenerator(WIDTH, HEIGHT)

    # Initialize with cells, entry, and exit
    maze_cells = generator.generate(make_perfect=is_perfect)
    maze: Maze = Maze(
        maze_cells,
        HEIGHT, WIDTH,
        entry, exit,  # Pass these to the renderer
        int((term_width / 2) - (WIDTH / 2)),
        int((term_height / 2) - (HEIGHT / 2)),
    )

    def update_and_draw():
        # Reset path flags for all cells
        for row in generator.grid:
            for cell in row:
                cell.is_path = False

        # Calculate new path
        path = dijkstra(generator.grid, entry, exit)
        if path:
            for (px, py) in path:
                generator.grid[py][px].is_path = True

            save_maze(generator.grid, WIDTH, HEIGHT, entry, exit, path, "maze.txt")
        maze.gen_grid()
        maze.brake_walls()
        maze.handel_corners()
        render_elements(stdscr, maze.get_elements())

    update_and_draw()

    while True:
        key = stdscr.getch()
        if key == ord('q') or key == ord('\n'):
            break
        elif key == ord('r'):
            stdscr.clear()
            maze.cells = generator.generate(make_perfect=is_perfect)
            update_and_draw()


def main_wrapper():
    """Entry point from the console script"""
    wrapper(main)


if __name__ == "__main__":
    main_wrapper()
