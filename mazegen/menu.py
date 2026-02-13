from .element import Element
from .tile import Tile

from typing import List


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

        if target_index >= len(self.sections):
            self.sections[selected_index].toggle()
            self.sections[0].toggle()
            self.selected_index = 0
        else:
            self.sections[selected_index].toggle()
            self.sections[target_index].toggle()
            self.selected_index += 1
