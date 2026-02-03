import random


def remove_random_walls(grid, width, height, factor=0.1):
    """
    Takes a finished maze and breaks extra walls to create loops.
    """

    pos_x = (width - 7) // 2
    pos_y = (height - 5) // 2
    end_x, end_y = pos_x + 7, pos_y + 5

    def is_protected(x, y):
        return pos_x <= x < end_x and pos_y <= y < end_y

    extra_openings = int((width * height) * factor)

    for _ in range(extra_openings):
        x = random.randint(0, width - 2)
        y = random.randint(0, height - 2)

        current_cell = grid[y][x]

        if random.choice(["right", "down"]) == "right":
            neighbor = grid[y][x + 1]
            if not is_protected(x, y) and not is_protected(x + 1, y):
                current_cell.right = False
                neighbor.left = False
        else:
            neighbor = grid[y + 1][x]
            if not is_protected(x, y) and not is_protected(x, y + 1):
                current_cell.down = False
                neighbor.up = False
