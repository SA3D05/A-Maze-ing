import heapq
import math


def dijkstra(grid, start, end):
    """
    grid: 2D list of Cell objects
    start/end: tuples (x, y)
    """

    if not isinstance(grid[0], list):

        width = int(math.sqrt(len(grid)))
        grid = [grid[i: i + width] for i in range(0, len(grid), width)]

    rows, cols = len(grid), len(grid[0])
    # pq: (distance, (x, y), path_list)
    pq = [(0, start, [start])]
    visited = set()

    while pq:
        (dist, (cx, cy), path) = heapq.heappop(pq)

        if (cx, cy) == end:
            return path

        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))

        current_cell = grid[cy][cx]

        # Check all 4 directions based on wall status
        # Note: We move to (nx, ny) only if the wall between is False
        directions = [
            (cx, cy - 1, not current_cell.up),
            (cx, cy + 1, not current_cell.down),
            (cx - 1, cy, not current_cell.left),
            (cx + 1, cy, not current_cell.right)
        ]

        for nx, ny, is_open in directions:
            if is_open and 0 <= nx < cols and 0 <= ny < rows:
                if (nx, ny) not in visited:
                    heapq.heappush(pq, (dist + 1, (nx, ny), path + [(nx, ny)]))

    return None  # No path found
