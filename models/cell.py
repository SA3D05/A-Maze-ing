from .cell_state import CellState


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
