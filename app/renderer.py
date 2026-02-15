from .player import Player
from .menu import Menu

from mazegen.tile import Tile
from mazegen.maze import Maze

from curses import window, color_pair
from typing import Optional, Tuple
from time import sleep


class Rendrer:
    """Handles rendering of maze, player, and menu elements to the terminal.

    This class manages all visual output for the maze application using curses,
    including maze layout, player position, and menu interface.

    Attributes:
        stdscr (window): The curses window object for terminal output.
    """

    def __init__(self, stdscr: window) -> None:
        """Initialize the Renderer with a curses window.

        Args:
            stdscr (window): The curses window object to render output to.
        """
        self.stdscr: window = stdscr

    def render_maze(
        self, maze: Maze, duration: float, color_id: int, show_path: bool
    ) -> None:
        """Render the maze to the terminal with optional colored output.

        Draws each element of the maze with appropriate colors and delays,
        optionally showing or hiding the solution path.

        Args:
            maze (Maze):
            The maze object containing elements to render.
            duration (float):
            Sleep duration (in seconds) between rendering each element.
            color_id (int):
            The base color pair ID for rendering.
            show_path (bool):
            Whether to display the solution path.
        """
        for element in maze.get_elements():

            current_attr: int = color_pair(color_id)
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

    def erase_maze(self, maze: Maze) -> None:
        """Clear the maze from the terminal by rendering spaces over it.

        Args:
            maze (Maze): The maze object containing elements to erase.
        """
        for element in maze.get_elements():
            self.stdscr.addch(
                element.y,
                element.x,
                " ",
            )
            sleep(0.001)
            self.stdscr.refresh()

    def render_player(
        self,
        player: Player,
        last_pos: Optional[Tuple[int, int]] = None,
    ) -> None:
        """Render the player at its current position and
        erase it from the last position.

        Args:
            player (Player): The player object to render.
            last_pos (Optional[Tuple[int, int]]):
            The previous (y, x) position of the player.
                If provided, that position will be cleared. Defaults to None.
        """
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

    def render_menu(self, menu: Menu) -> None:
        """Render the menu and all its sections to the terminal.

        Args:
            menu (Menu): The menu object containing sections to render.
        """
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
