from enum import Enum


class CellState(Enum):
    REGULAR = 0
    PATH = 1
    FT = 2
    ENTRY = 3
    EXIT = 4


class Cell:
    def __init__(
        self,
        y: int,
        x: int,
        up: bool,
        right: bool,
        down: bool,
        left: bool,
        state: CellState = CellState.PATH,
    ) -> None:
        self.y = y
        self.x = x
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.state = state
