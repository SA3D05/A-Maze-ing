from mazegen.cell import Cell

from enum import Enum
from typing import List


class PlayerDirection(Enum):
    """Enumeration of player movement directions.
    
    Attributes:
        UP: Move upward (value: 0).
        DOWN: Move downward (value: 1).
        LEFT: Move left (value: 2).
        RIGHT: Move right (value: 3).
    """
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Player:
    """Represents a player entity in the maze.
    
    Attributes:
        y (int): The row coordinate of the player.
        x (int): The column coordinate of the player.
        y_shift (int): Vertical offset for rendering the player.
        x_shift (int): Horizontal offset for rendering the player.
        shape (str): The character used to represent the player visually.
    """

    def __init__(self, y: int, x: int, y_shift: int, x_shift: int, shape: str) -> None:
        """Initialize a new Player instance.
        
        Args:
            y (int): The initial row coordinate.
            x (int): The initial column coordinate.
            y_shift (int): Vertical rendering offset.
            x_shift (int): Horizontal rendering offset.
            shape (str): The character to display for the player.
        """
        self.y: int = y
        self.x: int = x
        self.y_shift: int = y_shift
        self.x_shift: int = x_shift
        self.shape: str = shape

    def move(self, direction: PlayerDirection, maze_cells: List[Cell]) -> None:
        """Move the player in the specified direction if not blocked by a wall.
        
        Checks if there is an open path in the given direction and updates the
        player's position accordingly. Movement is constrained by maze walls.
        
        Args:
            direction (PlayerDirection): The direction to move (UP, DOWN, LEFT, RIGHT).
            maze_cells (List[Cell]): List of all cells in the maze used for validation.
        """
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
