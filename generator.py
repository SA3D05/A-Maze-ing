"""
mazegen/generator.py
Core maze generation logic.
(REFACTORED INTERNALLY — BEHAVIOR UNCHANGED)
"""

import random
import time
from typing import List, Tuple, Optional
from dataclasses import dataclass


# ───────────────────────── CELL ──────────────────────────

@dataclass
class Cell:
    """
    Represents a single cell in the maze.
    """
    x: int
    y: int
    walls: List[bool]  # [North, East, South, West]
    visited: bool = False

    def __post_init__(self):
        if len(self.walls) != 4:
            self.walls = [True, True, True, True]

    def get_wall_bits(self) -> int:
        bits = 0
        for i, wall in enumerate(self.walls):
            if wall:
                bits |= (1 << i)
        return bits

    def remove_wall(self, direction: int):
        if 0 <= direction < 4:
            self.walls[direction] = False

    def is_fully_closed(self) -> bool:
        return all(self.walls)

    def __str__(self) -> str:
        names = ['N', 'E', 'S', 'W']
        active = ''.join(names[i] for i, w in enumerate(self.walls) if w)
        return f"Cell({self.x},{self.y}) walls:{active or 'none'}"


# ───────────────────────── MAZE ──────────────────────────

class Maze:
    """
    Represents a complete maze structure.
    """

    def __init__(self, width: int, height: int, cells: List[List[Cell]],
                 entry: Tuple[int, int],
                 exit: Tuple[int, int], verbose: bool = False):
        self.width = width
        self.height = height
        self.cells = cells
        self.entry = entry
        self.exit = exit
        self.solution_path: Optional[str] = None
        self.verbose = verbose

    # ─────────────── FILE OUTPUT ───────────────

    def save_to_file(self, filename: str):
        if self.verbose:
            print(f"[Maze] Saving to {filename}...")

        with open(filename, 'w') as file:
            for y in range(self.height):
                file.write(''.join(
                    f"{self.cells[y][x].get_wall_bits():X}"
                    for x in range(self.width)
                ) + '\n')

            file.write('\n')
            file.write(f"{self.entry[0]},{self.entry[1]}\n")
            file.write(f"{self.exit[0]},{self.exit[1]}\n")

            if self.solution_path:
                file.write(self.solution_path + '\n')

        if self.verbose:
            print(f"[Maze] ✓ Maze saved to {filename}")

    # ─────────────── VALIDATION ───────────────

    def validate(self) -> bool:
        if self.verbose:
            print("[Maze] Validating maze structure...")

        try:
            if len(self.cells) != self.height:
                return False

            for row in self.cells:
                if len(row) != self.width:
                    return False

            for y in range(self.height):
                for x in range(self.width):
                    cell = self.cells[y][x]

                    if x < self.width - 1:
                        if cell.walls[1] != self.cells[y][x + 1].walls[3]:
                            return False

                    if y < self.height - 1:
                        if cell.walls[2] != self.cells[y + 1][x].walls[0]:
                            return False

            if self.verbose:
                print("  ✓ Maze validation passed")
            return True

        except Exception:
            return False


# ────────────────────── GENERATOR ───────────────────────

class MazeGenerator:
    """
    Main maze generator class.
    """

    def __init__(self, config, verbose=False):
        self.config = config
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit
        self.perfect = config.perfect
        self.seed = config.seed
        self.verbose = verbose

        if self.seed is not None:
            random.seed(self.seed)

        self.cells = [
            [Cell(x, y, [True, True, True, True]) for x in range(self.width)]
            for y in range(self.height)
        ]

    # ─────────────── GENERATE ───────────────

    def generate(self) -> Maze:
        if self.verbose:
            print("[Generator] Generating maze...")
        start_time = time.time()

        if self.config.algorithm == "simple":
            self._generate_simple()
        else:
            self._generate_prim()

        self._set_entry_exit()

        maze = Maze(self.width, self.height, self.cells,
                    self.entry, self.exit, verbose=self.verbose)

        if not maze.validate():
            raise ValueError("Generated maze failed validation")

        if self.verbose:
            print(f"[Generator] ✓ Done in {time.time() - start_time:.2f}s")

        return maze

    # ─────────────── SIMPLE ───────────────

    def _generate_simple(self):
        for y in range(self.height):
            for x in range(self.width):
                if x < self.width - 1 and random.random() > 0.5:
                    self._remove_wall_pair(x, y, 1)

                if y < self.height - 1 and random.random() > 0.5:
                    self._remove_wall_pair(x, y, 2)

    # ─────────────── PRIM ───────────────

    def _generate_prim(self):
        start_x = random.randint(0, self.width - 1)
        start_y = random.randint(0, self.height - 1)
        self.cells[start_y][start_x].visited = True

        walls = self._get_cell_walls(start_x, start_y)

        while walls:
            x, y, direction = random.choice(walls)
            nx, ny = self._get_neighbor(x, y, direction)

            if self._in_bounds(nx, ny) and not self.cells[ny][nx].visited:
                self._remove_wall_pair(x, y, direction)
                self.cells[ny][nx].visited = True
                walls.extend(self._get_cell_walls(nx, ny))

            walls.remove((x, y, direction))

    # ─────────────── HELPERS ───────────────

    def _remove_wall_pair(self, x: int, y: int, direction: int):
        nx, ny = self._get_neighbor(x, y, direction)
        self.cells[y][x].remove_wall(direction)
        self.cells[ny][nx].remove_wall((direction + 2) % 4)

    def _get_cell_walls(self, x: int, y: int) -> List[Tuple[int, int, int]]:
        return [
            (x, y, d)
            for d in range(4)
            if self._in_bounds(*self._get_neighbor(x, y, d))
        ]

    def _get_neighbor(self, x: int, y: int, direction: int) -> Tuple[int, int]:
        return [
            (x, y - 1),
            (x + 1, y),
            (x, y + 1),
            (x - 1, y),
        ][direction]

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def _set_entry_exit(self):
        ex, ey = self.entry
        sx, sy = self.exit

        self._open_border_wall(ex, ey)
        self._open_border_wall(sx, sy)

    def _open_border_wall(self, x: int, y: int):
        if y == 0:
            self.cells[y][x].remove_wall(0)
        elif y == self.height - 1:
            self.cells[y][x].remove_wall(2)
        elif x == 0:
            self.cells[y][x].remove_wall(3)
        elif x == self.width - 1:
            self.cells[y][x].remove_wall(1)
