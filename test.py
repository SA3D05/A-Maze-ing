import curses
import time


def main(stdscr: curses.window):
    stdscr.nodelay(True)  # non-blocking input
    stdscr.clear()
    curses.curs_set(0)
    x = 0
    while True:
        key = stdscr.getch()

        if key == ord("q"):
            break

        stdscr.clear()
        stdscr.addstr(0, x, "@")
        stdscr.refresh()

        x = (x + 1) % 20
        time.sleep(0.02)


curses.wrapper(main)
