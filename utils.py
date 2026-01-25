from model import Element, Cell, Tile
from deb import pdeb

from typing import List, Dict, Union, Any, Set


class Maze:

    def __init__(
        self,
        cells: List[Cell],
        height: int,
        width: int,
        horizontal_shift: int = 0,
        vertical_shift: int = 0,
    ) -> None:
        self.cells = cells
        self.height = height
        self.width = width
        self.horizontal_shift = horizontal_shift
        self.vertical_shift = vertical_shift
        self._elements: List[Element] = []

    def get_elements(self) -> List[Element]:
        return self._elements

    def gen_grid(self):

        for column in range(self.height * 2 + 1):
            y_even = True if column % 2 == 0 else False
            for row in range(self.width * 2 + 1):
                x_even = True if row % 2 == 0 else False
                # corners
                if column == 0 and row == 0:
                    self._elements.append(
                        Element(
                            column + self.vertical_shift,
                            row + self.horizontal_shift,
                            Tile.LEFT_TOP.value,
                        )
                    )
                elif column == 0 and row == self.width * 2:
                    self._elements.append(
                        Element(
                            column + self.vertical_shift,
                            row + self.horizontal_shift,
                            Tile.RIGHT_TOP.value,
                        )
                    )
                elif column == self.height * 2 and row == 0:
                    self._elements.append(
                        Element(
                            column + self.vertical_shift,
                            row + self.horizontal_shift,
                            Tile.LEFT_BOTTOM.value,
                        )
                    )
                elif column == self.height * 2 and row == self.width * 2:
                    self._elements.append(
                        Element(
                            column + self.vertical_shift,
                            row + self.horizontal_shift,
                            Tile.RIGHT_BOTTOM.value,
                        )
                    )

                elif x_even and column == 0:
                    self._elements.append(
                        Element(
                            column + self.vertical_shift,
                            row + self.horizontal_shift,
                            Tile.T_DOWN.value,
                        )
                    )
                elif x_even and column == self.height * 2:
                    self._elements.append(
                        Element(
                            column + self.vertical_shift,
                            row + self.horizontal_shift,
                            Tile.T_UP.value,
                        )
                    )

                elif y_even:
                    if row == 0:
                        self._elements.append(
                            Element(
                                column + self.vertical_shift,
                                row + self.horizontal_shift,
                                Tile.T_RIGHT.value,
                            )
                        )
                    elif row == self.width * 2:
                        self._elements.append(
                            Element(
                                column + self.vertical_shift,
                                row + self.horizontal_shift,
                                Tile.T_LEFT.value,
                            )
                        )
                    elif x_even:
                        self._elements.append(
                            Element(
                                column + self.vertical_shift,
                                row + self.horizontal_shift,
                                Tile.CENTER.value,
                            )
                        )
                    else:
                        self._elements.append(
                            Element(
                                column + self.vertical_shift,
                                row + self.horizontal_shift,
                                Tile.HORIZONTAL.value,
                            )
                        )
                elif not y_even and x_even:
                    self._elements.append(
                        Element(
                            column + self.vertical_shift,
                            row + self.horizontal_shift,
                            Tile.VERTICAL.value,
                        )
                    )
                else:
                    self._elements.append(
                        Element(
                            column + self.vertical_shift,
                            row + self.horizontal_shift,
                            " ",
                        )
                    )

    def brake_walls(self):

        for cell in self.cells:
            for element in self._elements:
                # up
                if (
                    element.x == self.get_cell_pos(cell.x)
                    and element.y == self.get_cell_pos(cell.y) - 1
                ):
                    if cell.up:
                        element.sprite = " "
                # right
                if element.x == self.get_cell_pos(
                    cell.x
                ) + 1 and element.y == self.get_cell_pos(cell.y):
                    if cell.right:
                        element.sprite = " "
                # up and right  for the next cell handel the previes down and left so we dont actily need them

    def get_cell_pos(self, pos) -> int:
        result: int = (pos * 2) + 1 + self.shift
        return result

    def get_up_element(self, element: Element):
        for el in self._elements:
            if el.x == element.x and el.y == element.y - 1:
                return el.sprite
        return None

    def get_down_element(self, element: Element):
        for el in self._elements:
            if el.x == element.x and el.y == element.y + 1:
                return el.sprite
        return None

    def get_left_element(self, element: Element):
        for el in self._elements:
            if el.x == element.x - 1 and el.y == element.y:
                return el.sprite
        return None

    def get_right_element(self, element: Element):
        for el in self._elements:
            if el.x == element.x + 1 and el.y == element.y:
                return el.sprite
        return None

    def handel_corners(self):
        for element in self._elements:
            if element.sprite == Tile.CENTER.value:
                self.handel_center(element)
            elif element.sprite == Tile.T_DOWN.value:
                if self.get_down_element(element) == " ":
                    element.sprite = Tile.HORIZONTAL.value

            elif element.sprite == Tile.T_UP.value:
                if self.get_up_element(element) == " ":
                    element.sprite = Tile.HORIZONTAL.value

            elif element.sprite == Tile.T_LEFT.value:
                if self.get_left_element(element) == " ":
                    element.sprite = Tile.VERTICAL.value

            elif element.sprite == Tile.T_RIGHT.value:
                if self.get_right_element(element) == " ":
                    element.sprite = Tile.VERTICAL.value

    def handel_center(self, element: Element):
        up = 1 if self.get_up_element(element) != " " else 0
        down = 2 if self.get_down_element(element) != " " else 0
        left = 4 if self.get_left_element(element) != " " else 0
        right = 8 if self.get_right_element(element) != " " else 0

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
