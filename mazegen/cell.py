from enum import Enum


class CellState(Enum):
    """
    Enumeration of possible states for a cell in a maze.
    Attributes:
        REGULAR: A standard cell with no special designation.
        PATH: A cell that is part of the solution path through the maze.
        FT: A frontier cell (used during maze generation algorithm).
        ENTRY: The entry point to the maze.
        EXIT: The exit point from the maze.
    """

    regular = 0
    path = 1
    ft = 2
    entry = 3
    _exit = 4


class Cell:
    """Represents a single cell in a maze with walls on all four sides.
    Represents a single cell in a maze.
    Attributes:
        y (int): The row coordinate of the cell in the maze grid.
        x (int): The column coordinate of the cell in the maze grid.
        up (bool): Whether there is a wall on the top side of the cell.
        right (bool): Whether there is a wall on the right side of the cell.
        down (bool): Whether there is a wall on the bottom side of the cell.
        left (bool): Whether there is a wall on the left side of the cell.
        state (CellState):
        The current state of the cell (default: CellState.path).
    Args:
        x (int): The row coordinate of the cell.
        y (int): The column coordinate of the cell.
        up (bool): Indicates if the cell has a wall pointing upward.
        right (bool): Indicates if the cell has a wall pointing right.
        down (bool): Indicates if the cell has a wall pointing downward.
        left (bool): Indicates if the cell has a wall pointing left.
        state (CellState):
        The initial state of the cell. Defaults to CellState.path.
    """

    def __init__(
        self,
        y: int,
        x: int,
        up: bool,
        right: bool,
        down: bool,
        left: bool,
        state: CellState = CellState.path,
    ) -> None:
        """Initialize a Cell with position, walls, and state.
        Args:
            y (int): The row coordinate of the cell.
            x (int): The column coordinate of the cell.
            up (bool): Whether there is a wall on the top side.
            right (bool): Whether there is a wall on the right side.
            down (bool): Whether there is a wall on the bottom side.
            left (bool): Whether there is a wall on the left side.
            state (CellState): The state of the cell.
            Defaults to CellState.path.
        """
        self.y: int = y
        self.x: int = x
        self.up: bool = up
        self.right: bool = right
        self.down: bool = down
        self.left: bool = left
        self.state: CellState = state
