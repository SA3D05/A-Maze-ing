from enum import Enum


class CellState(Enum):
    REGULAR = 0
    PATH = 1
    FT = 2
    ENTRY = 3
    EXIT = 4
