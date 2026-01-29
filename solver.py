"""
mazegen/solver.py
Maze solving algorithms and path finding.
(REFACTORED INTERNALLY — BEHAVIOR UNCHANGED)
"""

from typing import List, Tuple, Optional
from collections import deque
import heapq


class MazeSolver:
    """
    Solves mazes using various algorithms.
    """

    # Direction table (single source of truth)
    DIRECTIONS = [
        (0, -1, 'N', 0),  # North
        (1, 0, 'E', 1),   # East
        (0, 1, 'S', 2),   # South
        (-1, 0, 'W', 3),  # West
    ]

    # ───────────────────────── BFS ─────────────────────────

    @staticmethod
    def bfs_solve(
            maze, start: Tuple[int, int], end: Tuple[int, int]
            ) -> Optional[str]:
        width, height = maze.width, maze.height
        cells = maze.cells

        visited = [[False] * width for _ in range(height)]
        parent = [[None] * width for _ in range(height)]

        queue = deque()
        queue.append(start)
        visited[start[1]][start[0]] = True
        parent[start[1]][start[0]] = (-1, -1, '')

        while queue:
            x, y = queue.popleft()

            if (x, y) == end:
                return MazeSolver._reconstruct_path(parent, start, end)

            for dx, dy, direction, wall_idx in MazeSolver.DIRECTIONS:
                nx, ny = x + dx, y + dy

                if not (0 <= nx < width and 0 <= ny < height):
                    continue

                if cells[y][x].walls[wall_idx]:
                    continue

                if visited[ny][nx]:
                    continue

                visited[ny][nx] = True
                parent[ny][nx] = (x, y, direction)
                queue.append((nx, ny))

        return None

    # ─────────────────────── Dijkstra ──────────────────────

    @staticmethod
    def dijkstra_solve(
            maze, start: Tuple[int, int], end: Tuple[int, int]
            ) -> Optional[str]:
        width, height = maze.width, maze.height
        cells = maze.cells

        INF = float('inf')
        dist = [[INF] * width for _ in range(height)]
        parent = [[None] * width for _ in range(height)]

        dist[start[1]][start[0]] = 0
        parent[start[1]][start[0]] = (-1, -1, '')

        pq = [(0, start[0], start[1])]

        while pq:
            current_dist, x, y = heapq.heappop(pq)

            if current_dist > dist[y][x]:
                continue

            if (x, y) == end:
                return MazeSolver._reconstruct_path(parent, start, end)

            for dx, dy, direction, wall_idx in MazeSolver.DIRECTIONS:
                nx, ny = x + dx, y + dy

                if not (0 <= nx < width and 0 <= ny < height):
                    continue

                if cells[y][x].walls[wall_idx]:
                    continue

                new_dist = current_dist + 1

                if new_dist < dist[ny][nx]:
                    dist[ny][nx] = new_dist
                    parent[ny][nx] = (x, y, direction)
                    heapq.heappush(pq, (new_dist, nx, ny))

        return None

    # ─────────────────── PATH RECONSTRUCTION ─────────────────

    @staticmethod
    def _reconstruct_path(parent, start, end) -> str:
        path = []
        x, y = end

        while (x, y) != start:
            px, py, direction = parent[y][x]
            path.append(direction)
            x, y = px, py

        path.reverse()
        return ''.join(path)

    # ───────────────────── PATH VALIDATION ───────────────────

    @staticmethod
    def validate_path(maze, path: str, start: Tuple[int, int]) -> bool:
        x, y = start
        cells = maze.cells

        move_map = {
            'N': (0, -1, 0),
            'E': (1, 0, 1),
            'S': (0, 1, 2),
            'W': (-1, 0, 3),
        }

        for direction in path:
            if direction not in move_map:
                return False

            dx, dy, wall_idx = move_map[direction]

            if cells[y][x].walls[wall_idx]:
                return False

            x += dx
            y += dy

            if not (0 <= x < maze.width and 0 <= y < maze.height):
                return False

        return True

    # ───────────────────── FIND ALL PATHS ────────────────────

    @staticmethod
    def find_all_paths(
        maze, start: Tuple[int, int], end: Tuple[int, int]
            ) -> List[str]:
        width, height = maze.width, maze.height
        cells = maze.cells

        visited = [[False] * width for _ in range(height)]
        all_paths = []

        def dfs(x: int, y: int, path: str):
            visited[y][x] = True

            if (x, y) == end:
                all_paths.append(path)
                visited[y][x] = False
                return

            for dx, dy, direction, wall_idx in MazeSolver.DIRECTIONS:
                nx, ny = x + dx, y + dy

                if not (0 <= nx < width and 0 <= ny < height):
                    continue

                if cells[y][x].walls[wall_idx]:
                    continue

                if visited[ny][nx]:
                    continue

                dfs(nx, ny, path + direction)

            visited[y][x] = False

        dfs(start[0], start[1], "")
        all_paths.sort(key=len)
        return all_paths


# ───────────────────── PUBLIC HELPER ───────────────────────

def find_solution_path(maze) -> Optional[str]:
    if not maze or not maze.cells:
        return None

    solver = MazeSolver()
    path = solver.bfs_solve(maze, maze.entry, maze.exit)

    if path and solver.validate_path(maze, path, maze.entry):
        return path

    return None
