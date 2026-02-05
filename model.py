from curses import window
from enum import Enum
import random
from typing import List, Tuple
from deb import pdeb


class Cell:
    def __init__(
        self,
        y: int,
        x: int,
        up: bool,
        right: bool,
        down: bool,
        left: bool,
    ) -> None:
        self.y = y
        self.x = x
        self.up = up
        self.right = right
        self.down = down
        self.left = left


class Element:
    def __init__(
        self,
        y: int,
        x: int,
        sprite: str,
    ):
        self.y = y
        self.x = x
        self.sprite = sprite


class Maze:

    def __init__(self, y_shift: int, x_shift: int) -> None:
        self.y_shift = y_shift
        self.x_shift = x_shift

        self._elements: List[Element] = list()
        self._cells = list()

    def add_element(self, element_y: int, element_x: int, element_sprite) -> None:
        self._elements.append(Element(element_y, element_x, element_sprite))

    def get_elements(self) -> List[Element]:
        return self._elements

    def get_cells(self) -> List[Cell]:
        return self._cells

    def update_cells(self, new_cells: List[Cell]):
        self._cells.clear()
        self._elements.clear()
        self._cells = new_cells


class MazeConfig:
    def __init__(
        self,
    ) -> None:

        self.height: int = 10
        self.width: int = 10
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (9, 9)
        self.output: str = "output.txt"
        self.perfect: bool = True
        maze_height = self.height * 2 + 1
        maze_width = self.width * 2 + 1

    def parse_config(self, config_file: str):
        config_info = {}
        with open(config_file, "r") as fd:
            for line in fd:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    config_info[key.strip().upper()] = value.strip()
            self.width = int(config_info.get("WIDTH", 10))
            self.height = int(config_info.get("HEIGHT", 10))
            is_perfect_str = config_info.get("PERFECT", "TRUE").strip().upper()
            self.is_perfect = is_perfect_str == "TRUE"
            self.entry = tuple([config_info.get("ENTRY", "0,0").split(",")])
            self.exit = tuple([config_info.get("EXIT", "9,9").split(",")])


class MenuSection:

    def __init__(
        self, text: str, index: int, selected: bool, v_shift: int, h_shift: int
    ) -> None:
        self.text = text
        self.selected = selected
        self.index = index
        self._elements: List[Element] = []
        self._width = 22
        self._height = 3
        self.v_shift = v_shift
        self.h_shift = h_shift

    def get_elements(self) -> List[Element]:
        return self._elements

    def toggle(self):
        self.selected = not self.selected

    def fill_elements(self):
        for column in range(self._height):  # 3 in hight
            for row in range(self._width):  # 22 in width
                if column == 0 and row == 0:
                    self._elements.append(
                        Element(
                            column + self.v_shift,
                            row + self.h_shift,
                            Tile.LEFT_TOP.value,
                        )
                    )
                elif column == 0 and row == self._width - 1:
                    self._elements.append(
                        Element(
                            column + self.v_shift,
                            row + self.h_shift,
                            Tile.RIGHT_TOP.value,
                        )
                    )
                elif column == self._height - 1 and row == 0:
                    self._elements.append(
                        Element(
                            column + self.v_shift,
                            row + self.h_shift,
                            Tile.LEFT_BOTTOM.value,
                        )
                    )
                elif column == self._height - 1 and row == self._width - 1:
                    self._elements.append(
                        Element(
                            column + self.v_shift,
                            row + self.h_shift,
                            Tile.RIGHT_BOTTOM.value,
                        )
                    )
                elif column == 0 or column == self._height - 1:
                    self._elements.append(
                        Element(
                            column + self.v_shift,
                            row + self.h_shift,
                            Tile.HORIZONTAL.value,
                        )
                    )
                elif row == 0 or row == self._width - 1:
                    self._elements.append(
                        Element(
                            column + self.v_shift,
                            row + self.h_shift,
                            Tile.VERTICAL.value,
                        )
                    )


class Menu:
    def __init__(self, vertical_shift: int, horizontal_shift: int) -> None:
        self.vertical_shift: int = vertical_shift
        self.horizontal_shift: int = horizontal_shift
        self.sections: List[MenuSection] = []
        self.selected_index = 0

    def get_sections(self) -> List[MenuSection]:
        return self.sections

    def get_selected_index(self) -> int:
        return self.selected_index

    def add_section(self, text):
        self.sections.append(
            MenuSection(
                text,
                len(self.sections),
                len(self.sections) == 0,
                self.vertical_shift,
                self.horizontal_shift,
            )
        )
        self.sections[-1].fill_elements()
        self.vertical_shift += 3

    def move_up(self):

        selected_index = self.selected_index
        target_index = selected_index - 1

        if target_index < 0:
            self.sections[selected_index].toggle()
            self.sections[-1].toggle()
            self.selected_index = len(self.sections) - 1
        else:
            self.sections[self.selected_index].toggle()
            self.sections[self.selected_index - 1].toggle()
            self.selected_index -= 1

    def move_down(self):
        selected_index = self.selected_index
        target_index = selected_index + 1
        pdeb(f"selected_index: {selected_index}, target_index: {target_index}")

        if target_index >= len(self.sections):
            self.sections[selected_index].toggle()
            self.sections[0].toggle()
            self.selected_index = 0
        else:
            self.sections[selected_index].toggle()
            self.sections[target_index].toggle()
            self.selected_index += 1


class Tile(Enum):
    VERTICAL = "│"
    HORIZONTAL = "─"
    # Corners
    LEFT_TOP = "╭"
    RIGHT_TOP = "╮"
    LEFT_BOTTOM = "╰"
    RIGHT_BOTTOM = "╯"
    # Junctions
    CENTER = "┼"
    T_DOWN = "┬"
    T_UP = "┴"
    T_RIGHT = "├"
    T_LEFT = "┤"
    # Short Ends
    SHORT_UP = "╵"
    SHORT_DOWN = "╷"
    SHORT_LEFT = "╴"
    SHORT_RIGHT = "╶"


class Rendrer:
    def __init__(self, stdscr: window) -> None:
        self.stdscr: window = stdscr

    def render_maze(self, maze: Maze):

        for element in maze.get_elements():
            self.stdscr.addch(element.y, element.x, element.sprite)
        self.stdscr.refresh()

    def render_menu(self, menu: Menu):
        for section in menu.get_sections():
            for element in section.get_elements():
                self.stdscr.addch(
                    element.y,
                    element.x,
                    element.sprite if section.selected else " ",
                )

            self.stdscr.addstr(
                section.v_shift + 1,
                (section.h_shift + 1) + (20 // 2) - (len(section.text) // 2),
                section.text,
            )
        self.stdscr.refresh()


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
