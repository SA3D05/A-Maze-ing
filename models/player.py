from enum import Enum
from typing import List
from deb import pdeb
from models.cell import Cell


class PlayerDirection(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Player:
    def __init__(self, y: int, x: int, y_shift: int, x_shift: int, shape: str) -> None:
        self.y = y
        self.x = x
        self.y_shift = y_shift
        self.x_shift = x_shift
        self.shape = shape

    def move(self, direction: PlayerDirection, maze_cells: List[Cell]) -> None:

        pdeb(f"Player position before move: ({self.y}, {self.x})")
        for cell in maze_cells:
            if (cell.y, cell.x) == (self.y, self.x):
                if not cell.left and direction == PlayerDirection.LEFT:
                    self.x -= 1
                    return
                elif not cell.right and direction == PlayerDirection.RIGHT:
                    self.x += 1
                    return

                elif not cell.up and direction == PlayerDirection.UP:
                    self.y -= 1
                    return

                elif not cell.down and direction == PlayerDirection.DOWN:
                    self.y += 1
                    return
