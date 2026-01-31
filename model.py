from curses import window
from enum import Enum
from typing import List, Dict, Union, Any, Set, Optional, Tuple
from deb import pdeb


class Cell:
    def __init__(
        self, y: int, x: int, up: bool, down: bool, left: bool, right: bool
    ) -> None:
        self.y = y
        self.x = x
        self.up = up
        self.down = down
        self.left = left
        self.right = right


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

    def __init__(
        self,
        cells: List[Cell],
        height: int,
        width: int,
    ) -> None:
        """Initialize the Maze with cells, dimensions, and optional shifts.
        Args:
            cells (List[Cell]): List of Cell objects representing the maze structure.
            height (int): Height of the maze in cells.
            width (int): Width of the maze in cells.
            horizontal_shift (int, optional): Horizontal shift for rendering. Defaults to 0.
            vertical_shift (int, optional): Vertical shift for rendering. Defaults to 0.
        """
        self.cells = cells
        self.height = height
        self.width = width
        self._elements: List[Element] = []

    def add_element(self, element_y: int, element_x: int, element_sprite) -> None:
        self._elements.append(Element(element_y, element_x, element_sprite))

    def get_elements(self) -> List[Element]:
        return self._elements


class MazeConfig:
    def __init__(
        self,
        height: int,
        width: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        output: str,
        perfect: bool,
        y_shift: int,
        x_shift: int,
    ) -> None:

        self.height: int = height
        self.width: int = width
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.output: str = output
        self.perfect: bool = perfect
        self.y_shift: int = y_shift
        self.x_shift: int = x_shift


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
        self.selected_index = 1

    def get_sections(self) -> List[MenuSection]:
        return self.sections

    def get_selected_index(self) -> int:
        return self.selected_index

    def add_section(self, text):
        self.sections.append(
            MenuSection(
                text,
                len(self.sections),
                len(self.sections) == 2,
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
            pdeb("you cant move up")
        else:
            self.sections[self.selected_index].toggle()
            self.sections[self.selected_index - 1].toggle()
            self.selected_index -= 1

    def move_down(self):

        selected_index = self.selected_index
        target_index = selected_index + 1

        if target_index >= len(self.sections):
            pdeb("you cant move down")
        else:
            self.sections[selected_index].toggle()
            self.sections[target_index].toggle()
            self.selected_index += 1

    def rebuild(self, stdscr):
        pass


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
    def __init__(self, config: MazeConfig) -> None:
        self.config: MazeConfig = config

    def generate_perfect_maze(self, config: MazeConfig) -> Maze: ...

    def generate_nonperfect_maze(self, config: MazeConfig) -> Maze: ...

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
                        column + self.config.y_shift,
                        row + self.config.x_shift,
                        Tile.LEFT_TOP.value,
                    )
                elif column == 0 and row == self.config.width * 2:
                    maze.add_element(
                        column + self.config.y_shift,
                        row + self.config.x_shift,
                        Tile.RIGHT_TOP.value,
                    )
                elif column == self.config.height * 2 and row == 0:
                    maze.add_element(
                        column + self.config.y_shift,
                        row + self.config.x_shift,
                        Tile.LEFT_BOTTOM.value,
                    )
                elif column == self.config.height * 2 and row == self.config.width * 2:
                    maze.add_element(
                        column + self.config.y_shift,
                        row + self.config.x_shift,
                        Tile.RIGHT_BOTTOM.value,
                    )

                elif x_even and column == 0:
                    maze.add_element(
                        column + self.config.y_shift,
                        row + self.config.x_shift,
                        Tile.T_DOWN.value,
                    )
                elif x_even and column == self.config.height * 2:
                    maze.add_element(
                        column + self.config.y_shift,
                        row + self.config.x_shift,
                        Tile.T_UP.value,
                    )

                elif y_even:
                    if row == 0:
                        maze.add_element(
                            column + self.config.y_shift,
                            row + self.config.x_shift,
                            Tile.T_RIGHT.value,
                        )
                    elif row == self.config.width * 2:
                        maze.add_element(
                            column + self.config.y_shift,
                            row + self.config.x_shift,
                            Tile.T_LEFT.value,
                        )

                    elif x_even:
                        maze.add_element(
                            column + self.config.y_shift,
                            row + self.config.x_shift,
                            Tile.CENTER.value,
                        )

                    else:
                        maze.add_element(
                            column + self.config.y_shift,
                            row + self.config.x_shift,
                            Tile.HORIZONTAL.value,
                        )

                elif not y_even and x_even:
                    maze.add_element(
                        column + self.config.y_shift,
                        row + self.config.x_shift,
                        Tile.VERTICAL.value,
                    )

                else:
                    maze.add_element(
                        column + self.config.y_shift,
                        row + self.config.x_shift,
                        " ",
                    )

    def get_horizontal_cell_pos(self, pos) -> int:
        result: int = (pos * 2) + 1 + self.config.x_shift
        return result

    def get_vertical_cell_pos(self, pos) -> int:
        result: int = (pos * 2) + 1 + self.config.y_shift
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
        for cell in maze.cells:
            for element in maze.get_elements():
                # up
                if (
                    element.x == self.get_horizontal_cell_pos(cell.x)
                    and element.y == self.get_vertical_cell_pos(cell.y) - 1
                ):
                    if cell.up:
                        element.sprite = " "
                # right
                if element.x == self.get_horizontal_cell_pos(
                    cell.x
                ) + 1 and element.y == self.get_vertical_cell_pos(cell.y):
                    if cell.right:
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
