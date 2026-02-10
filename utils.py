import curses
from typing import List


def init_colors():

    curses.init_color(20, 0, 960, 1000)  # Electric Cyan
    curses.init_color(21, 1000, 200, 600)  # Bright Hot Pink
    curses.init_color(22, 800, 650, 1000)  # Vivid Lavender
    curses.init_color(23, 1000, 600, 200)  # Sunset Orange
    curses.init_color(24, 700, 300, 1000)  # Bright Violet

    curses.init_color(25, 400, 1000, 200)  # Spring Green
    curses.init_color(26, 0, 1000, 600)  # Turquoise Green
    curses.init_color(27, 700, 1000, 700)  # Seafoam Mint
    curses.init_color(28, 600, 1000, 0)  # Bright Chartreuse
    curses.init_color(29, 900, 1000, 300)  # Lemon Lime

    curses.init_color(30, 200, 800, 1000)  # Sky Blue
    curses.init_color(31, 950, 950, 1000)  # Pure Ice White
    curses.init_color(32, 500, 950, 1000)  # Bright Teal
    curses.init_color(33, 700, 850, 1000)  # Periwinkle
    curses.init_color(34, 1000, 500, 600)  # Pastel Watermelon

    curses.init_color(35, 1000, 850, 600)  # Creamy Peach
    curses.init_color(36, 1000, 400, 400)  # Bright Coral
    curses.init_color(37, 1000, 950, 200)  # Laser Yellow
    curses.init_color(38, 1000, 600, 800)  # Bright Orchid
    curses.init_color(39, 1000, 300, 0)  # Burning Orange

    curses.init_color(40, 1000, 1000, 1000)  # Full White
    curses.init_color(41, 800, 850, 900)  # Bright Silver
    curses.init_color(42, 400, 600, 1000)  # Tech Blue
    curses.init_color(43, 1000, 400, 0)  # Safety Orange
    curses.init_color(44, 1000, 100, 300)  # Neon Red

    curses.use_default_colors()

    for i in range(25):
        curses.init_pair(i + 1, 20 + i, -1)


sections: List[str] = [
    "Generate",
    "Play",
    "Show/Hide",
    "Change colours",
    "Exit",
]
