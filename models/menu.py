from typing import List
from models.menu_section import MenuSection


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
