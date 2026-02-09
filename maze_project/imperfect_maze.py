import random


def remove_random_walls(grid, width, height, factor=0.1):
    pos_x = (width - 7) // 2
    pos_y = (height - 5) // 2
    end_x, end_y = pos_x + 7, pos_y + 5

    def is_protected(x, y):
        return pos_x <= x < end_x and pos_y <= y < end_y

    target_openings = int((width * height) * factor)
    opened_count = 0
    max_attempts = 1000
    attempts = 0

    while opened_count < target_openings and attempts < max_attempts:
        attempts += 1
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        direction = random.choice(["right", "down"])

        if direction == "right" and x < width - 1:
            if not is_protected(x, y) and not is_protected(x + 1, y):
                if grid[y][x].right:
                    grid[y][x].right = False
                    grid[y][x+1].left = False
                    opened_count += 1

        elif direction == "down" and y < height - 1:
            if not is_protected(x, y) and not is_protected(x, y + 1):
                if grid[y][x].down:
                    grid[y][x].down = False
                    grid[y+1][x].up = False
                    opened_count += 1
