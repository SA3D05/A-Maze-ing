import curses
from curses import wrapper
from cells_place_holder import MazeGenerator
from utils import Maze

config = {}
try:
    with open("config.txt", "r") as fd:
        for line in fd:
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                config[key.strip().upper()] = value.strip()
        WIDTH = int(config.get("WIDTH", 10))
        HEIGHT = int(config.get("HEIGHT", 10))
except (FileNotFoundError, PermissionError, KeyError, ValueError) as e:
    print(f"[Error loading], using default config {e}")
    WIDTH = 10
    HEIGHT = 10


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
        generator.generate(),
        HEIGHT, WIDTH,
        int((term_width / 2) - (WIDTH / 2)),
        int((term_height / 2) - (HEIGHT / 2)),
    )

    def redraw():
        maze.gen_grid()
        maze.brake_walls()
        maze.handel_corners()
        render_elements(stdscr, maze.get_elements())

    redraw()

    while True:
        key = stdscr.getch()

        # Exit on 'q' or 'Enter' as requested
        if key == ord('q') or key == ord('\n'):
            break
        # Regenerate on 'r'
        elif key == ord('r'):
            stdscr.clear()
            maze.cells = generator.generate()
            redraw()


if __name__ == "__main__":
    wrapper(main)
