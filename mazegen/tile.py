from enum import Enum


class Tile(Enum):
    """Enumeration of tile characters used for rendering maze elements.
    
    Attributes:
        VERTICAL: Vertical line character.
        HORIZONTAL: Horizontal line character.
        LEFT_TOP: Top-left corner character.
        RIGHT_TOP: Top-right corner character.
        LEFT_BOTTOM: Bottom-left corner character.
        RIGHT_BOTTOM: Bottom-right corner character.
        CENTER: Center junction character.
        T_DOWN: T-junction pointing down.
        T_UP: T-junction pointing up.
        T_RIGHT: T-junction pointing right.
        T_LEFT: T-junction pointing left.
        SHORT_UP: Space for up direction.
        SHORT_DOWN: Space for down direction.
        SHORT_LEFT: Space for left direction.
        SHORT_RIGHT: Space for right direction.
        BLOCK: Solid block character.
        ENTER: Entry point marker.
        EXIT: Exit point marker.
        PATH: Solution path marker.
        SPACE: Empty space character.
    """

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
