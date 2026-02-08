from typing import List
from models.element import Element
from models.tile import Tile


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
