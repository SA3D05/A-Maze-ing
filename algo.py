"""
mazegen/generator.py
Core maze generation logic.
"""

import random
from typing import List, Tuple, Optional
from dataclasses import dataclass
import time


@dataclass
class Cell:
    """
    Represents a single cell in the maze.

    Attributes:
        x: X coordinate (column)
        y: Y coordinate (row)
        walls: List of 4 booleans for [North, East, South, West] walls
        visited: Whether this cell has been visited during generation
    """
    x: int
    y: int
    walls: List[bool]  # [North, East, South, West]
    visited: bool = False

    def __post_init__(self):
        """Ensure walls list has exactly 4 elements."""
        if len(self.walls) != 4:
            self.walls = [True, True, True, True]

    def get_wall_bits(self) -> int:
        """
        Convert walls to a hexadecimal digit.

        Returns:
            Integer where each bit represents a wall (1=closed, 0=open)
            Bit 0 (LSB): North, Bit 1: East, Bit 2: South, Bit 3: West
        """
        bits = 0
        for i, wall in enumerate(self.walls):
            if wall:
                bits |= (1 << i)
        return bits

    def remove_wall(self, direction: int):
        """
        Remove a wall in the given direction.

        Args:
            direction: 0=North, 1=East, 2=South, 3=West
        """
        if 0 <= direction < 4:
            self.walls[direction] = False

    def is_fully_closed(self) -> bool:
        """Check if all walls are closed."""
        return all(self.walls)

    def __str__(self) -> str:
        """String representation of the cell."""
        directions = ['N', 'E', 'S', 'W']
        walls_str = ''.join(directions[i] for i, wall in enumerate(self.walls) if wall)
        return f"Cell({self.x},{self.y}) walls:{walls_str or 'none'}"


class Maze:
    """
    Represents a complete maze structure.
    """

    def __init__(self, width: int, height: int, cells: List[List[Cell]], 
                 entry: Tuple[int, int], exit: Tuple[int, int]):
        self.width = width
        self.height = height
        self.cells = cells
        self.entry = entry
        self.exit = exit
        self.solution_path: Optional[str] = None

    def save_to_file(self, filename: str):
        """
        Save maze to file in the specified hexadecimal format.

        Format:
            - One hexadecimal digit per cell, row by row
            - Empty line
            - Entry coordinates
            - Exit coordinates
            - Solution path (if available)
        """
        print(f"[Maze] Saving to {filename}...")

        with open(filename, 'w') as file:
            # Write cell grid in hexadecimal
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    cell_value = self.cells[y][x].get_wall_bits()
                    row.append(f"{cell_value:X}")  # Convert to hex uppercase
                file.write(''.join(row) + '\n')

            # Empty line
            file.write('\n')

            # Write entry and exit
            file.write(f"{self.entry[0]},{self.entry[1]}\n")
            file.write(f"{self.exit[0]},{self.exit[1]}\n")

            # Write solution path if available
            if self.solution_path:
                file.write(self.solution_path + '\n')

        print(f"[Maze] ✓ Maze saved to {filename}")

        # Show a preview of the file
        print("[Maze] File preview (first 5 lines):")
        with open(filename, 'r') as file:
            for i, line in enumerate(file):
                if i < 5:
                    print(f"  Line {i+1}: {line.rstrip()}")
                else:
                    break

    def validate(self) -> bool:
        """
        Validate maze consistency.

        Returns:
            True if maze is valid, False otherwise
        """
        print("[Maze] Validating maze structure...")

        try:
            # Check that all cells exist
            if len(self.cells) != self.height:
                print(f"  ✗ Height mismatch: expected {self.height}, got {len(self.cells)}")
                return False

            for y, row in enumerate(self.cells):
                if len(row) != self.width:
                    print(f"  ✗ Width mismatch at row {y}: expected {self.width}, got {len(row)}")
                    return False

            # Check wall consistency between adjacent cells
            for y in range(self.height):
                for x in range(self.width):
                    cell = self.cells[y][x]

                    # Check east neighbor
                    if x < self.width - 1:
                        neighbor = self.cells[y][x + 1]
                        if cell.walls[1] != neighbor.walls[3]:  # East vs West
                            print(f"  ✗ Wall mismatch at ({x},{y}) east / ({x+1},{y}) west")
                            return False

                    # Check south neighbor
                    if y < self.height - 1:
                        neighbor = self.cells[y + 1][x]
                        if cell.walls[2] != neighbor.walls[0]:  # South vs North
                            print(f"  ✗ Wall mismatch at ({x},{y}) south / ({x},{y+1}) north")
                            return False

            print("  ✓ Maze validation passed!")
            print(f" ✓ Size: {self.width}x{self.height}")
            print(f" ✓ Entry: {self.entry}")
            print(f" ✓ Exit: {self.exit}")
            return True

        except Exception as e:
            print(f"  ✗ Validation error: {e}")
            return False


class MazeGenerator:
    """
    Main maze generator class.
    Generates mazes using various algorithms.
    """

    def __init__(self, config):
        """
        Initialize the maze generator with configuration.

        Args:
            config: MazeConfig object with generation parameters
        """
        self.config = config
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit
        self.perfect = config.perfect
        self.seed = config.seed

        # Set random seed for reproducibility
        if self.seed is not None:
            random.seed(self.seed)
            print(f"[Generator] Using seed: {self.seed}")

        # Initialize empty grid of cells
        self.cells: List[List[Cell]] = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Start with all walls up (closed)
                row.append(Cell(x, y, [True, True, True, True]))
            self.cells.append(row)

        print("[Generator] Initialized maze generator")
        print(f"  [Generator] Size: {self.width}x{self.height}")
        print(f"  [Generator] Perfect maze: {self.perfect}")

    def generate(self) -> Maze:
        """
        Generate a maze.

        Returns:
            Maze object representing the generated maze

        Raises:
            ValueError: If maze generation fails
        """
        print("\n[Generator] Generating maze...")
        start_time = time.time()

        try:
            # Choose generation algorithm based on config
            if self.config.algorithm == "simple":
                self._generate_simple()
            else:
                self._generate_prim()  # Default to Prim's algorithm

            # Set entry and exit
            self._set_entry_exit()

            # Create maze object
            maze = Maze(self.width, self.height, self.cells, self.entry, self.exit)

            # Validate the generated maze
            if not maze.validate():
                raise ValueError("Generated maze failed validation")

            # Calculate generation time
            elapsed_time = time.time() - start_time
            print(f"[Generator] ✓ Maze generated in {elapsed_time:.2f} seconds")

            return maze

        except Exception as e:
            raise ValueError(f"Failed to generate maze: {e}")

    def _generate_simple(self):
        """Generate a simple maze (for testing)."""
        print("[Generator] Using simple generation algorithm")

        # Simple algorithm: randomly remove some walls
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]

                # Randomly remove east wall (50% chance)
                if random.random() > 0.5 and x < self.width - 1:
                    cell.remove_wall(1)  # Remove east wall
                    self.cells[y][x + 1].remove_wall(3)  # Remove neighbor's west wall

                # Randomly remove south wall (50% chance)
                if random.random() > 0.5 and y < self.height - 1:
                    cell.remove_wall(2)  # Remove south wall
                    self.cells[y + 1][x].remove_wall(0)  # Remove neighbor's north wall

    def _generate_prim(self):
        """Generate maze using Prim's algorithm."""
        print("[Generator] Using Prim's algorithm")

        # Start with a random cell
        start_x, start_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        self.cells[start_y][start_x].visited = True

        # Get walls of the starting cell
        walls = self._get_cell_walls(start_x, start_y)

        while walls:
            # Pick a random wall
            wall = random.choice(walls)
            x, y, direction = wall

            # Get neighbor in that direction
            nx, ny = self._get_neighbor(x, y, direction)

            # If neighbor exists and hasn't been visited
            if (0 <= nx < self.width and 0 <= ny < self.height and
                    not self.cells[ny][nx].visited):

                # Remove the wall between current cell and neighbor
                self.cells[y][x].remove_wall(direction)
                opposite_dir = (direction + 2) % 4
                self.cells[ny][nx].remove_wall(opposite_dir)

                # Mark neighbor as visited
                self.cells[ny][nx].visited = True

                # Add new cell's walls to the list
                walls.extend(self._get_cell_walls(nx, ny))

            # Remove this wall from the list
            walls.remove(wall)

    def _get_cell_walls(self, x: int, y: int) -> List[Tuple[int, int, int]]:
        """
        Get all walls of a cell as (x, y, direction) tuples.

        Returns:
            List of walls where each wall is (x, y, direction)
        """
        walls = []
        for direction in range(4):
            nx, ny = self._get_neighbor(x, y, direction)
            if 0 <= nx < self.width and 0 <= ny < self.height:
                walls.append((x, y, direction))
        return walls

    def _get_neighbor(self, x: int, y: int, direction: int) -> Tuple[int, int]:
        """
        Get coordinates of neighbor in given direction.

        Args:
            x, y: Current cell coordinates
            direction: 0=North, 1=East, 2=South, 3=West

        Returns:
            Tuple (nx, ny) of neighbor coordinates
        """
        if direction == 0:  # North
            return x, y - 1
        elif direction == 1:  # East
            return x + 1, y
        elif direction == 2:  # South
            return x, y + 1
        else:  # West
            return x - 1, y

    def _set_entry_exit(self):
        """Remove walls at entry and exit points."""
        print("[Generator] Setting entry and exit...")

        ex, ey = self.entry
        sx, sy = self.exit

        # Remove appropriate walls for entry point based on position
        if ey == 0:  # Entry at top edge
            self.cells[ey][ex].remove_wall(0)  # North wall
            print("  [Generator] Entry at top - removed north wall")
        elif ey == self.height - 1:  # Entry at bottom edge
            self.cells[ey][ex].remove_wall(2)  # South wall
            print("  [Generator] Entry at bottom - removed south wall")
        elif ex == 0:  # Entry at left edge
            self.cells[ey][ex].remove_wall(3)  # West wall
            print("  [Generator] Entry at left - removed west wall")
        elif ex == self.width - 1:  # Entry at right edge
            self.cells[ey][ex].remove_wall(1)  # East wall
            print("  [Generator] Entry at right - removed east wall")

        # Remove appropriate walls for exit point based on position
        if sy == 0:  # Exit at top edge
            self.cells[sy][sx].remove_wall(0)  # North wall
            print("  [Generator] Exit at top - removed north wall")
        elif sy == self.height - 1:  # Exit at bottom edge
            self.cells[sy][sx].remove_wall(2)  # South wall
            print("  [Generator] Exit at bottom - removed south wall")
        elif sx == 0:  # Exit at left edge
            self.cells[sy][sx].remove_wall(3)  # West wall
            print("  [Generator] Exit at left - removed west wall")
        elif sx == self.width - 1:  # Exit at right edge
            self.cells[sy][sx].remove_wall(1)  # East wall
            print("  [Generator] Exit at right - removed east wall")

        print(f"  [Generator] Entry: {self.entry}, Exit: {self.exit}")


# Quick test function
if __name__ == "__main__":
    print("Testing maze generator...")

    # Create a simple config for testing
    class TestConfig:
        width = 5
        height = 5
        entry = (0, 0)
        exit = (4, 4)
        perfect = True
        algorithm = "prim"
        seed = 42
        output_file = "test_output.txt"
        display = False

    config = TestConfig()

    try:
        generator = MazeGenerator(config)
        maze = generator.generate()

        print("\nGenerated maze preview:")
        for y in range(maze.height):
            row = []
            for x in range(maze.width):
                cell = maze.cells[y][x]
                walls = cell.get_wall_bits()
                row.append(f"{walls:X}")
            print(f"  Row {y}: {''.join(row)}")

        maze.save_to_file(config.output_file)

        print("\n✓ Test completed successfully!")

    except Exception as e:
        print(f"✗ Test failed: {e}")