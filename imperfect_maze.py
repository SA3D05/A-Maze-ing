import random

def remove_random_walls(grid, width, height, factor=0.1):
    """
    Takes a finished maze and breaks extra walls to create loops.
    """

    extra_openings = int((width * height) * factor)

    for _ in range(extra_openings):
        x = random.randint(0, width - 2)
        y = random.randint(0, height - 2)

        current_cell = grid[y][x]

        if random.choice(["right", "down"]) == "right":
            neighbor = grid[y][x + 1]
            current_cell.right = False
            neighbor.left = False
        else:
            neighbor = grid[y + 1][x]
            current_cell.down = False
            neighbor.up = False
