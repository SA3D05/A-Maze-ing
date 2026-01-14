from time import sleep as s
import curses
import sys
import random


from curses import wrapper


class Cell:
    def __init__(
        self, x: int, y: int, up: bool, down: bool, left: bool, right: bool
    ) -> None:
        self.x = x
        self.y = y
        self.up = up
        self.down = down
        self.left = left
        self.right = right


TILES = {
    "vertical": "┃",
    "horizontal": "━",
    "left-top": "┏",
    "right-top": "┓",
    "left-bottom": "┗",
    "right-bottom": "┛",
    "center": "╋",
    "t-down": "┳",
    "t-up": "┻",
    "t-right": "┣",
    "t-left": "┫",
}


maze: list[Cell] = [
    # Row 0
    Cell(0, 0, False, True, False, False),  # Start: Can only go Down
    Cell(1, 0, False, False, False, True),  # Path: Can only go Right
    Cell(2, 0, False, True, True, True),  # Junction
    Cell(3, 0, False, False, True, True),  # Path
    Cell(4, 0, False, True, True, False),  # Corner
    # Row 1
    Cell(0, 1, True, True, False, False),  # Path
    Cell(1, 1, False, True, False, False),  # Dead end
    Cell(2, 1, True, True, False, False),  # Path
    Cell(3, 1, False, True, False, False),  # Path
    Cell(4, 1, True, False, False, False),  # Path
    # Row 2 (The "42" pattern often starts around here)
    Cell(0, 2, True, False, False, True),  # Path
    Cell(1, 2, True, True, True, False),  # Junction
    Cell(2, 2, True, False, False, True),  # Path
    Cell(3, 2, True, True, True, False),  # Path
    Cell(4, 2, False, True, False, False),  # Path
    # Row 3
    Cell(0, 3, False, True, False, True),  # Path
    Cell(1, 3, True, False, True, False),  # Path
    Cell(2, 3, False, True, False, True),  # Path
    Cell(3, 3, True, True, True, True),  # 4-Way Junction
    Cell(4, 3, True, False, True, False),  # Path
    # Row 4
    Cell(0, 4, True, False, False, True),  # Corner
    Cell(1, 4, False, False, True, True),  # Path
    Cell(2, 4, True, False, True, False),  # Path
    Cell(3, 4, True, False, False, True),  # Path
    Cell(4, 4, False, False, True, False),  # Exit: Path from Left
]


def gen_maze(scr: curses.window, xmax: int, ymax: int):
    for y in range(HEIGHT * 2 + 1):
        for x in range(WIDTH * 2 + 1):
            if x == 0 and y == 0:
                scr.addch(y, x, TILES["left-top"])
            elif x == xmax and y == 0:
                scr.addch(y, x, TILES["right-top"])
            elif x == 0 and y == ymax:
                scr.addch(y, x, TILES["left-bottom"])
            elif x == xmax and y == ymax:
                scr.addch(y, x, TILES["right-bottom"])

            elif y == 0:
                if x % 2 == 0:
                    scr.addch(y, x, TILES["t-down"])
                else:
                    scr.addch(y, x, TILES["horizontal"])
            elif y == ymax:
                if x % 2 == 0:
                    scr.addch(y, x, TILES["t-up"])
                else:
                    scr.addch(y, x, TILES["horizontal"])

            elif x == 0:
                if y % 2 == 0:
                    scr.addch(y, x, TILES["t-right"])
                else:
                    scr.addch(y, x, TILES["vertical"])

            elif x == xmax:
                if y % 2 == 0:
                    scr.addch(y, x, TILES["t-left"])
                else:
                    scr.addch(y, x, TILES["vertical"])

            elif x % 2 == 0:
                if y % 2 == 0:
                    scr.addch(y, x, TILES["center"])
                else:
                    scr.addch(y, x, TILES["vertical"])
            elif y % 2 == 0:
                scr.addch(y, x, TILES["horizontal"])


WIDTH = 5
HEIGHT = 5


def get_pos(pos) -> int:

    result: int = (pos * 2) + 1
    return result


class Player:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


def main(scr: curses.window) -> None:
    p = Player(1, 1)
    scr.keypad(True)
    xmax = WIDTH * 2 + 1
    ymax = HEIGHT * 2 + 1

    curses.curs_set(0)
    scr.clear()
    scr.refresh()
    for cell in maze:
        if cell.up is False:
            scr.addch(get_pos(cell.y) - 1, get_pos(cell.x), TILES["horizontal"])

        if cell.down is False:
            scr.addch(get_pos(cell.y) + 1, get_pos(cell.x), TILES["horizontal"])

        if cell.left is False:
            scr.addch(get_pos(cell.y), get_pos(cell.x) - 1, TILES["vertical"])

        if cell.right is False:
            scr.addch(get_pos(cell.y), get_pos(cell.x) + 1, TILES["vertical"])

        scr.addch((cell.y * 2) + 1, (cell.x * 2) + 1, " ")

    while True:

        key = scr.getch()

        if key == ord("q"):
            break
        elif key == curses.KEY_UP:
            p.y -= 1
        elif key == curses.KEY_DOWN:
            p.y += 1
        elif key == curses.KEY_LEFT:
            p.x -= 1
        elif key == curses.KEY_RIGHT:
            p.x += 1
        for y in range(ymax):
            for x in range(xmax):
                if p.x == x and p.y == y:
                    scr.addch(y, x, "o")
                elif x == 0 and y == 0:
                    scr.addch(y, x, TILES["left-top"])
                elif x == xmax - 1 and y == 0:
                    scr.addch(y, x, TILES["right-top"])
                elif x == 0 and y == ymax - 1:
                    scr.addch(y, x, TILES["left-bottom"])
                elif x == xmax - 1 and y == ymax - 1:
                    scr.addch(y, x, TILES["right-bottom"])
                elif y == 0:
                    scr.addch(y, x, TILES["horizontal"])
                elif x == 0:
                    scr.addch(y, x, TILES["vertical"])
                elif x == xmax - 1:
                    scr.addch(y, x, TILES["vertical"])
                elif y == ymax - 1:
                    scr.addch(y, x, TILES["horizontal"])
        scr.refresh()


wrapper(main)
