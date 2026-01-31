from model import Element, Cell, Tile
from typing import List

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
        """Generates the full grid with all initial junction sprites."""
        self._elements = [] 
        for column in range(self.height * 2 + 1):
            y_even = column % 2 == 0
            for row in range(self.width * 2 + 1):
                x_even = row % 2 == 0
                
                # Assign visual sprites based on grid position
                if column == 0 and row == 0:
                    sprite = Tile.LEFT_TOP.value
                elif column == 0 and row == self.width * 2:
                    sprite = Tile.RIGHT_TOP.value
                elif column == self.height * 2 and row == 0:
                    sprite = Tile.LEFT_BOTTOM.value
                elif column == self.height * 2 and row == self.width * 2:
                    sprite = Tile.RIGHT_BOTTOM.value
                elif x_even and column == 0:
                    sprite = Tile.T_DOWN.value
                elif x_even and column == self.height * 2:
                    sprite = Tile.T_UP.value
                elif y_even and row == 0:
                    sprite = Tile.T_RIGHT.value
                elif y_even and row == self.width * 2:
                    sprite = Tile.T_LEFT.value
                elif y_even and x_even:
                    sprite = Tile.CENTER.value
                elif y_even:
                    sprite = Tile.HORIZONTAL.value
                elif x_even:
                    sprite = Tile.VERTICAL.value
                else:
                    sprite = " "

                self._elements.append(
                    Element(column + self.vertical_shift, row + self.horizontal_shift, sprite)
                )

    def brake_walls(self):
        """Carves paths by removing walls internally while protecting the border."""
        for cell in self.cells:
            # Check for False (path carved) and ensure it's not a border wall
            if not cell.up and cell.y > 0:
                self._remove_sprite_at(self.get_horizontal_cell_pos(cell.x), self.get_vertical_cell_pos(cell.y) - 1)
            if not cell.down and cell.y < self.height - 1:
                self._remove_sprite_at(self.get_horizontal_cell_pos(cell.x), self.get_vertical_cell_pos(cell.y) + 1)
            if not cell.left and cell.x > 0:
                self._remove_sprite_at(self.get_horizontal_cell_pos(cell.x) - 1, self.get_vertical_cell_pos(cell.y))
            if not cell.right and cell.x < self.width - 1:
                self._remove_sprite_at(self.get_horizontal_cell_pos(cell.x) + 1, self.get_vertical_cell_pos(cell.y))

    def _remove_sprite_at(self, x: int, y: int):
        for element in self._elements:
            if element.x == x and element.y == y:
                element.sprite = " "
                break

    def get_horizontal_cell_pos(self, pos) -> int:
        return (pos * 2) + 1 + self.horizontal_shift

    def get_vertical_cell_pos(self, pos) -> int:
        return (pos * 2) + 1 + self.vertical_shift

    # Helper methods to check surrounding wall connectivity
    def get_up_element(self, element: Element):
        return next((el.sprite for el in self._elements if el.x == element.x and el.y == element.y - 1), None)

    def get_down_element(self, element: Element):
        return next((el.sprite for el in self._elements if el.x == element.x and el.y == element.y + 1), None)

    def get_left_element(self, element: Element):
        return next((el.sprite for el in self._elements if el.x == element.x - 1 and el.y == element.y), None)

    def get_right_element(self, element: Element):
        return next((el.sprite for el in self._elements if el.x == element.x + 1 and el.y == element.y), None)

    def handel_corners(self):
        """Refines edge junctions into straight lines if paths were carved through them."""
        for element in self._elements:
            if element.sprite == Tile.CENTER.value:
                self.handel_center(element)
            elif element.sprite == Tile.T_DOWN.value and self.get_down_element(element) in [" ", None]:
                element.sprite = Tile.HORIZONTAL.value
            elif element.sprite == Tile.T_UP.value and self.get_up_element(element) in [" ", None]:
                element.sprite = Tile.HORIZONTAL.value
            elif element.sprite == Tile.T_LEFT.value and self.get_left_element(element) in [" ", None]:
                element.sprite = Tile.VERTICAL.value
            elif element.sprite == Tile.T_RIGHT.value and self.get_right_element(element) in [" ", None]:
                element.sprite = Tile.VERTICAL.value

    def handel_center(self, element: Element):
        """Bit-score logic to determine the correct junction character."""
        up = 1 if self.get_up_element(element) not in [" ", None] else 0
        down = 2 if self.get_down_element(element) not in [" ", None] else 0
        left = 4 if self.get_left_element(element) not in [" ", None] else 0
        right = 8 if self.get_right_element(element) not in [" ", None] else 0
        
        score = up + down + left + right
        
        BIT_MAP = {
            1: Tile.SHORT_UP.value, 2: Tile.SHORT_DOWN.value, 3: Tile.VERTICAL.value,
            4: Tile.SHORT_LEFT.value, 5: Tile.RIGHT_BOTTOM.value, 6: Tile.RIGHT_TOP.value,
            7: Tile.T_LEFT.value, 8: Tile.SHORT_RIGHT.value, 9: Tile.LEFT_BOTTOM.value,
            10: Tile.LEFT_TOP.value, 11: Tile.T_RIGHT.value, 12: Tile.HORIZONTAL.value,
            13: Tile.T_UP.value, 14: Tile.T_DOWN.value, 15: Tile.CENTER.value,
        }
        element.sprite = BIT_MAP.get(score, " ")
