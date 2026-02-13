from .element import Element
from .cell import Cell

from typing import List, Tuple
from random import seed as set_random_seed


class MazeConfig:
    def __init__(self) -> None:
        self.height: int = 10
        self.width: int = 10
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (9, 9)
        self.is_perfect: bool = True
        self.seed_val: str = "Random/System Time"

    def parse(self, filename: str) -> None:
        raw_config = {}
        try:
            with open(filename, "r") as fd:
                for line in fd:
                    line = line.strip()
                    # Skip empty lines or comments
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        raw_config[key.strip().upper()] = value.strip()

            self.width = int(raw_config.get("WIDTH", self.width))
            self.height = int(raw_config.get("HEIGHT", self.height))

            perf_str = raw_config.get("PERFECT", "TRUE").upper()
            self.is_perfect = (perf_str == "TRUE")

            # --- SEED LOGIC ---
            raw_seed = raw_config.get("SEED")
            if raw_seed:
                # If a seed exists in config, use it
                self.seed_val = raw_seed
                # We can set the seed here globally or pass it to generator
                set_random_seed(raw_seed)
            else:
                # If seed is missing or commented out, use system time (None)
                self.seed_val = "Random/System Time"
                set_random_seed(None)

            self.entry = self._get_safe_coords(raw_config, "ENTRY", 0, 0)
            self.exit = self._get_safe_coords(raw_config, "EXIT", self.width - 1, self.height - 1)

            print(f"Config Loaded: {self.width}x{self.height} (Seed: {self.seed_val})")

        except (FileNotFoundError, PermissionError) as e:
            print(f"File error: {e}. Using defaults.")

    def _get_safe_coords(self, config_dict, key, def_x, def_y) -> Tuple[int, int]:
        val = config_dict.get(key)
        if not val:
            return (def_x, def_y)

        try:
            parts = val.split(",")
            x, y = int(parts[0].strip()), int(parts[1].strip())
            if 0 <= x < self.width and 0 <= y < self.height:
                return (x, y)
            raise ValueError
        except (ValueError, IndexError):
            return (def_x, def_y)


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
