import curses
import time

from curses import wrapper
import sys
from cells_place_holder import maze
from model import Cell, Element
from tiles import Tile


def gen_maze(scr: curses.window, xmax: int, ymax: int):
    for y in range(HEIGHT * 2 + 1):
        for x in range(WIDTH * 2 + 1):
            if x == 0 and y == 0:
                scr.addch(y, x, Tile.LEFT_TOP.value)
            elif x == xmax and y == 0:
                scr.addch(y, x, Tile.RIGHT_TOP.value)
            elif x == 0 and y == ymax:
                scr.addch(y, x, Tile.LEFT_BOTTOM.value)
            elif x == xmax and y == ymax:
                scr.addch(y, x, Tile.RIGHT_BOTTOM.value)

            elif y == 0:
                if x % 2 == 0:
                    scr.addch(y, x, Tile.T_DOWN.value)
                else:
                    scr.addch(y, x, Tile.HORIZONTAL.value)
            elif y == ymax:
                if x % 2 == 0:
                    scr.addch(y, x, Tile.T_UP.value)
                else:
                    scr.addch(y, x, Tile.HORIZONTAL.value)

            elif x == 0:
                if y % 2 == 0:
                    scr.addch(y, x, Tile.T_RIGHT.value)
                else:
                    scr.addch(y, x, Tile.VERTICAL.value)

            elif x == xmax:
                if y % 2 == 0:
                    scr.addch(y, x, Tile.T_LEFT.value)
                else:
                    scr.addch(y, x, Tile.VERTICAL.value)

            elif x % 2 == 0:
                if y % 2 == 0:
                    scr.addch(y, x, Tile.CENTER.value)
                else:
                    scr.addch(y, x, Tile.VERTICAL.value)
            elif y % 2 == 0:
                scr.addch(y, x, Tile.HORIZONTAL.value)


WIDTH = int(sys.argv[1])
HEIGHT = int(sys.argv[2])


elements: list[Element] = []

for column in range(HEIGHT * 2 + 1):
    for row in range(WIDTH * 2 + 1):

        if column == 0 and row == 0:
            elements.append(Element(column, row, Tile.LEFT_TOP.value))
        elif column == 0 and row == WIDTH * 2:
            elements.append(Element(column, row, Tile.RIGHT_TOP.value))
        elif column == HEIGHT * 2 and row == 0:
            elements.append(Element(column, row, Tile.LEFT_BOTTOM.value))
        elif column == HEIGHT * 2 and row == WIDTH * 2:
            elements.append(Element(column, row, Tile.RIGHT_BOTTOM.value))

        elif not row % 2 and column == 0:
            elements.append(Element(column, row, Tile.T_DOWN.value))
        elif not row % 2 and column == HEIGHT * 2:
            elements.append(Element(column, row, Tile.T_UP.value))
        elif not column % 2:
            if row == 0:
                elements.append(Element(column, row, Tile.T_RIGHT.value))
            elif row == WIDTH * 2:
                elements.append(Element(column, row, Tile.T_LEFT.value))
            elif not row % 2:
                elements.append(Element(column, row, Tile.CENTER.value))
            else:
                elements.append(Element(column, row, Tile.HORIZONTAL.value))
        elif column % 2 and not row % 2:
            elements.append(Element(column, row, Tile.VERTICAL.value))
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


def get_up_element(element: Element):
    for el in elements:
        if el.x == element.x and el.y == element.y - 1:
            return el.sprite
    return None


def get_down_element(element: Element):
    for el in elements:
        if el.x == element.x and el.y == element.y + 1:
            return el.sprite
    return None


def get_left_element(element: Element):
    for el in elements:
        if el.x == element.x - 1 and el.y == element.y:
            return el.sprite
    return None


def get_right_element(element: Element):
    for el in elements:
        if el.x == element.x + 1 and el.y == element.y:
            return el.sprite
    return None


def handel_center(element: Element):
    up = 1 if get_up_element(element) != " " else 0
    down = 2 if get_down_element(element) != " " else 0
    left = 4 if get_left_element(element) != " " else 0
    right = 8 if get_right_element(element) != " " else 0

    score = up + down + left + right

    BIT_MAP = {
        1: Tile.SHORT_UP.value,
        2: Tile.SHORT_DOWN.value,
        3: Tile.VERTICAL.value,
        4: Tile.SHORT_LEFT.value,
        5: Tile.RIGHT_BOTTOM.value,
        6: Tile.RIGHT_TOP.value,
        7: Tile.T_LEFT.value,
        8: Tile.SHORT_RIGHT.value,
        9: Tile.LEFT_BOTTOM.value,
        10: Tile.LEFT_TOP.value,
        11: Tile.T_RIGHT.value,
        12: Tile.HORIZONTAL.value,
        13: Tile.T_UP.value,
        14: Tile.T_DOWN.value,
        15: Tile.CENTER.value,
    }

    element.sprite = BIT_MAP.get(score, " ")


def main(scr: curses.window) -> None:
    curses.curs_set(0)
    scr.clear()
    scr.refresh()
    for element in elements:
        scr.addch(element.y, element.x, element.sprite)
        scr.refresh()

    for cell in maze:
        for element in elements:

            if element.x == get_pos(cell.x) and element.y == get_pos(cell.y) - 1:
                if cell.up:
                    element.sprite = " "

            if element.x == get_pos(cell.x) + 1 and element.y == get_pos(cell.y):
                if cell.right:
                    element.sprite = " "

            if element.x == get_pos(cell.x) and element.y == get_pos(cell.y) + 1:
                if cell.down:
                    element.sprite = " "

            if element.x == get_pos(cell.x) - 1 and element.y == get_pos(cell.y):
                if cell.left:
                    element.sprite = " "

    for element in elements:
        if element.sprite == Tile.CENTER.value:
            handel_center(element)
        elif element.sprite == Tile.T_DOWN.value:
            if get_down_element(element) == " ":
                element.sprite = Tile.HORIZONTAL.value

        elif element.sprite == Tile.T_UP.value:
            if get_up_element(element) == " ":
                element.sprite = Tile.HORIZONTAL.value

        elif element.sprite == Tile.T_LEFT.value:
            if get_left_element(element) == " ":
                element.sprite = Tile.VERTICAL.value

        elif element.sprite == Tile.T_RIGHT.value:
            if get_right_element(element) == " ":
                element.sprite = Tile.VERTICAL.value

    for element in elements:
        scr.addch(element.y, element.x, element.sprite)
    scr.refresh()
    # scr.getch()
    time.sleep(1000)


wrapper(main)
