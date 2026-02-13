from .cell import Cell, CellState
from .maze import MazeConfig
from .element import Element
from .maze import Maze
from .tile import Tile


from heapq import heappop, heappush
from random import choice, randint
from typing import List, Optional
from math import sqrt
from random import seed as sync_seed


class MazeGenerator:

    def __init__(self, config: MazeConfig):
        self.config: MazeConfig = config
        self.last_path: Optional[List] = None  # stores the last dijkstra solution

    def __get_neighbors(self, x: int, y: int, visited: set):

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

    def generate(self, maze: Maze, make_perfect: bool) -> None:
        """Recursive Backtracking to create a perfect maze.
        take maze object and update its cells with new generated ones.
        """

        if self.config.seed_val == "Random/System Time":
            sync_seed(None)
        else:
            sync_seed(self.config.seed_val)
        grid: List[List[Cell]] = []
        for y in range(self.config.height):
            row: List[Cell] = []
            for x in range(self.config.width):
                current_cell_state: CellState = CellState.REGULAR

                if (y, x) == self.config.entry:
                    current_cell_state = CellState.ENTRY

                if (y, x) == self.config.exit:
                    current_cell_state = CellState.EXIT

                new_cell = Cell(y, x, True, True, True, True, current_cell_state)
                row.append(new_cell)
            grid.append(row)
        stack = []
        visited = set()

        # Coordinates (x, y) that should stay as solid blocks to form "42"

        coordinating_42_cells = [
            (0, 0),
            (1, 0),
            (2, 0),
            (2, 1),
            (2, 2),
            (3, 2),
            (4, 2),
            (0, 4),
            (0, 5),
            (0, 6),
            (1, 6),
            (2, 6),
            (2, 5),
            (2, 4),
            (3, 4),
            (4, 4),
            (4, 5),
            (4, 6),
        ]

        if self.config.width >= 9 and self.config.height >= 7:
            start_x = (self.config.width - 7) // 2
            start_y = (self.config.height - 5) // 2

            for dy, dx in coordinating_42_cells:
                target_x, target_y = start_x + dx, start_y + dy

                # make this conition less ugly later

                if (
                    target_y == self.config.entry[0]
                    and target_x == self.config.entry[1]
                ) or (
                    target_y == self.config.exit[0] and target_x == self.config.exit[1]
                ):
                    raise ValueError(
                        "The entry or exit point cannot be placed within the protected '42' area."
                    )

                for cell_list in grid:
                    for cell in cell_list:
                        if cell.x == target_x and cell.y == target_y:
                            cell.state = CellState.FT
                        # we dont know whta the fu** is this for
                        # if (
                        #     0 <= target_x < self.config.width
                        #     and 0 <= target_y < self.config.height
                        # ):
                        visited.add((target_x, target_y))

        start_pos = (0, 0)
        visited.add(start_pos)
        stack.append(grid[0][0])
        while stack:
            current = stack[-1]
            neighbors = self.__get_neighbors(current.x, current.y, visited)

            if neighbors:
                nx, ny, curr_wall, neigh_wall = choice(neighbors)
                neighbor_cell = grid[ny][nx]

                # Remove shared walls internally to carve paths
                setattr(current, curr_wall, False)
                setattr(neighbor_cell, neigh_wall, False)

                visited.add((nx, ny))
                stack.append(neighbor_cell)
            else:
                stack.pop()

        if not make_perfect:
            self.__remove_random_walls(
                grid, self.config.width, self.config.height, factor=0.1
            )

        cells_list = []
        for row in grid:
            for cell in row:
                cells_list.append(cell)

        path = self.__dijkstra(grid, self.config.entry, self.config.exit)
        self.last_path = path  # store path so caller can pass it to save_maze()
        self.last_grid = grid  # store 2D grid so caller can pass it to save_maze()

        if path is not None:
            for cell in cells_list:
                if (cell.x, cell.y) in path and cell.state not in [
                    CellState.ENTRY,
                    CellState.EXIT,
                ]:
                    cell.state = CellState.PATH
        maze.update_cells(cells_list)

    def __remove_random_walls(self, grid, width, height, factor=0.1) -> None:
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
            x = randint(0, width - 2)
            y = randint(0, height - 2)

            current_cell = grid[y][x]

            if choice(["right", "down"]) == "right":
                neighbor = grid[y][x + 1]
                if not is_protected(x, y) and not is_protected(x + 1, y):
                    current_cell.right = False
                    neighbor.left = False
            else:
                neighbor = grid[y + 1][x]
                if not is_protected(x, y) and not is_protected(x, y + 1):
                    current_cell.down = False
                    neighbor.up = False

    def __dijkstra(self, grid, start, end):
        """
        grid: 2D list of Cell objects
        start/end: tuples (x, y)
        """
        if not isinstance(grid[0], list):
            # We assume square or use a known width
            width = int(sqrt(len(grid)))
            grid = [grid[i: i + width] for i in range(0, len(grid), width)]

        rows, cols = len(grid), len(grid[0])
        # pq: (distance, (x, y), path_list)
        pq = [(0, start, [start])]
        visited = set()

        while pq:
            (dist, (cx, cy), path) = heappop(pq)

            if (cx, cy) == end:
                return path

            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))

            current_cell = grid[cy][cx]

            # Check all 4 directions based on wall status
            # Note: We move to (nx, ny) only if the wall between is False
            directions = [
                (cx, cy - 1, not current_cell.up),
                (cx, cy + 1, not current_cell.down),
                (cx - 1, cy, not current_cell.left),
                (cx + 1, cy, not current_cell.right),
            ]

            for nx, ny, is_open in directions:
                if is_open and 0 <= nx < cols and 0 <= ny < rows:
                    if (nx, ny) not in visited:
                        heappush(pq, (dist + 1, (nx, ny), path + [(nx, ny)]))

        return None  # No path found
        # -------------------------------------------------------------

    def gen_grid(self, maze: Maze) -> None:
        """Generate the initial grid structure of the maze.
        Note: Make me less ugly !!
        """
        h_max = self.config.height * 2
        w_max = self.config.width * 2

        for col in range(h_max + 1):
            for row in range(w_max + 1):
                # 1. Determine the character
                shape = None

                # Perfect Corners
                if (col, row) == (0, 0):
                    shape = Tile.LEFT_TOP.value
                elif (col, row) == (0, w_max):
                    shape = Tile.RIGHT_TOP.value
                elif (col, row) == (h_max, 0):
                    shape = Tile.LEFT_BOTTOM.value
                elif (col, row) == (h_max, w_max):
                    shape = Tile.RIGHT_BOTTOM.value

                # Top/Bottom Edges (T-Junctions)
                elif col == 0 and row % 2 == 0:
                    shape = Tile.T_DOWN.value
                elif col == h_max and row % 2 == 0:
                    shape = Tile.T_UP.value

                # Left/Right Edges (T-Junctions)
                elif row == 0 and col % 2 == 0:
                    shape = Tile.T_RIGHT.value
                elif row == w_max and col % 2 == 0:
                    shape = Tile.T_LEFT.value

                # Internal Grid
                elif col % 2 == 0:
                    shape = Tile.CENTER.value if row % 2 == 0 else Tile.HORIZONTAL.value
                elif row % 2 == 0:
                    shape = Tile.VERTICAL.value

                # 2. Add to maze (One single call!)
                if shape:
                    maze.add_element(col + maze.y_shift, row + maze.x_shift, shape)

                else:
                    for cell in maze.get_cells():

                        cell_x = self.get_horizontal_cell_pos(cell.x, 0)
                        cell_y = self.get_vertical_cell_pos(cell.y, 0)

                        if cell_x == row and cell_y == col:

                            if cell.state == CellState.FT:
                                maze.add_element(
                                    col + maze.y_shift,
                                    row + maze.x_shift,
                                    Tile.BLOCK.value,
                                )
                            elif cell.state == CellState.ENTRY:
                                maze.add_element(
                                    col + maze.y_shift,
                                    row + maze.x_shift,
                                    Tile.ENTER.value,
                                )
                            elif cell.state == CellState.EXIT:
                                maze.add_element(
                                    col + maze.y_shift,
                                    row + maze.x_shift,
                                    Tile.EXIT.value,
                                )
                            elif cell.state == CellState.PATH:
                                maze.add_element(
                                    col + maze.y_shift,
                                    row + maze.x_shift,
                                    Tile.PATH.value,
                                )
                            elif cell.state == CellState.REGULAR:
                                maze.add_element(
                                    col + maze.y_shift,
                                    row + maze.x_shift,
                                    Tile.SPACE.value,
                                )

    def get_horizontal_cell_pos(self, pos: int, x_shift: int) -> int:
        result: int = pos * 2 + 1 + x_shift
        return result

    def get_vertical_cell_pos(self, pos: int, y_shift: int) -> int:
        result: int = pos * 2 + 1 + y_shift
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
                return el.shape
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
                        element.shape = " "
                # right
                if element.x == self.get_horizontal_cell_pos(
                    cell.x, maze.x_shift
                ) + 1 and element.y == self.get_vertical_cell_pos(cell.y, maze.y_shift):
                    if not cell.right:
                        element.shape = " "
                # up and right  for the next cell handel the previes down and left so we dont actily need them

    def handel_center(self, element: Element, elements: List[Element]):
        """Handle the rendering of center junctions based on surrounding elements."""
        up = 1 if self.get_near_element(element, elements, 0) != " " else 0
        down = 2 if self.get_near_element(element, elements, 2) != " " else 0
        left = 4 if self.get_near_element(element, elements, 3) != " " else 0
        right = 8 if self.get_near_element(element, elements, 1) != " " else 0

        score = up + down + left + right

        bit_map = {
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

        element.shape = bit_map.get(score, Tile.SPACE.value)

    def handel_corners(self, elements: List[Element]):
        for element in elements:
            if element.shape == Tile.CENTER.value:
                self.handel_center(element, elements)
            if element.shape == Tile.T_DOWN.value:
                if self.get_near_element(element, elements, 2) == " ":
                    element.shape = Tile.HORIZONTAL.value

            elif element.shape == Tile.T_UP.value:
                if self.get_near_element(element, elements, 0) == " ":
                    element.shape = Tile.HORIZONTAL.value

            elif element.shape == Tile.T_LEFT.value:
                if self.get_near_element(element, elements, 3) == " ":
                    element.shape = Tile.VERTICAL.value

            elif element.shape == Tile.T_RIGHT.value:
                if self.get_near_element(element, elements, 1) == " ":
                    element.shape = Tile.VERTICAL.value