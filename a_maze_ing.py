import curses

from curses import wrapper


class Cell:
    def __init__(
        self, y: int, x: int, up: bool, down: bool, left: bool, right: bool
    ) -> None:
        self.y = y
        self.x = x
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
    Cell(0, 0, False, True, False, False),
    Cell(0, 1, False, True, False, True),
    Cell(0, 2, False, True, True, False),
    Cell(1, 0, True, False, False, True),
    Cell(1, 1, True, True, True, False),
    Cell(1, 2, True, False, False, False),
    Cell(2, 0, False, False, False, True),
    Cell(2, 1, True, False, True, True),
    Cell(2, 2, False, False, True, False),
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


WIDTH = 3
HEIGHT = 3


def get_pos(pos) -> int:

    result: int = (pos * 2) + 1
    return result


def get_cell(x, y):
    for c in maze:
        if c.x == x and c.y == y:
            return c
    return None


def main(scr: curses.window) -> None:
    xmax = WIDTH - 1
    ymax = HEIGHT - 1
    curses.curs_set(0)
    scr.clear()
    scr.refresh()
    for cell in maze:
        if not cell.up:
            scr.addch(get_pos(cell.y) - 1, get_pos(cell.x), TILES["horizontal"])

        if not cell.down:
            scr.addch(get_pos(cell.y) + 1, get_pos(cell.x), TILES["horizontal"])

        if not cell.left:
            scr.addch(get_pos(cell.y), get_pos(cell.x) - 1, TILES["vertical"])

        if not cell.right:
            scr.addch(get_pos(cell.y), get_pos(cell.x) + 1, TILES["vertical"])
    for cell in maze:
        if cell.x == 0 and cell.y == 0:
            scr.addch(get_pos(cell.y) - 1, get_pos(cell.x) - 1, TILES["left-top"])
        if cell.x == xmax and cell.y == 0:
            scr.addch(get_pos(cell.y) - 1, get_pos(cell.x) + 1, TILES["right-top"])
        if cell.x == 0 and cell.y == ymax:
            scr.addch(get_pos(cell.y) + 1, get_pos(cell.x) - 1, TILES["left-bottom"])
        if cell.x == xmax and cell.y == ymax:
            scr.addch(get_pos(cell.y) + 1, get_pos(cell.x) + 1, TILES["right-bottom"])
    scr.refresh()
    scr.getch()


wrapper(main)
