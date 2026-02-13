from .player import Player
from .tile import Tile
from .maze import Maze
from .menu import Menu


from curses import window, color_pair
from typing import Optional, Tuple
from time import sleep


class Rendrer:
    def __init__(self, stdscr: window) -> None:
        self.stdscr: window = stdscr

    def render_maze(self, maze: Maze, duration: float, color_id: int, show_path: bool):
        for element in maze.get_elements():

            current_attr = color_pair(color_id)
            match element.shape:
                case Tile.BLOCK.value:
                    current_attr = color_pair(color_id + 1)
                case Tile.PATH.value:
                    current_attr = color_pair(color_id + 2)
                case Tile.ENTER.value:
                    current_attr = color_pair(color_id + 3)
                case Tile.EXIT.value:
                    current_attr = color_pair(color_id + 4)

            if show_path and element.shape == Tile.PATH.value:
                self.stdscr.addch(
                    element.y,
                    element.x,
                    element.shape,
                    current_attr,
                )
            else:
                self.stdscr.addch(
                    element.y,
                    element.x,
                    (
                        element.shape
                        if element.shape != Tile.PATH.value
                        else Tile.SPACE.value
                    ),
                    current_attr,
                )
            self.stdscr.refresh()
            sleep(duration)

    def erase_maze(self, maze: Maze):
        for element in maze.get_elements():
            self.stdscr.addch(
                element.y,
                element.x,
                " ",
            )
            sleep(0.001)
            self.stdscr.refresh()

    def render_player(self, player: Player, last_pos: Optional[Tuple[int, int]] = None):

        if last_pos is not None:
            self.stdscr.addch(
                last_pos[0] * 2 + 1 + player.y_shift,
                last_pos[1] * 2 + 1 + player.x_shift,
                Tile.SPACE.value,
            )

        self.stdscr.addch(
            player.y * 2 + 1 + player.y_shift,
            player.x * 2 + 1 + player.x_shift,
            player.shape,
        )

    def render_menu(self, menu: Menu):
        for section in menu.get_sections():
            for element in section.get_elements():
                self.stdscr.addch(
                    element.y,
                    element.x,
                    element.shape if section.selected else Tile.SPACE.value,
                )

            self.stdscr.addstr(
                section.v_shift + 1,
                (section.h_shift + 1) + (20 // 2) - (len(section.text) // 2),
                section.text,
            )
        self.stdscr.refresh()
