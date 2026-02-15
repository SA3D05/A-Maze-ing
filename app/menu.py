from mazegen.element import Element
from mazegen.tile import Tile

from typing import List


class MenuSection:
    """
    A class representing a section of a menu with a bordered box layout.
    This class manages the visual representation of a menu section,
    including its position,
    selection state, and the elements that compose its border and structure.
    Attributes:
        text (str): The text content displayed in the menu section.
        selected (bool): Whether the menu section is currently selected.
        index (int): The index position of this menu section.
        v_shift (int): Vertical shift offset for positioning elements.
        h_shift (int): Horizontal shift offset for positioning elements.
        elements (List[Element]):
        Internal list of elements that make up the menu section.
        width (int): The width of the menu section (default: 22).
        height (int): The height of the menu section (default: 3).
    """

    def __init__(
        self, text: str, index: int, selected: bool, v_shift: int, h_shift: int
    ) -> None:
        """Initialize a MenuSection.
        Args:
            text (str): The text to display in the menu section.
            index (int): The index position of this section within the menu.
            selected (bool): Whether this section is initially selected.
            v_shift (int): Vertical offset for positioning the section.
            h_shift (int): Horizontal offset for positioning the section.
        """
        self.text: str = text
        self.selected: bool = selected
        self.index: int = index
        self.elements: List[Element] = []
        self.v_shift: int = v_shift
        self.h_shift: int = h_shift
        self.width: int = 22
        self.height: int = 3

    def get_elements(self) -> List[Element]:
        """Get the list of elements that compose this menu section's border.
        Returns:
            List[Element]: List of Element objects making up the section box.
        """
        return self.elements

    def toggle(self) -> None:
        """Toggle the selection state of this menu section."""
        self.selected = not self.selected

    def fill_elements(self) -> None:
        """Generate and populate the elements
        list to create a bordered box layout.
        Creates border elements (corners, edges)
        using the appropriate tile graphics
        and positions them based on the section's offset and dimensions.
        """
        for column in range(self.height):  # 3 in hight
            for row in range(self.width):  # 22 in width
                if column == 0 and row == 0:
                    self.elements.append(
                        Element(
                            column + self.v_shift,
                            row + self.h_shift,
                            Tile.LEFT_TOP.value,
                        )
                    )
                elif column == 0 and row == self.width - 1:
                    self.elements.append(
                        Element(
                            column + self.v_shift,
                            row + self.h_shift,
                            Tile.RIGHT_TOP.value,
                        )
                    )
                elif column == self.height - 1 and row == 0:
                    self.elements.append(
                        Element(
                            column + self.v_shift,
                            row + self.h_shift,
                            Tile.LEFT_BOTTOM.value,
                        )
                    )
                elif column == self.height - 1 and row == self.width - 1:
                    self.elements.append(
                        Element(
                            column + self.v_shift,
                            row + self.h_shift,
                            Tile.RIGHT_BOTTOM.value,
                        )
                    )
                elif column == 0 or column == self.height - 1:
                    self.elements.append(
                        Element(
                            column + self.v_shift,
                            row + self.h_shift,
                            Tile.HORIZONTAL.value,
                        )
                    )
                elif row == 0 or row == self.width - 1:
                    self.elements.append(
                        Element(
                            column + self.v_shift,
                            row + self.h_shift,
                            Tile.VERTICAL.value,
                        )
                    )


class Menu:
    """
    A class representing a menu with multiple selectable sections.
    This class manages a vertical menu with sections
    that can be navigated using
    move_up() and move_down() methods.
    It tracks which section is currently selected
    and handles the visual positioning of menu sections.
    Attributes:
        vertical_shift (int): The vertical offset for menu positioning.
        horizontal_shift (int): The horizontal offset for menu positioning.
        selected_index (int): The index of the currently selected menu section.
        sections (List[MenuSection]):
        List of menu sections contained in this menu.
    """

    def __init__(self, vertical_shift: int, horizontal_shift: int) -> None:
        """Initialize a Menu with positioning offsets.
        Args:
            vertical_shift (int): The vertical offset for menu positioning.
            horizontal_shift (int): The horizontal offset for menu positioning.
        """
        self.vertical_shift: int = vertical_shift
        self.horizontal_shift: int = horizontal_shift
        self.selected_index: int = 0
        self.sections: List[MenuSection] = []

    def get_sections(self) -> List[MenuSection]:
        """Get all menu sections.
        Returns:
            List[MenuSection]: List of all sections in the menu.
        """
        return self.sections

    def get_selected_index(self) -> int:
        """Get the index of the currently selected section.
        Returns:
            int: Index of the selected section.
        """
        return self.selected_index

    def add_section(self, text: str) -> None:
        """Add a new section to the menu.
        Creates a new MenuSection with the given text
        and populates its elements.
        Updates the vertical position for the next section to be added.
        Args:
            text (str): The text to display in the new section.
        """
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

    def move_up(self) -> None:
        """Move the selection upward through the menu sections.
        Wraps around to the last section if already at the first section.
        """
        selected_index: int = self.selected_index
        target_index: int = selected_index - 1

        if target_index < 0:
            self.sections[selected_index].toggle()
            self.sections[-1].toggle()
            self.selected_index = len(self.sections) - 1
        else:
            self.sections[self.selected_index].toggle()
            self.sections[self.selected_index - 1].toggle()
            self.selected_index -= 1

    def move_down(self) -> None:
        """Move the selection downward through the menu sections.
        Wraps around to the first section if already at the last section.
        """
        selected_index = self.selected_index
        target_index: int = selected_index + 1

        if target_index >= len(self.sections):
            self.sections[selected_index].toggle()
            self.sections[0].toggle()
            self.selected_index = 0
        else:
            self.sections[selected_index].toggle()
            self.sections[target_index].toggle()
            self.selected_index += 1
