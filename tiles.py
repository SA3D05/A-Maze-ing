from enum import Enum


class Tile(Enum):
    VERTICAL = "│"
    HORIZONTAL = "─"

    # Corners
    LEFT_TOP = "╭"
    RIGHT_TOP = "╮"
    LEFT_BOTTOM = "╰"
    RIGHT_BOTTOM = "╯"

    # Junctions
    CENTER = "┼"
    T_DOWN = "┬"
    T_UP = "┴"
    T_RIGHT = "├"
    T_LEFT = "┤"

    # Short Ends
    SHORT_UP = "╵"
    SHORT_DOWN = "╷"
    SHORT_LEFT = "╴"
    SHORT_RIGHT = "╶"
