from enum import Enum
from typing import List
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


class MenuSection:

    def __init__(self, text: str, index: int, selected: bool = False) -> None:
        self.text = text
        self.selected = selected
        self.index = index
        self._elements: List[Element] = []
        self._width = 22
        self._height = 3

    def get_elements(self) -> List[Element]:
        return self._elements

    def toggle(self):
        self.selected = not self.selected

    def fill_elements(self, vertical_shift, horizontal_shift):
        for column in range(self._height):  # 3 in hight
            for row in range(self._width):  # 22 in width
                # corners
                if column == 0 and row == 0:
                    self._elements.append(
                        Element(
                            column + vertical_shift,
                            row + horizontal_shift,
                            Tile.LEFT_TOP.value,
                        )
                    )
                elif column == 0 and row == self._width - 1:
                    self._elements.append(
                        Element(
                            column + vertical_shift,
                            row + horizontal_shift,
                            Tile.RIGHT_TOP.value,
                        )
                    )
                elif column == self._height - 1 and row == 0:
                    self._elements.append(
                        Element(
                            column + vertical_shift,
                            row + horizontal_shift,
                            Tile.LEFT_BOTTOM.value,
                        )
                    )
                elif column == self._height - 1 and row == self._width - 1:
                    self._elements.append(
                        Element(
                            column + vertical_shift,
                            row + horizontal_shift,
                            Tile.RIGHT_BOTTOM.value,
                        )
                    )
                elif column == 0 or column == self._height - 1:
                    self._elements.append(
                        Element(
                            column + vertical_shift,
                            row + horizontal_shift,
                            Tile.HORIZONTAL.value,
                        )
                    )
                elif row == 0 or row == self._width - 1:
                    self._elements.append(
                        Element(
                            column + vertical_shift,
                            row + horizontal_shift,
                            Tile.VERTICAL.value,
                        )
                    )


class Menu:
    def __init__(
        self,
        vertical_shift: int,
        horizontal_shift: int,
    ) -> None:
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
            MenuSection(text, len(self.sections), len(self.sections) == 0)
        )

    def build(self):
        v_shift = self.vertical_shift
        for section in self.sections:
            section.fill_elements(
                v_shift,
                self.horizontal_shift,
            )
            v_shift += 3

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
