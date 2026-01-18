import curses
import time

from curses import wrapper
import sys


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


WIDTH = int(sys.argv[1])
HEIGHT = int(sys.argv[2])


class Element:
    def __init__(self, y, x, sprite):
        self.y = y
        self.x = x
        self.sprite = sprite


elements: list[Element] = []

for column in range(HEIGHT * 2 + 1):
    for row in range(WIDTH * 2 + 1):

        if column == 0 and row == 0:
            elements.append(Element(column, row, TILES["left-top"]))
        elif column == 0 and row == WIDTH * 2:
            elements.append(Element(column, row, TILES["right-top"]))
        elif column == HEIGHT * 2 and row == 0:
            elements.append(Element(column, row, TILES["left-bottom"]))
        elif column == HEIGHT * 2 and row == WIDTH * 2:
            elements.append(Element(column, row, TILES["right-bottom"]))

        elif not row % 2 and column == 0:
            elements.append(Element(column, row, TILES["t-down"]))
        elif not row % 2 and column == HEIGHT * 2:
            elements.append(Element(column, row, TILES["t-up"]))
        elif not column % 2:
            if row == 0:
                elements.append(Element(column, row, TILES["t-right"]))
            elif row == WIDTH * 2:
                elements.append(Element(column, row, TILES["t-left"]))
            elif not row % 2:
                elements.append(Element(column, row, TILES["center"]))
            else:
                elements.append(Element(column, row, TILES["horizontal"]))
        elif column % 2 and not row % 2:
            elements.append(Element(column, row, TILES["vertical"]))
        else:
            elements.append(Element(column, row, " "))


def get_pos(pos) -> int:

    result: int = (pos * 2) + 1
    return result


def get_cell(x, y):
    for c in maze:
        if c.x == x and c.y == y:
            return c
    return None


def main(scr: curses.window) -> None:
    curses.curs_set(0)
    scr.clear()
    scr.refresh()
    for element in elements:
        scr.addch(element.y, element.x, element.sprite)

        for cell in maze:
            # left corner

            for element in elements:
                if element.x == get_pos(cell.x) - 1:
                    if element.y == get_pos(cell.y) - 1:
                        if element.sprite == TILES["center"]:
                            scr.addch(
                                get_pos(cell.y) - 1,
                                get_pos(cell.x) - 1,
                                " ",
                            )
                        if element.sprite == TILES["t-right"]:
                            scr.addch(
                                get_pos(cell.y) - 1,
                                get_pos(cell.x) - 1,
                                TILES["vertical"],
                            )

                # right corner

            if cell.down:
                scr.addch(get_pos(cell.y) + 1, get_pos(cell.x), " ")

            if cell.left:
                scr.addch(get_pos(cell.y), get_pos(cell.x) - 1, " ")

            if cell.right:
                scr.addch(get_pos(cell.y), get_pos(cell.x) + 1, " ")

    # for cell in maze:
    #     if cell.x == 0 and cell.y == 0:
    #         scr.addch(get_pos(cell.y) - 1, get_pos(cell.x) - 1, TILES["left-top"])
    #     if cell.x == xmax and cell.y == 0:
    #         scr.addch(get_pos(cell.y) - 1, get_pos(cell.x) + 1, TILES["right-top"])
    #     if cell.x == 0 and cell.y == ymax:
    #         scr.addch(get_pos(cell.y) + 1, get_pos(cell.x) - 1, TILES["left-bottom"])
    #     if cell.x == xmax and cell.y == ymax:
    #         scr.addch(get_pos(cell.y) + 1, get_pos(cell.x) + 1, TILES["right-bottom"])

    scr.refresh()
    # scr.getch()
    while True:
        time.sleep(10)


wrapper(main)
