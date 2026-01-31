import curses
from curses import wrapper
from sys import argv
from cells_place_holder import MazeGenerator
from utils import Maze

if len(argv) < 3:
    print("Usage: python3 a_maze_ing.py <width> <height>")
    exit(1)

WIDTH, HEIGHT = int(argv[1]), int(argv[2])


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
        int((term_width / 2) - WIDTH),
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
