from typing import List, Tuple
from mazegen.model import Cell


def save_maze(grid: List[List[Cell]], width: int, height: int, 
              entry: Tuple[int, int], exit_pt: Tuple[int, int], 
              path_coords: List[Tuple[int, int]], filename: str = "maze.txt") -> None:
    """
    Saves maze structure (Hex), Entry/Exit, and Path Solution to a file.
    Weights: North=1, East=2, South=4, West=8.
    """
    try:
        with open(filename, "w") as f:
            # 1. Write the Maze Structure Rows
            for y in range(height):
                row_hex = ""
                for x in range(width):
                    cell = grid[y][x]
                    val = 0
                    # Match the attributes in your model.py: up, right, down, left
                    if cell.up:
                        val += 1
                    if cell.right:
                        val += 2
                    if cell.down:
                        val += 4
                    if cell.left:
                        val += 8
                    row_hex += f"{val:X}"
                f.write(f"{row_hex}\n")

            f.write("\n")  # Blank line separator

            # 2. Write Entry and Exit
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_pt[0]},{exit_pt[1]}\n\n")

            # 3. Write Path Solution as a single long Hex mask
            path_hex = _encode_path_mask(width, height, path_coords)
            f.write(f"{path_hex}\n")

    except Exception as e:
        # Using print here as a fallback if pdeb isn't imported
        print(f"[File Error]: {e}")


def _encode_path_mask(width: int, height: int, path_coords: List[Tuple[int, int]]) -> str:
    bit_string = ""
    path_set = set(path_coords)
    for y in range(height):
        for x in range(width):
            bit_string += "1" if (x, y) in path_set else "0"
    return f"{int(bit_string, 2):X}" if bit_string else "0"
