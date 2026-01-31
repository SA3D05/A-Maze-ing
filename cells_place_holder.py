import random
from model import Cell


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
            (0, -1, 'up', 'down'),     # North
            (0, 1, 'down', 'up'),      # South
            (-1, 0, 'left', 'right'),  # West
            (1, 0, 'right', 'left')    # East
        ]

        for dx, dy, curr_attr, neigh_attr in directions:
            nx, ny = x + dx, y + dy
            # Strictly stay within bounds to keep outer walls solid
            if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                neighbors.append((nx, ny, curr_attr, neigh_attr))
        return neighbors

    def generate(self) -> list[Cell]:
        """Recursive Backtracking to create a perfect maze."""

        stack = []
        visited = set()
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

        flat_list = []
        for row in self.grid:
            for cell in row:
                flat_list.append(cell)
        return flat_list
