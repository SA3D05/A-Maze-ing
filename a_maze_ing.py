import curses
from curses import wrapper
from cells_place_holder import MazeGenerator
from utils import Maze
from gen_path import dijkstra


config = {}
try:
    with open("config.txt", "r") as fd:
        for line in fd:
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                config[key.strip().upper()] = value.strip()
        WIDTH = int(config.get("WIDTH", 10))
        HEIGHT = int(config.get("HEIGHT", 10))
        is_perfect_str = config.get("PERFECT", "TRUE").strip().upper()
        is_perfect = (is_perfect_str == "TRUE")
except (FileNotFoundError, PermissionError, KeyError, ValueError) as e:
    print(f"[Error loading], using default config {e}")
    WIDTH = 10
    HEIGHT = 10
    is_perfect = True


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
            print(f"[Warning]: {key} {x},{y} is out of bounds. Using default.")
            return (default_x, default_y)

    except (ValueError, IndexError):
        print(f"[Warning]: {key} has invalid format in config. Using default.")
        return (default_x, default_y)


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

    # Initialize the visual Maze utility with dynamic logic
    maze: Maze = Maze(
        generator.generate(make_perfect=is_perfect),
        HEIGHT, WIDTH,
        int((term_width / 2) - (WIDTH / 2)),
        int((term_height / 2) - (HEIGHT / 2)),
    )

    def redraw():
        maze.gen_grid()
        maze.brake_walls()
        maze.handel_corners()
        render_elements(stdscr, maze.get_elements())

    path = dijkstra(generator.grid, entry, exit)
    if path:
        for (px, py) in path:
            generator.grid[py][px].is_path = True

    redraw()

    while True:
        key = stdscr.getch()

        # Exit on 'q' or 'Enter' as requested
        if key == ord('q') or key == ord('\n'):
            break
        # Regenerate on 'r'
        elif key == ord('r'):
            stdscr.clear()
            maze.cells = generator.generate(make_perfect=is_perfect)
            redraw()

    # path = dijkstra(generator.grid, entry, exit)
    # if path:
    #     for (px, py) in path:
    #         generator.grid[py][px].is_path = True


if __name__ == "__main__":
    wrapper(main)
