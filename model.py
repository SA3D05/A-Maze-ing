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
