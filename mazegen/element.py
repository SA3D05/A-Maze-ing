class Element:
    """Represents a renderable visual element in the maze.
    Represents an element in a maze with positional and visual attributes.
    Attributes:
        y (int): The y-coordinate (row) position of the element.
        x (int): The x-coordinate (column) position of the element.
        shape (str): The character or string representation of the element's visual appearance.
    """

    def __init__(
        self,
        y: int,
        x: int,
        shape: str,
    ):
        """Initialize an Element at a specific position with a visual shape.
        
        Args:
            y (int): The y-coordinate (row) position.
            x (int): The x-coordinate (column) position.
            shape (str): The character or string representation of the element.
        """
        self.y: int = y
        self.x: int = x
        self.shape: str = shape
