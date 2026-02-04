import curses
from curses import wrapper
from model import MazeGenerator, Maze



config = {}
try:
    with open("config.txt", "r") as fd:
        for line in fd:
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                config[key.strip().upper()] = value.strip()
        WIDTH = int(config.get("WIDTH", 10))
        HEIGHT = int(config.get("HEIGHT", 10))
        is_perfect_str = config.get("PERFECT", "TRUE").strip().upper()
        is_perfect = (is_perfect_str == "TRUE")
except (FileNotFoundError, PermissionError, KeyError, ValueError) as e:
    print(f"[Error loading], using default config {e}")
    WIDTH = 10
    HEIGHT = 10
    is_perfect = True


def get_safe_coords(key, default_x, default_y, max_w, max_h):
    raw_val = config.get(key)
    if not raw_val:
        return (default_x, default_y)

    try:
        # Split "0,0" into [0, 0]
        parts = raw_val.split(',')
        if len(parts) != 2:
            raise ValueError

        x, y = int(parts[0].strip()), int(parts[1].strip())

        # Check if within maze bounds
        if 0 <= x < max_w and 0 <= y < max_h:
            return (x, y)
        else:
            print(f"[Warning]: {key} {x},{y} is out of bounds. Using default.")
            return (default_x, default_y)

    except (ValueError, IndexError):
        print(f"[Warning]: {key} has invalid format in config. Using default.")
        return (default_x, default_y)


entry = get_safe_coords("ENTRY", 0, 0, WIDTH, HEIGHT)
exit = get_safe_coords("EXIT", WIDTH - 1, HEIGHT - 1, WIDTH, HEIGHT)

