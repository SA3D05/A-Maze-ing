from enum import Enum


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


class Element:
    def __init__(
        self,
        y: int,
        x: int,
        sprite: str,
    ):
        self.y = y
        self.x = x
        self.sprite = sprite


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
