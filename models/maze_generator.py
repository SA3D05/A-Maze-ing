from typing import List
import random

from models.maze import Maze
from models.maze_config import MazeConfig
from models.tile import Tile
from models.element import Element
from models.cell import Cell


class MazeGenerator:

    def __init__(self, config: MazeConfig):
        self.config: MazeConfig = config

    def _get_neighbors(self, x: int, y: int, visited: set):
        neighbors = []
        directions = [
            (0, -1, "up", "down"),
            (0, 1, "down", "up"),
            (-1, 0, "left", "right"),
            (1, 0, "right", "left"),
        ]

        for dx, dy, curr_attr, neigh_attr in directions:
            nx, ny = x + dx, y + dy
            # Strictly stay within bounds to keep outer walls solid
            if (
                0 <= nx < self.config.width
                and 0 <= ny < self.config.height
                and (nx, ny) not in visited
            ):
                neighbors.append((nx, ny, curr_attr, neigh_attr))
        return neighbors

    def generate(self, make_perfect: bool = True) -> list[Cell]:
        """Recursive Backtracking to create a perfect maze."""

        stack = []
        visited = set()

        # Coordinates (x, y) that should stay as solid blocks to form "42"
        coordinating_42_cells = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (4, 0),
            (5, 0),
            (6, 0),
            (6, 1),
            (6, 2),
            (5, 2),
            (4, 2),
            (4, 3),
            (4, 4),
            (5, 4),
            (6, 4),
        ]

        self.grid = list()
        for y in range(self.config.height):
            row = list()
            for x in range(self.config.width):
                new_cell = Cell(y, x, True, True, True, True)
                row.append(new_cell)
            self.grid.append(row)

        if self.config.width >= 10 and self.config.height >= 10:
            start_x = (self.config.width - 7) // 2
            start_y = (self.config.height - 5) // 2

            for dx, dy in coordinating_42_cells:
                target_x, target_y = start_x + dx, start_y + dy
                if (
                    0 <= target_x < self.config.width
                    and 0 <= target_y < self.config.height
                ):
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
            self.remove_random_walls(
                self.grid, self.config.width, self.config.height, factor=0.1
            )

        flat_list = []
        for row in self.grid:
            for cell in row:
                flat_list.append(cell)

        return flat_list

    def remove_random_walls(self, grid, width, height, factor=0.1):
        """
        Takes a finished maze and breaks extra walls to create loops.
        """

        pos_x = (width - 7) // 2
        pos_y = (height - 5) // 2
        end_x, end_y = pos_x + 7, pos_y + 5

        def is_protected(x, y):
            return pos_x <= x < end_x and pos_y <= y < end_y

        extra_openings = int((width * height) * factor)

        for _ in range(extra_openings):
            x = random.randint(0, width - 2)
            y = random.randint(0, height - 2)

            current_cell = grid[y][x]

            if random.choice(["right", "down"]) == "right":
                neighbor = grid[y][x + 1]
                if not is_protected(x, y) and not is_protected(x + 1, y):
                    current_cell.right = False
                    neighbor.left = False
            else:
                neighbor = grid[y + 1][x]
                if not is_protected(x, y) and not is_protected(x, y + 1):
                    current_cell.down = False
                    neighbor.up = False

    # -------------------------------------------------------------

    def gen_grid(self, maze: Maze) -> None:
        """Generate the initial grid structure of the maze.
        Note: Make me less ugly !!
        """
        for column in range(self.config.height * 2 + 1):
            y_even = True if column % 2 == 0 else False
            for row in range(self.config.width * 2 + 1):
                x_even = True if row % 2 == 0 else False
                if column == 0 and row == 0:
                    maze.add_element(
                        column + maze.y_shift,
                        row + maze.x_shift,
                        Tile.LEFT_TOP.value,
                    )
                elif column == 0 and row == self.config.width * 2:
                    maze.add_element(
                        column + maze.y_shift,
                        row + maze.x_shift,
                        Tile.RIGHT_TOP.value,
                    )
                elif column == self.config.height * 2 and row == 0:
                    maze.add_element(
                        column + maze.y_shift,
                        row + maze.x_shift,
                        Tile.LEFT_BOTTOM.value,
                    )
                elif column == self.config.height * 2 and row == self.config.width * 2:
                    maze.add_element(
                        column + maze.y_shift,
                        row + maze.x_shift,
                        Tile.RIGHT_BOTTOM.value,
                    )

                elif x_even and column == 0:
                    maze.add_element(
                        column + maze.y_shift,
                        row + maze.x_shift,
                        Tile.T_DOWN.value,
                    )
                elif x_even and column == self.config.height * 2:
                    maze.add_element(
                        column + maze.y_shift,
                        row + maze.x_shift,
                        Tile.T_UP.value,
                    )

                elif y_even:
                    if row == 0:
                        maze.add_element(
                            column + maze.y_shift,
                            row + maze.x_shift,
                            Tile.T_RIGHT.value,
                        )
                    elif row == self.config.width * 2:
                        maze.add_element(
                            column + maze.y_shift,
                            row + maze.x_shift,
                            Tile.T_LEFT.value,
                        )

                    elif x_even:
                        maze.add_element(
                            column + maze.y_shift,
                            row + maze.x_shift,
                            Tile.CENTER.value,
                        )

                    else:
                        maze.add_element(
                            column + maze.y_shift,
                            row + maze.x_shift,
                            Tile.HORIZONTAL.value,
                        )

                elif not y_even and x_even:
                    maze.add_element(
                        column + maze.y_shift,
                        row + maze.x_shift,
                        Tile.VERTICAL.value,
                    )

                else:
                    maze.add_element(
                        column + maze.y_shift,
                        row + maze.x_shift,
                        " ",
                    )

    def get_horizontal_cell_pos(self, pos: int, x_shift: int) -> int:
        result: int = (pos * 2) + 1 + x_shift
        return result

    def get_vertical_cell_pos(self, pos: int, y_shift: int) -> int:
        result: int = (pos * 2) + 1 + y_shift
        return result

    def get_near_element(
        self, element: Element, elements: List[Element], directions: int
    ):

        target_x = -1
        target_y = -1

        if directions == 0:
            target_x: int = element.x
            target_y: int = element.y - 1

        elif directions == 1:
            target_x: int = element.x + 1
            target_y: int = element.y
        elif directions == 2:
            target_x: int = element.x
            target_y: int = element.y + 1
        elif directions == 3:
            target_x: int = element.x - 1
            target_y: int = element.y

        for el in elements:
            if el.x == target_x and el.y == target_y:
                return el.sprite
        return None

    def brake_walls(self, maze: Maze):
        for cell in maze.get_cells():
            for element in maze.get_elements():
                # up
                if (
                    element.x == self.get_horizontal_cell_pos(cell.x, maze.x_shift)
                    and element.y
                    == self.get_vertical_cell_pos(cell.y, maze.y_shift) - 1
                ):
                    if not cell.up:
                        element.sprite = " "
                # right
                if element.x == self.get_horizontal_cell_pos(
                    cell.x, maze.x_shift
                ) + 1 and element.y == self.get_vertical_cell_pos(cell.y, maze.y_shift):
                    if not cell.right:
                        element.sprite = " "
                # up and right  for the next cell handel the previes down and left so we dont actily need them

    def handel_center(self, element: Element, elements: List[Element]):
        """Handle the rendering of center junctions based on surrounding elements."""
        up = 1 if self.get_near_element(element, elements, 0) != " " else 0
        down = 2 if self.get_near_element(element, elements, 2) != " " else 0
        left = 4 if self.get_near_element(element, elements, 3) != " " else 0
        right = 8 if self.get_near_element(element, elements, 1) != " " else 0

        score = up + down + left + right

        BIT_MAP = {
            1: Tile.SHORT_UP.value,
            2: Tile.SHORT_DOWN.value,
            3: Tile.VERTICAL.value,
            4: Tile.SHORT_LEFT.value,
            5: Tile.RIGHT_BOTTOM.value,
            6: Tile.RIGHT_TOP.value,
            7: Tile.T_LEFT.value,
            8: Tile.SHORT_RIGHT.value,
            9: Tile.LEFT_BOTTOM.value,
            10: Tile.LEFT_TOP.value,
            11: Tile.T_RIGHT.value,
            12: Tile.HORIZONTAL.value,
            13: Tile.T_UP.value,
            14: Tile.T_DOWN.value,
            15: Tile.CENTER.value,
        }

        element.sprite = BIT_MAP.get(score, " ")

    def handel_corners(self, elements: List[Element]):
        for element in elements:
            if element.sprite == Tile.CENTER.value:
                self.handel_center(element, elements)
            if element.sprite == Tile.T_DOWN.value:
                if self.get_near_element(element, elements, 2) == " ":
                    element.sprite = Tile.HORIZONTAL.value

            elif element.sprite == Tile.T_UP.value:
                if self.get_near_element(element, elements, 0) == " ":
                    element.sprite = Tile.HORIZONTAL.value

            elif element.sprite == Tile.T_LEFT.value:
                if self.get_near_element(element, elements, 3) == " ":
                    element.sprite = Tile.VERTICAL.value

            elif element.sprite == Tile.T_RIGHT.value:
                if self.get_near_element(element, elements, 1) == " ":
                    element.sprite = Tile.VERTICAL.value
