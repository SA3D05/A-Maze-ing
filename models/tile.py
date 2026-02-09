from enum import Enum


class Tile(Enum):

    VERTICAL = "║"
    HORIZONTAL = "═"

    LEFT_TOP = "╔"
    RIGHT_TOP = "╗"
    LEFT_BOTTOM = "╚"
    RIGHT_BOTTOM = "╝"

    CENTER = "╬"
    T_DOWN = "╦"
    T_UP = "╩"
    T_RIGHT = "╠"
    T_LEFT = "╣"

    SHORT_UP = " "
    SHORT_DOWN = " "
    SHORT_LEFT = " "
    SHORT_RIGHT = " "

    BLOCK = "█"
    ENTER = "E"
    EXIT = "X"
    PATH = "*"
    SPACE = " "
