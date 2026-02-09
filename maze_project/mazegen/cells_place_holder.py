import random
from mazegen.model import Cell
from imperfect_maze import remove_random_walls
import time
# from app.a_maze_ing import 


class MazeGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = []
        for y in range(height):
            row = []
            for x in range(width):
                new_cell = Cell(y, x, True, True, True, True)
                row.append(new_cell)
            self.grid.append(row)

    def _get_neighbors(self, x: int, y: int, visited: set):
        neighbors = []
        directions = [
            (0, -1, 'up', 'down'),
            (0, 1, 'down', 'up'),
            (-1, 0, 'left', 'right'),
            (1, 0, 'right', 'left')
        ]

        for dx, dy, curr_attr, neigh_attr in directions:
            nx, ny = x + dx, y + dy
            # Strictly stay within bounds to keep outer walls solid
            if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                neighbors.append((nx, ny, curr_attr, neigh_attr))
        return neighbors

    def generate(self, make_perfect: bool = True) -> list[Cell]:
        """Recursive Backtracking to create a perfect maze."""

        stack = []
        visited = set()

        # Coordinates (x, y) that should stay as solid blocks to form "42"
        coordinating_42_cells = [
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
            (4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2), (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)
        ]

        if self.width >= 10 and self.height >= 7:
            start_x = (self.width - 7) // 2
            start_y = (self.height - 5) // 2

            for dx, dy in coordinating_42_cells:
                target_x, target_y = start_x + dx, start_y + dy
                if 0 <= target_x < self.width and 0 <= target_y < self.height:
                    visited.add((target_x, target_y))
                    self.grid[target_y][target_x].is_shape = True

        start_pos = (0, 0)
        visited.add(start_pos)
        stack.append(self.grid[0][0])

        while stack:
            current = stack[-1]
            neighbors = self._get_neighbors(current.x, current.y, visited)

            if neighbors:
                nx, ny, curr_wall, neigh_wall = random.choice(neighbors)
                neighbor_cell = self.grid[ny][nx]

                # Remove shared walls internally to carve paths
                setattr(current, curr_wall, False)
                setattr(neighbor_cell, neigh_wall, False)

                visited.add((nx, ny))
                stack.append(neighbor_cell)
            else:
                stack.pop()

        if not make_perfect:
            print("Modifying maza to be perfect...")
            time.sleep(1)
            remove_random_walls(self.grid, self.width, self.height, factor=0.1)

        flat_list = []
        for row in self.grid:
            for cell in row:
                flat_list.append(cell)

        return flat_list
