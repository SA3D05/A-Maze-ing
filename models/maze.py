from typing import List
from models.element import Element
from models.cell import Cell


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
