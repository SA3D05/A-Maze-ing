class Cell:
    def __init__(
        self,
        y: int,
        x: int,
        up: bool,
        right: bool,
        down: bool,
        left: bool,
        is_in_42: bool = False,
    ) -> None:
        self.y = y
        self.x = x
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.is_in_42 = is_in_42
