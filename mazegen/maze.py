from .element import Element
from .cell import Cell

from typing import List, Tuple
from random import seed


class MazeConfig:
    def __init__(
        self,
    ) -> None:

        self.height: int = 10
        self.width: int = 10
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (1, 1)
        self.output: str = "output.txt"
        self.is_perfect: bool = True

    # fix later : to seddik
    # def parse(self, filename: str):
    #     config = {}
    #     try:
    #         with open(filename, "r") as fd:
    #             for line in fd:
    #                 if "=" in line and not line.startswith("#"):
    #                     key, value = line.strip().split("=", 1)
    #                     config[key.strip().upper()] = value.strip()

    #             WIDTH = int(config.get("WIDTH", 10))
    #             HEIGHT = int(config.get("HEIGHT", 10))

    #             is_perfect_str = config.get("PERFECT", "TRUE").strip().upper()
    #             is_perfect = is_perfect_str == "TRUE"

    #             raw_seed = config.get("SEED")

    #             if raw_seed and raw_seed.strip():
    #                 seed(raw_seed)
    #                 current_seed = raw_seed
    #             else:
    #                 seed(None)
    #                 current_seed = "Random/System Time"

    #     except (FileNotFoundError, PermissionError, KeyError, ValueError) as e:
    #         print(f"[Error loading], using default config {e}")
    #         is_perfect = True
    #         exit(1)

    #     print(f"Configuration Loaded: {WIDTH}x{HEIGHT} (Seed: {current_seed})")

    # def get_safe_coords(self, key, default_x, default_y, max_w, max_h, config):
    #     raw_val = config.get(key)
    #     if not raw_val:
    #         return (default_x, default_y)

    #     try:
    #         # Split "0,0" into [0, 0]
    #         parts = raw_val.split(",")
    #         if len(parts) != 2:
    #             raise ValueError

    #         x, y = int(parts[0].strip()), int(parts[1].strip())

    #         # Check if within maze bounds
    #         if 0 <= x < max_w and 0 <= y < max_h:
    #             return (x, y)
    #         else:
    #             raise ValueError

    #     except (ValueError, IndexError):
    #         print(f"[Warning]: {key} {x},{y} has invalid format in config.txt")
    #         exit(1)


class Maze:

    def __init__(self, y_shift: int, x_shift: int) -> None:
        self.y_shift = y_shift
        self.x_shift = x_shift

        self._elements: List[Element] = list()
        self._cells = list()

    def add_element(self, element_y: int, element_x: int, element_shape) -> None:
        self._elements.append(Element(element_y, element_x, element_shape))

    def get_elements(self) -> List[Element]:
        return self._elements

    def get_cells(self) -> List[Cell]:
        return self._cells

    def update_cells(self, new_cells: List[Cell]) -> None:
        self._cells.clear()
        self._elements.clear()
        self._cells = new_cells
