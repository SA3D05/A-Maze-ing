from .cell import Cell, CellState
from .maze import MazeConfig
from .element import Element
from .maze import Maze
from .tile import Tile


from heapq import heappop, heappush
from random import choice, randint
from typing import List, Optional, Set, Tuple
from random import seed as sync_seed


class MazeGenerator:
    """Generates mazes using recursive backtracking algorithm.

    This class handles maze generation, wall carving, path finding (Dijkstra's algorithm),
    and rendering logic for converting maze structure to visual elements.

    Attributes:
        config (MazeConfig): Configuration parameters for the maze.
        last_path (List[Tuple[int, int]]): The solution path from last generation.
        last_grid (List[List[Cell]]): The cell grid from last generation.
    """

    def __init__(self, config: MazeConfig):
        """Initialize the MazeGenerator with a configuration.

        Args:
            config (MazeConfig): Configuration object containing maze parameters.
        """
        self.config: MazeConfig = config
        self.last_path: List[Tuple[int, int]] = list()
        self.last_grid: List[List[Cell]] = list()

    def save_maze(
        self,
        grid: List[List[Cell]],
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit_pt: Tuple[int, int],
        path_coords: List[Tuple[int, int]],
        filename: str = "maze.txt",
    ) -> None:
        """Save maze structure, entry/exit points, and solution path to a file.

        Encodes the maze structure as hexadecimal where each cell is represented
        by a 4-bit value (walls on up=1, right=2, down=4, left=8).
        Saves entry/exit coordinates and solution path as a hex mask.

        Args:
            grid (List[List[Cell]]): The maze grid to save.
            width (int): Width of the maze in cells.
            height (int): Height of the maze in cells.
            entry (Tuple[int, int]): Entry point as (y, x).
            exit_pt (Tuple[int, int]): Exit point as (y, x).
            path_coords (List[Tuple[int, int]]): List of cells in the solution path.
            filename (str): Output file path. Defaults to "maze.txt".
        """
        try:
            with open(filename, "w") as f:
                # 1. Write the Maze Structure Rows
                for y in range(height):
                    row_hex = ""
                    for x in range(width):
                        cell = grid[y][x]
                        val = 0
                        # Match the attributes in your model.py: up, right, down, left
                        if cell.up:
                            val += 1
                        if cell.right:
                            val += 2
                        if cell.down:
                            val += 4
                        if cell.left:
                            val += 8
                        row_hex += f"{val:X}"
                    f.write(f"{row_hex}\n")

                f.write("\n")  # Blank line separator

                # 2. Write Entry and Exit
                f.write(f"{entry[0]},{entry[1]}\n")
                f.write(f"{exit_pt[0]},{exit_pt[1]}\n\n")

                # 3. Write Path Solution as a single long Hex mask
                path_hex = self.__encode_path_mask(width, height, path_coords)
                f.write(f"{path_hex}\n")

        except Exception as e:
            # Using print here as a fallback if pdeb isn't imported
            print(f"[File Error]: {e}")

    def __encode_path_mask(
        self, width: int, height: int, path_coords: List[Tuple[int, int]]
    ) -> str:
        """Encode the solution path as a hexadecimal mask.

        Creates a binary string where each bit represents whether a cell is part
        of the solution path, then converts to hexadecimal.

        Args:
            width (int): Width of the maze in cells.
            height (int): Height of the maze in cells.
            path_coords (List[Tuple[int, int]]): List of cells in the solution path.

        Returns:
            str: Hexadecimal representation of the path mask.
        """
        bit_string = ""
        path_set = set(path_coords)
        for y in range(height):
            for x in range(width):
                bit_string += "1" if (x, y) in path_set else "0"
        return f"{int(bit_string, 2):X}" if bit_string else "0"

    def __get_neighbors(
        self, x: int, y: int, visited: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int, str, str]]:
        """Get unvisited neighboring cells in four cardinal directions.

        Args:
            x (int): X-coordinate of current cell.
            y (int): Y-coordinate of current cell.
            visited (Set[Tuple[int, int]]): Set of already visited cell coordinates.

        Returns:
            List[Tuple[int, int, str, str]]: List of (x, y, current_wall_attr, neighbor_wall_attr) tuples
                for each valid unvisited neighbor, where wall attributes are 'up', 'down', 'left', 'right'.
        """
        neighbors: List[Tuple[int, int, str, str]] = []
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
        """Generate a maze using recursive backtracking algorithm.

        Creates a maze by carving passages through a grid of cells. The algorithm
        randomly selects unvisited neighbors and removes walls between them.
        Can generate perfect mazes (no loops) or imperfect ones (with loops).
        The center area displays a large "42" pattern that cannot be carved.

        Args:
            maze (Maze): The maze object to populate with generated cells.
            make_perfect (bool): If True, generates a perfect maze (no loops).
                If False, randomly removes walls to create loops.

        Raises:
            ValueError: If entry or exit is within the protected "42" pattern area.
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
        stack: List[Cell] = []
        visited: Set[Tuple[int, int]] = set()

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
            neighbors: List[Tuple[int, int, str, str]] = self.__get_neighbors(
                current.x, current.y, visited
            )

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
        self.last_path = path if path else [()]  # type: ignore # store path so caller can pass it to save_maze()
        self.last_grid = grid

        if path is not None:
            for cell in cells_list:
                if (cell.y, cell.x) in path and cell.state not in [
                    CellState.ENTRY,
                    CellState.EXIT,
                ]:
                    cell.state = CellState.PATH
        maze.update_cells(cells_list)

    def __remove_random_walls(
        self, grid: List[List[Cell]], width: int, height: int, factor: float = 0.1
    ) -> None:
        """Randomly remove walls to create loops in the maze.

        Breaks down walls in the maze to transform it from a perfect maze
        (spanning tree with no loops) to one with multiple paths. Protected
        areas (the "42" pattern) are not affected.

        Args:
            grid (List[List[Cell]]): The maze grid to modify.
            width (int): Width of the maze in cells.
            height (int): Height of the maze in cells.
            factor (float): Fraction of walls to remove relative to total cells.
                Defaults to 0.1 (10% of cells worth of walls).
        """

        pos_x = (width - 7) // 2
        pos_y = (height - 5) // 2
        end_x, end_y = pos_x + 7, pos_y + 5

        def is_protected(x: int, y: int) -> bool:
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

    def __dijkstra(
        self, grid: List[List[Cell]], start: Tuple[int, int], end: Tuple[int, int]
    ) -> Optional[List[Tuple[int, int]]]:
        """Find the shortest path between two points using Dijkstra's algorithm.

        Finds the shortest path through the maze from start to end by exploring
        cells in order of distance, respecting walls and barriers.

        Args:
            grid (List[List[Cell]]): The maze grid containing cells and walls.
            start (Tuple[int, int]): Starting position as (y, x).
            end (Tuple[int, int]): Ending position as (y, x).

        Returns:
            Optional[List[Tuple[int, int]]]: List of (y, x) coordinates forming the path,
                or a fallback single-coordinate list if no path exists.
        """

        # if the grid type is correct that scope logic not neessesery
        # if not isinstance(grid[0], list):
        #     width = int(sqrt(len(grid)))
        #     grid = [grid[i : i + width] for i in range(0, len(grid), width)]

        rows, cols = len(grid), len(grid[0])

        # pq: (distance, (y, x), path_list)
        pq = [(0, start, [start])]
        visited: Set[Tuple[int, int]] = set()

        while pq:
            # Unpack as (cy, cx) to match the new (y, x) format
            (dist, (cy, cx), path) = heappop(pq)

            if (cy, cx) == end:
                return path

            if (cy, cx) in visited:
                continue
            visited.add((cy, cx))

            # Grid access remains [y][x]
            current_cell = grid[cy][cx]

            # directions are now (ny, nx, is_open)
            directions = [
                (cy - 1, cx, not current_cell.up),  # North
                (cy + 1, cx, not current_cell.down),  # South
                (cy, cx - 1, not current_cell.left),  # West
                (cy, cx + 1, not current_cell.right),  # East
            ]

            for ny, nx, is_open in directions:
                # Note: ny is checked against rows, nx against cols
                if is_open and 0 <= ny < rows and 0 <= nx < cols:
                    if (ny, nx) not in visited:
                        heappush(pq, (dist + 1, (ny, nx), path + [(ny, nx)]))
        return [(0, 0)]
        # -------------------------------------------------------------

    def gen_grid(self, maze: Maze) -> None:
        """Generate visual elements for the maze based on cell structure.

        Creates visual representation by mapping cell data to appropriate
        tile characters. Handles corners, edges, and internal junctions.
        Populates the maze's element list for rendering.

        Args:
            maze (Maze): The maze object to populate with visual elements.
        """
        h_max: int = self.config.height * 2
        w_max: int = self.config.width * 2

        for col in range(h_max + 1):
            for row in range(w_max + 1):
                # 1. Determine the character
                shape: Optional[str] = None

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
        """Convert a cell column position to horizontal rendering position.

        Args:
            pos (int): The cell column position.
            x_shift (int): Horizontal rendering offset.

        Returns:
            int: The horizontal screen position.
        """
        result: int = pos * 2 + 1 + x_shift
        return result

    def get_vertical_cell_pos(self, pos: int, y_shift: int) -> int:
        """Convert a cell row position to vertical rendering position.

        Args:
            pos (int): The cell row position.
            y_shift (int): Vertical rendering offset.

        Returns:
            int: The vertical screen position.
        """
        result: int = pos * 2 + 1 + y_shift
        return result

    def get_near_element(
        self, element: Element, elements: List[Element], directions: int
    ) -> Optional[str]:
        """Get the character of an adjacent element in a specified direction.

        Args:
            element (Element): The reference element.
            elements (List[Element]): List of all elements to search.
            directions (int): Direction to search (0=up, 1=right, 2=down, 3=left).

        Returns:
            Optional[str]: The shape of the adjacent element, or None if not found.
        """

        target_x: int = -1
        target_y: int = -1

        if directions == 0:
            target_x = element.x
            target_y = element.y - 1

        elif directions == 1:
            target_x = element.x + 1
            target_y = element.y
        elif directions == 2:
            target_x = element.x
            target_y = element.y + 1
        elif directions == 3:
            target_x = element.x - 1
            target_y = element.y

        for el in elements:
            if el.x == target_x and el.y == target_y:
                return el.shape
        return None

    def brake_walls(self, maze: Maze) -> None:
        """Clear visual elements for open walls based on cell structure.

        Updates element shapes to spaces where cells have no walls,
        effectively "breaking" the wall characters in those positions.

        Args:
            maze (Maze): The maze to process.
        """
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

    def handel_center(self, element: Element, elements: List[Element]) -> None:
        """Update a center junction element based on surrounding cell walls.

        Examines the four adjacent directions to determine which passages are open,
        then selects the appropriate T-junction or corner tile character.

        Args:
            element (Element): The center junction element to update.
            elements (List[Element]): List of all elements for context lookup.
        """
        up: int = 1 if self.get_near_element(element, elements, 0) != " " else 0
        down: int = 2 if self.get_near_element(element, elements, 2) != " " else 0
        left: int = 4 if self.get_near_element(element, elements, 3) != " " else 0
        right: int = 8 if self.get_near_element(element, elements, 1) != " " else 0

        score: int = up + down + left + right

        bit_map: dict[int, str] = {
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

    def handel_corners(self, elements: List[Element]) -> None:
        """Update all junction and corner elements based on surrounding structure.

        Processes all elements that represent junctions or corners, updating them
        to the correct tile character based on which adjacent passages are open.

        Args:
            elements (List[Element]): List of all elements to process.
        """
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
