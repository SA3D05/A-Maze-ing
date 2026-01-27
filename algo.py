"""
Maze generation algorithms implementation.
"""

import random
from typing import List, Tuple, Set
from .generator import Cell


class BaseAlgorithm:
    """Base class for maze generation algorithms."""
    
    def __init__(self, cells: List[List[Cell]], width: int, height: int):
        self.cells = cells
        self.width = width
        self.height = height
    
    def generate(self):
        """Generate maze - to be implemented by subclasses."""
        raise NotImplementedError


class PrimAlgorithm(BaseAlgorithm):
    """Prim's algorithm for maze generation."""
    
    def generate(self):
        # Start with a grid full of walls
        # Pick a cell, mark it as part of the maze
        # Add the walls of the cell to the wall list
        
        start_x, start_y = 0, 0
        self.cells[start_y][start_x].visited = True
        
        walls = self._get_cell_walls(start_x, start_y)
        
        while walls:
            # Pick a random wall
            wall = random.choice(walls)
            x, y, direction = wall
            
            # Get neighbor in that direction
            nx, ny = self._get_neighbor(x, y, direction)
            
            if (0 <= nx < self.width and 0 <= ny < self.height and
                not self.cells[ny][nx].visited):
                
                # Remove the wall
                self.cells[y][x].walls[direction] = False
                opposite_dir = (direction + 2) % 4
                self.cells[ny][nx].walls[opposite_dir] = False
                
                # Mark the neighbor as visited
                self.cells[ny][nx].visited = True
                
                # Add the new cell's walls
                walls.extend(self._get_cell_walls(nx, ny))
            
            # Remove this wall from the list
            walls.remove(wall)
    
    def _get_cell_walls(self, x: int, y: int) -> List[Tuple[int, int, int]]:
        """Get all walls of a cell as (x, y, direction) tuples."""
        walls = []
        for direction in range(4):
            nx, ny = self._get_neighbor(x, y, direction)
            if 0 <= nx < self.width and 0 <= ny < self.height:
                walls.append((x, y, direction))
        return walls
    
    def _get_neighbor(self, x: int, y: int, direction: int) -> Tuple[int, int]:
        """Get neighbor coordinates in given direction."""
        if direction == 0:  # North
            return x, y - 1
        elif direction == 1:  # East
            return x + 1, y
        elif direction == 2:  # South
            return x, y + 1
        else:  # West
            return x - 1, y


class RecursiveBacktracker(BaseAlgorithm):
    """Recursive backtracker algorithm for maze generation."""

    def generate(self):
        start_x, start_y = 0, 0
        self._carve_passage(start_x, start_y)
    
    def _carve_passage(self, x: int, y: int):
        """Recursively carve passages."""
        self.cells[y][x].visited = True

        # Randomize directions
        directions = [0, 1, 2, 3]  # N, E, S, W
        random.shuffle(directions)

        for direction in directions:
            nx, ny = self._get_neighbor(x, y, direction)

            if (0 <= nx < self.width and 0 <= ny < self.height and not self.cells[ny][nx].visited):

                # Remove the wall between current cell and neighbor
                self.cells[y][x].walls[direction] = False
                opposite_dir = (direction + 2) % 4
                self.cells[ny][nx].walls[opposite_dir] = False

                # Recursively visit the neighbor
                self._carve_passage(nx, ny)

    def _get_neighbor(self, x: int, y: int, direction: int) -> Tuple[int, int]:
        """Get neighbor coordinates in given direction."""
        if direction == 0:  # North
            return x, y - 1
        elif direction == 1:  # East
            return x + 1, y
        elif direction == 2:  # South
            return x, y + 1
        else:  # West
            return x - 1, y
