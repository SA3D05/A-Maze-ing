import sys
from .element import Element
from .cell import Cell

from typing import Dict, List, Optional, Tuple
from random import seed as set_random_seed


class MazeConfig:
    """
    Configuration manager for maze generation.
    This class handles parsing and storing maze configuration parameters from a file.
    It validates dimensions, handles entry/exit points, and manages random seed settings.
    Attributes:
        height (int): The height of the maze in cells. Minimum value is 7.
        width (int): The width of the maze in cells. Minimum value is 9.
        entry (Tuple[int, int]): The (y, x) coordinates of the maze entry point.
        exit (Tuple[int, int]): The (y, x) coordinates of the maze exit point.
        output (str): The output file path for the generated maze. Defaults to "output.txt".
        is_perfect (bool): Whether the maze should be perfect (no loops). Defaults to True.
        seed_val (str): The random seed value. Defaults to "Random/System Time".
    """

    def __init__(
        self,
    ) -> None:
        """Initialize a MazeConfig with default values.
        
        Sets default configuration parameters that must be populated via parse().
        """
        self.height: int = 0
        self.width: int = 0
        self.entry: Tuple[int, int] = (-1, -1)
        self.exit: Tuple[int, int] = (-1, -1)
        self.output: str = "output.txt"
        self.is_perfect: bool = True
        self.seed_val: str = "Random/System Time"

    def parse(self, filename: str) -> None:
        """Parse maze configuration from a text file.
        
        Reads configuration parameters from a file with KEY=VALUE format.
        Validates dimensions and sets up random seed. Raises an exception if
        the maze dimensions are too small or entry/exit are invalid.
        
        Args:
            filename (str): Path to the configuration file.
            
        Raises:
            Exception: If maze dimensions are invalid or entry/exit are identical or out of bounds.
        """
        row_config: Dict[str, str] = {}
        with open(filename, "r") as fd:
            for line in fd:
                line = line.strip()
                # Skip empty lines or comments
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    row_config[key.strip().upper()] = value.strip()

        self.width = int(row_config.get("WIDTH", -1))
        self.height = int(row_config.get("HEIGHT", -1))

        if self.width < 9 or self.height < 7:
            raise Exception()

        perf_str = row_config.get("PERFECT", "TRUE").upper()
        self.is_perfect = perf_str == "TRUE"

        # --- SEED LOGIC ---
        raw_seed = row_config.get("SEED")
        if raw_seed:
            # If a seed exists in config, use it
            self.seed_val = raw_seed
            # We can set the seed here globally or pass it to generator
            set_random_seed(raw_seed)
        else:
            # If seed is missing or commented out, use system time (None)
            self.seed_val = "Random/System Time"
            set_random_seed(None)

        self.entry = self._get_safe_coords(row_config, "ENTRY", -1, -1)
        self.exit = self._get_safe_coords(row_config, "EXIT", -1, -1)

        if self.entry == self.exit or -1 in self.entry or -1 in self.exit:
            raise Exception()

    def _get_safe_coords(
        self, config_dict: Dict[str, str], key: str, def_x: int, def_y: int
    ) -> Tuple[int, int]:
        """Safely extract and validate coordinate values from config dictionary.
        
        Parses comma-separated coordinate strings and validates them against
        maze dimensions. Returns default values if parsing fails or coordinates
        are out of bounds.
        
        Args:
            config_dict (Dict[str, str]): Configuration dictionary to extract from.
            key (str): The configuration key to look up.
            def_x (int): Default x-coordinate if parsing fails.
            def_y (int): Default y-coordinate if parsing fails.
            
        Returns:
            Tuple[int, int]: A tuple of (y, x) coordinates (not (x, y)).
        """
        val: Optional[str] = config_dict.get(key)
        if not val:
            return (def_y, def_x)

        try:
            parts = val.split(",")
            y, x = int(parts[0].strip()), int(parts[1].strip())
            if 0 <= x < self.width and 0 <= y < self.height:
                return (y, x)
            raise ValueError
        except (ValueError, IndexError):
            return (def_y, def_x)


class Maze:
    """Represents a generated maze with elements and cells.
    
    This class stores the visual elements (renderable characters) and logical
    cells (maze structure) of a maze, along with positioning offsets for
    rendering on the terminal.
    
    Attributes:
        y_shift (int): Vertical offset for rendering the maze.
        x_shift (int): Horizontal offset for rendering the maze.
    """

    def __init__(self, y_shift: int, x_shift: int) -> None:
        """Initialize a Maze with positioning offsets.
        
        Args:
            y_shift (int): Vertical rendering offset.
            x_shift (int): Horizontal rendering offset.
        """
        self.y_shift = y_shift
        self.x_shift = x_shift

        self._elements: List[Element] = list()
        self._cells: List[Cell] = list()

    def add_element(self, element_y: int, element_x: int, element_shape: str) -> None:
        """Add a visual element to the maze.
        
        Args:
            element_y (int): Y-coordinate of the element.
            element_x (int): X-coordinate of the element.
            element_shape (str): Character representation of the element.
        """
        self._elements.append(Element(element_y, element_x, element_shape))

    def get_elements(self) -> List[Element]:
        """Get all visual elements of the maze.
        
        Returns:
            List[Element]: List of all elements in the maze.
        """
        return self._elements

    def get_cells(self) -> List[Cell]:
        """Get all logical cells of the maze.
        
        Returns:
            List[Cell]: List of all cells in the maze.
        """
        return self._cells

    def update_cells(self, new_cells: List[Cell]) -> None:
        """Update the maze with new cell data and clear elements.
        
        Replaces all cells in the maze and clears the elements list,
        typically used after maze generation to update the structure.
        
        Args:
            new_cells (List[Cell]): New list of cells to replace the current ones.
        """
        self._cells.clear()
        self._elements.clear()
        self._cells = new_cells
