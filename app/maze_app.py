from .player import Player, PlayerDirection
from .renderer import Rendrer
from .menu import Menu
from mazegen.maze_generator import MazeGenerator
from mazegen.maze import Maze, MazeConfig

from random import choice
from typing import List, Optional
from sys import argv
import curses


class MazeApp:
    """Main application class for the interactive maze generator and player.
    
    This class manages the curses terminal interface, menu navigation, maze generation,
    and player interaction within the maze. It coordinates all components of the
    maze application including rendering, generation, and user input handling.
    """
    
    def __init__(self) -> None:
        """Initialize the MazeApp and set up the curses terminal interface.
        
        Parses configuration from command-line arguments, initializes curses,
        calculates terminal layout, and creates the menu, maze, and renderer.
        
        Raises:
            SystemExit: If configuration file is missing, invalid, or terminal is too small.
        """
        self.error: Optional[str] = None
        try:
            if len(argv) < 2:
                raise Exception("Missing config file")
            elif len(argv) > 2:
                raise Exception("Too many arguments")
        except Exception as e:
            print(e)
            exit()

        try:
            self.config = MazeConfig()
            self.config.parse(argv[1])
        except Exception:
            print("Config file error")
            exit()

        self.sections: List[str] = [
            "Generate",
            "With steps",
            "Player mode",
            "Show/Hide",
            "Change colours",
            "Exit",
        ]

        self.__setup_curses()

        self.term_height, self.term_width = self.stdscr.getmaxyx()

        self.maze_height: int = self.config.height * 2 + 1
        self.maze_width: int = self.config.width * 2 + 1

        self.menu_height: int = 3 * len(self.sections)
        self.menu_width: int = 22
        self.menu_yshift = 0
        if self.menu_height > self.maze_height:
            self.menu_yshift = (self.term_height // 2) - (self.menu_height // 2)
        else:
            self.menu_yshift = (self.maze_height // 2) - (self.menu_height // 2)
        self.menu_xshift: int = (self.term_width // 2) + 2

        self.maze_yshift: int = (self.term_height // 2) - (self.maze_height // 2)
        self.maze_xshift: int = (self.term_width // 2) - (self.maze_width) - 2

        try:
            if (
                self.menu_height + 2 > self.term_height
                or self.maze_height + 2 > self.term_height
            ):
                raise Exception()
            if self.menu_width + 10 + self.maze_width > self.term_width:
                raise Exception()
            if self.maze_xshift <= 2 or self.maze_yshift <= 2:
                raise Exception()

        except Exception:
            print("terminal size error")
            exit()

        self.menu: Menu = Menu(self.menu_yshift, self.menu_xshift)
        self.rendrer: Rendrer = Rendrer(self.stdscr)
        self.generator: MazeGenerator = MazeGenerator(self.config)
        self.maze: Maze = Maze(self.maze_yshift, self.maze_xshift)

        for section in self.sections:
            self.menu.add_section(section)
        self.show_hide: bool = False
        self.duration: float = 0.001
        self.current_color_id: int = 1
        self.running: bool = False

    def run(self) -> None:
        """Start the main application loop.
        
        Displays the menu and enters the main event loop, handling user input for
        maze generation, stepping through generation, player mode, path toggling,
        color changing, and application exit. Gracefully handles terminal errors
        and keyboard interrupts.
        """
        try:
            self.rendrer.render_menu(self.menu)
            self.generator.gen_grid(self.maze)
            self.rendrer.render_maze(
                self.maze, self.duration, self.current_color_id, self.show_hide
            )
            # GAME LOOOOOOOOOOOOOOOOOOOOP
            while True:
                key = self.stdscr.getch()
                if key == curses.KEY_RESIZE:
                    raise Exception(
                        "Please do not resize the terminal or i will kill you"
                    )
                elif key == ord("\n"):
                    match self.menu.get_selected_index():
                        # generate
                        case 0:
                            self.running = True
                            self.rendrer.erase_maze(self.maze)
                            self.generator.generate(self.maze, self.config.is_perfect)
                            output_file = getattr(
                                self.config, "output_file", "maze.txt"
                            )

                            self.generator.save_maze(
                                self.generator.last_grid,
                                self.config.width,
                                self.config.height,
                                self.config.entry,
                                self.config.exit,
                                self.generator.last_path,
                                output_file,
                            )

                            self.generator.gen_grid(self.maze)
                            self.generator.brake_walls(self.maze)
                            self.generator.handel_corners(self.maze.get_elements())
                            self.rendrer.render_maze(
                                self.maze,
                                self.duration,
                                self.current_color_id,
                                self.show_hide,
                            )

                        # generate with steps
                        case 1:
                            self.running = True
                            self.rendrer.erase_maze(self.maze)
                            self.generator.generate(
                                self.maze,
                                self.config.is_perfect,
                            )
                            self.generator.gen_grid(self.maze)
                            self.rendrer.render_maze(
                                self.maze,
                                self.duration,
                                self.current_color_id,
                                self.show_hide,
                            )
                            self.generator.brake_walls(self.maze)
                            self.rendrer.render_maze(
                                self.maze,
                                self.duration,
                                self.current_color_id,
                                self.show_hide,
                            )
                            self.generator.handel_corners(self.maze.get_elements())
                            self.rendrer.render_maze(
                                self.maze,
                                self.duration,
                                self.current_color_id,
                                self.show_hide,
                            )

                        # play
                        case 2:
                            if not self.running:
                                continue
                            old_show_hide = self.show_hide
                            show_hide = False
                            player = Player(
                                self.config.entry[0],
                                self.config.entry[1],
                                self.maze.y_shift,
                                self.maze.x_shift,
                                "@",
                            )
                            self.rendrer.render_maze(
                                self.maze,
                                self.duration,
                                self.current_color_id,
                                show_hide,
                            )
                            self.rendrer.render_player(player)
                            while True:
                                last_player_pos = (player.y, player.x)
                                player_key = self.stdscr.getch()
                                if player_key == curses.KEY_RESIZE:
                                    raise Exception(
                                        "Please do not resize the terminal or i will kill you"
                                    )

                                elif player_key == ord("q") or player_key == ord("Q"):
                                    break

                                elif player_key == curses.KEY_UP:

                                    player.move(
                                        PlayerDirection.UP, self.maze.get_cells()
                                    )
                                    self.rendrer.render_player(player, last_player_pos)

                                elif player_key == curses.KEY_DOWN:
                                    player.move(
                                        PlayerDirection.DOWN, self.maze.get_cells()
                                    )
                                    self.rendrer.render_player(player, last_player_pos)

                                elif player_key == curses.KEY_LEFT:
                                    player.move(
                                        PlayerDirection.LEFT, self.maze.get_cells()
                                    )
                                    self.rendrer.render_player(player, last_player_pos)

                                elif player_key == curses.KEY_RIGHT:
                                    player.move(
                                        PlayerDirection.RIGHT, self.maze.get_cells()
                                    )
                                    self.rendrer.render_player(player, last_player_pos)

                                if (player.y, player.x) == self.config.exit:
                                    break
                                curses.flushinp()

                            show_hide = old_show_hide
                            self.rendrer.render_maze(
                                self.maze,
                                self.duration,
                                self.current_color_id,
                                self.show_hide,
                            )

                        # show/hide
                        case 3:
                            if not self.running:
                                continue
                            self.show_hide = not self.show_hide
                            self.rendrer.render_maze(
                                self.maze,
                                0,
                                self.current_color_id,
                                self.show_hide,
                            )

                        # change color
                        case 4:
                            old_color = self.current_color_id
                            while self.current_color_id == old_color:
                                self.current_color_id = choice([1, 5, 10, 15, 20])
                            self.rendrer.render_maze(
                                self.maze,
                                self.duration,
                                self.current_color_id,
                                self.show_hide,
                            )

                        # Exit
                        case 5:
                            self.__dispose_curses()
                            exit()

                elif key == curses.KEY_DOWN:
                    self.menu.move_down()
                    self.rendrer.render_menu(self.menu)
                elif key == curses.KEY_UP:
                    self.menu.move_up()
                    self.rendrer.render_menu(self.menu)
                curses.flushinp()
        except Exception as e:
            self.error = str(e)
        except KeyboardInterrupt:
            self.error = "Quit the program"
        finally:
            self.__dispose_curses()
            if self.error:
                print(self.error)

    def __setup_curses(self) -> None:
        """Initialize the curses terminal environment.
        
        Sets up terminal modes, color pairs, and custom colors for the maze
        visualization. Configures the curses library for interactive input and
        custom color support.
        """
        self.stdscr = curses.initscr()  # Start curses
        self.stdscr.keypad(True)  # Enable arrow keys
        curses.noecho()  # Don't print keys pressed to screen
        curses.cbreak()  # React to keys instantly (no Enter needed)
        curses.curs_set(0)  # hide curses
        curses.start_color()
        curses.use_default_colors()

        curses.init_color(20, 200, 800, 1000)  # Sky Blue
        curses.init_color(21, 950, 950, 1000)  # Pure Ice White
        curses.init_color(22, 500, 950, 1000)  # Bright Teal
        curses.init_color(23, 700, 850, 1000)  # Periwinkle
        curses.init_color(24, 1000, 500, 600)  # Pastel Watermelon

        curses.init_color(25, 1000, 850, 600)  # Creamy Peach
        curses.init_color(26, 1000, 400, 400)  # Bright Coral
        curses.init_color(27, 1000, 950, 200)  # Laser Yellow
        curses.init_color(28, 1000, 600, 800)  # Bright Orchid
        curses.init_color(29, 1000, 300, 0)  # Burning Orange

        curses.init_color(30, 1000, 1000, 1000)  # Full White
        curses.init_color(31, 800, 850, 900)  # Bright Silver
        curses.init_color(32, 400, 600, 1000)  # Tech Blue
        curses.init_color(33, 1000, 400, 0)  # Safety Orange
        curses.init_color(34, 1000, 100, 300)  # Neon Red

        curses.init_color(35, 400, 1000, 200)  # Spring Green
        curses.init_color(36, 0, 1000, 600)  # Turquoise Green
        curses.init_color(37, 700, 1000, 700)  # Seafoam Mint
        curses.init_color(38, 600, 1000, 0)  # Bright Chartreuse
        curses.init_color(39, 900, 1000, 300)  # Lemon Lime

        curses.init_color(40, 0, 960, 1000)  # Electric Cyan
        curses.init_color(41, 1000, 200, 600)  # Bright Hot Pink
        curses.init_color(42, 800, 650, 1000)  # Vivid Lavender
        curses.init_color(43, 1000, 600, 200)  # Sunset Orange
        curses.init_color(44, 700, 300, 1000)  # Bright Violet

        for i in range(25):
            curses.init_pair(i + 1, 20 + i, -1)

    def __dispose_curses(self) -> None:
        """Clean up and restore the terminal to its normal state.
        
        Disables curses mode and returns the terminal to normal operation.
        Should be called before exiting the application.
        """
        self.stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()  # Close the window and return to normal terminal
