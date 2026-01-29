"""
visualizer.py
ASCII terminal visualization of mazes.
(REFACTORED INTERNALLY — DISPLAY OUTPUT UNCHANGED)
"""

import os
import sys
import time
from typing import Set, Tuple


class TerminalVisualizer:
    WALL_CHAR = '█'
    EMPTY_CHAR = ' '
    ENTRY_CHAR = 'E'
    EXIT_CHAR = '◆'
    SOLUTION_CHAR = '*'
    CURRENT_CHAR = '◆'

    COLORS = {
        'wall': '\033[90m',
        'entry': '\033[92m',
        'exit': '\033[91m',
        'solution': '\033[93m',
        'current': '\033[95m',
        'reset': '\033[0m'
    }

    MOVES = {
        'N': (0, -1),
        'E': (1, 0),
        'S': (0, 1),
        'W': (-1, 0),
    }

    def __init__(self, maze, use_colors=True, show_solution=False,
                 solution_style='arrow'):
        self.maze = maze
        self.use_colors = use_colors and sys.stdout.isatty()
        self.show_solution = show_solution
        self.solution_style = solution_style

    # ───────────────────────── helpers (SAFE) ─────────────────────────

    def _color(self, char, key):
        if not self.use_colors:
            return char
        return f"{self.COLORS[key]}{char}{self.COLORS['reset']}"

    def _solution_coords(self):
        x, y = self.maze.entry
        coords = [(x, y)]
        for d in self.maze.solution_path:
            dx, dy = self.MOVES.get(d, (0, 0))
            x += dx
            y += dy
            coords.append((x, y))
        return coords

    def _solution_arrows(self, coords):
        arrows = {}
        for (x1, y1), (x2, y2) in zip(coords, coords[1:]):
            dx, dy = x2 - x1, y2 - y1
            arrows[(x1, y1)] = {
                (1, 0): '→',
                (-1, 0): '←',
                (0, 1): '↓',
                (0, -1): '↑'
            }.get((dx, dy), self.SOLUTION_CHAR)
        return arrows

    # ───────────────────── GRID (LOGIC ONLY) ──────────────────────────

    def _build_grid(self, traced=None, current=None, arrows=None):
        traced = traced or set()

        h = self.maze.height * 2 + 1
        w = self.maze.width * 2 + 1
        grid = [[self.WALL_CHAR for _ in range(w)] for _ in range(h)]

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.cells[y][x]
                gx, gy = x * 2 + 1, y * 2 + 1
                grid[gy][gx] = self.EMPTY_CHAR

                pos = (x, y)

                if pos == current:
                    grid[gy][gx] = self._color(self.CURRENT_CHAR, 'current')
                elif pos == self.maze.entry:
                    grid[gy][gx] = self._color(self.ENTRY_CHAR, 'entry')
                elif pos == self.maze.exit:
                    grid[gy][gx] = self._color(self.EXIT_CHAR, 'exit')
                elif pos in traced:
                    char = (arrows or {}).get(pos, self.SOLUTION_CHAR)
                    grid[gy][gx] = self._color(char, 'solution')

                if not cell.walls[0]:
                    grid[gy - 1][gx] = self.EMPTY_CHAR
                if not cell.walls[1]:
                    grid[gy][gx + 1] = self.EMPTY_CHAR
                if not cell.walls[2]:
                    grid[gy + 1][gx] = self.EMPTY_CHAR
                if not cell.walls[3]:
                    grid[gy][gx - 1] = self.EMPTY_CHAR

        if self.use_colors:
            for y in range(h):
                for x in range(w):
                    if grid[y][x] == self.WALL_CHAR:
                        grid[y][x] = self._color(self.WALL_CHAR, 'wall')

        return grid

    def _print_grid(self, grid):
        for row in grid:
            print(''.join(row))

    # ───────────────── DISPLAY (UNCHANGED OUTPUT) ─────────────────────

    def display_solution_animated(self, delay=0.3):
        if not self.maze.solution_path:
            print("\n✗ No solution available to display!")
            return

        coords = self._solution_coords()
        arrows = self._solution_arrows(coords)
        traced: Set[Tuple[int, int]] = set()

        print("\n" + "=" * 60)
        print("ANIMATED SOLUTION - WATCHING PATH BUILD IN MAZE")
        print("=" * 60 + "\n")

        for step, pos in enumerate(coords):
            traced.add(pos)

            os.system('clear' if os.name == 'posix' else 'cls')

            print("=" * 60)
            print("ANIMATED SOLUTION - WATCHING PATH BUILD IN MAZE")
            print("=" * 60)

            if step == len(coords) - 1:
                print(f"Step {step}/{step}: ✓ COMPLETED!\n")
            else:
                print(f"Step {step}/{len(coords)-1}\n")

            grid = self._build_grid(traced, pos, arrows)
            self._print_grid(grid)

            filled = int(40 * step / (len(coords) - 1))
            bar = '█' * filled + '░' * (40 - filled)
            percent = int(100 * step / (len(coords) - 1))

            print(f"\nProgress: [{bar}] {percent}% ({step}/{len(coords)-1})\n")

            print("LEGEND:")
            print("  E  Entry point")
            print("  ◆  Exit point")
            print("  █  Wall")
            print("  *  Traced path")
            print("  ◆  Current position")

            time.sleep(delay)

        print("\n" + "=" * 60)
        print(f"✓ MAZE SOLVED IN {len(coords)-1} STEPS!")
        print("=" * 60 + "\n")
