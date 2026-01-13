import sys
import random


UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
TILES = {
    # Using a thin vertical line for the wall
    "WALL": "\033[30m┃\033[0m",
    # Using 3 spaces for the path makes the path look like a large square
    "PATH": "   ",
    # The Start/End markers (colored blocks from your image)
    "START": "\033[42m   \033[0m",  # Green block (3 spaces wide)
    "END": "\033[44m   \033[0m",  # Blue block (3 spaces wide)
}
moves = []

for _ in range(20):
    moves.append(random.randint(0, 3))

WIDTH = int(sys.argv[1])
HEIGHT = int(sys.argv[2])

EXIT = 5, 2
ENTRY = 8, 7
print()

sep = True
new_row = True


def is_corner(column, row):

    if column == 0 and row == 0:
        return True
    if column == 0 and row == WIDTH - 1:
        return True
    if column == HEIGHT - 1 and row == WIDTH - 1:
        return True
    if column == HEIGHT - 1 and row == 0:
        return True

    return False


for column in range(HEIGHT):

    for row in range(WIDTH):
        if is_corner(column, row):
            print(".", end="")

        elif row == 0 or row == WIDTH - 1:
            print("┃", end="")
        elif column == 0 or column == HEIGHT - 1:
            print("━", end="")

        else:
            print(" ", end="")
    print()


print()
