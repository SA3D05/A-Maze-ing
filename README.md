*This project has been created as part of the 42 curriculum by satifi, sehallil.*

---

# A-Maze-ing

A terminal-based interactive maze generator and solver built in Python. The application generates mazes using **Recursive Backtracking**, solves them with **Dijkstra's algorithm**, and renders them in the terminal using the `curses` library — complete with color themes, an interactive player mode, and a hidden **"42" signature** embedded in every maze.

---

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Instructions](#instructions)
- [Config File Format](#config-file-format)
- [Maze Generation Algorithm](#maze-generation-algorithm)
- [Maze File Format](#maze-file-format)
- [Project Structure](#project-structure)
- [Reusable Components](#reusable-components)
- [Team & Project Management](#team--project-management)
- [Resources](#resources)

---

## Description

**A-Maze-ing** is an interactive terminal application that procedurally generates and displays mazes. The goal of the project is to implement a complete maze generation pipeline — from reading a configuration file, generating a perfect (or imperfect) maze, computing its solution path, and rendering everything live in the terminal with `curses`.

The project includes:

- A **menu-driven TUI** (Text User Interface) with keyboard navigation
- **Maze generation** using Recursive Backtracking (Depth-First Search)
- **Pathfinding** using Dijkstra's algorithm
- **Serialization** of the maze and solution to a `.txt` file using a compact hexadecimal format
- An **interactive player mode** where you can walk through the maze yourself
- A **"42" easter egg** — a protected region carved into the center of every maze as a tribute to the 42 school network

---

## Features

| Feature | Description |
|---|---|
| Maze Generation | Recursive Backtracking (perfect maze) |
| Imperfect Mode | Randomly removes ~10% of walls to create loops |
| Pathfinding | Dijkstra's algorithm highlights the shortest solution |
| Color Themes | 25 randomizable color palettes for the display |
| Player Mode | Navigate the maze yourself using arrow keys |
| Show/Hide Solution | Toggle the solution path on/off |
| Save to File | Exports maze + solution in hex format to a `.txt` file |
| "42" Easter Egg | A pixel-art "42" is protected and embedded in every maze |
| Step-by-Step Mode | Watch the maze build itself wall by wall |
| Seed Support | Reproducible mazes via optional seed in config |

---

## Instructions

### Requirements

- Python 3.10+
- A terminal that supports `curses` (Linux / macOS recommended)
- `pip3` for dependency management

### Installation

```bash
make install
```

This installs `flake8`, `mypy`, and other required dependencies.

### Running the Application

```bash
make run
```

This is equivalent to:

```bash
PYTHONPATH=. python3 a_maze_ing.py config.txt
```

You can also point to any custom config file:

```bash
PYTHONPATH=. python3 a_maze_ing.py my_config.txt
```

> ⚠️ **Important:** Do not resize the terminal window while the application is running — this will terminate the program.

### Keyboard Controls

**Main Menu:**

| Key | Action |
|---|---|
| `↑` / `↓` | Navigate menu |
| `Enter` | Select option |

**Player Mode:**

| Key | Action |
|---|---|
| `↑ ↓ ← →` | Move player |
| `Q` | Quit player mode |

### Other Makefile Commands

```bash
make clean   # Remove __pycache__, build artifacts, and maze.txt
make lint    # Run flake8 and mypy for static analysis
make build   # Package the project for distribution
make help    # Show all available commands
make debug    # run in debug mode 

```

---

## Config File Format

The application reads its parameters from a plain text configuration file (e.g., `config.txt`). Each line follows the format `KEY=VALUE`. Lines beginning with `#` are treated as comments and ignored.

### Example

```
WIDTH=9
HEIGHT=7
ENTRY=0,0
EXIT=6,8
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Parameter Reference

| Key | Type | Required | Description |
|---|---|---|---|
| `WIDTH` | Integer | ✅ | Number of columns in the maze. **Minimum: 9** |
| `HEIGHT` | Integer | ✅ | Number of rows in the maze. **Minimum: 7** |
| `ENTRY` | `x,y` | ✅ | Entry point coordinates (0-indexed). Must be inside the grid and not equal to `EXIT` |
| `EXIT` | `x,y` | ✅ | Exit point coordinates (0-indexed). Must be inside the grid and not equal to `ENTRY` |
| `OUTPUT_FILE` | String | ✅ | Path to save the generated maze. Defaults to `maze.txt` |
| `PERFECT` | Boolean | ✅ | `True` = perfect maze (no loops). `False` = imperfect maze (random wall removals). Defaults to `True` |
| `SEED` | String | ❌ | Optional seed for reproducible maze generation. Omit for a random maze each run |

### Validation Rules

- `WIDTH` must be **≥ 9** and `HEIGHT` must be **≥ 7** — the minimum size needed to embed the "42" signature
- `ENTRY` and `EXIT` must both be valid coordinates within the grid bounds
- `ENTRY` and `EXIT` must **not** be the same point
- Neither `ENTRY` nor `EXIT` can be placed inside the protected "42" zone (the central region of the maze)
- If any validation fails, the application prints an error and exits

---

## Maze Generation Algorithm

### Chosen Algorithm: Recursive Backtracking (DFS)

The maze is generated using **Recursive Backtracking**, also known as the Depth-First Search (DFS) maze generation algorithm. It works iteratively using an explicit stack:

1. Start from the top-left cell `(0, 0)`; mark it as visited
2. Push the current cell onto the stack
3. While the stack is not empty:
   - Look at the current cell's unvisited neighbors
   - If there are unvisited neighbors: pick one at random, remove the wall between them, mark the neighbor as visited, and push it onto the stack
   - If there are no unvisited neighbors: backtrack by popping the stack
4. Repeat until the stack is empty — every cell has been visited

A special pre-processing step marks a central region of cells (forming the digit "42" in pixel art) as already visited **before** the DFS begins. This forces the algorithm to route around them, carving the "42" shape into the maze structure itself.

### Why Recursive Backtracking?

We chose Recursive Backtracking for several reasons:

- **Simplicity**: The algorithm is straightforward to implement and reason about
- **Perfect mazes by default**: It always produces a spanning tree — exactly one path exists between any two cells. This is ideal for a puzzle-style maze game
- **River-like aesthetic**: DFS tends to carve long, winding corridors, which look visually interesting and give a strong sense of depth
- **Easy to extend**: The imperfect mode (optional loop creation) was simple to add as a post-processing step on top of the base algorithm — we randomly remove ~10% of internal walls after generation
- **Seed support**: Since Python's `random` module is used throughout, plugging in a seed value makes mazes fully reproducible

### Pathfinding: Dijkstra's Algorithm

Once the maze is generated, the shortest solution path from `ENTRY` to `EXIT` is computed using **Dijkstra's algorithm** (via a min-heap priority queue). Since all wall traversals have equal cost (weight = 1), this is effectively a BFS, but implemented with Dijkstra's for correctness and extensibility. The path coordinates are stored and encoded into the output file.

---

## Maze File Format

Generated mazes are saved to `maze.txt` (or your configured `OUTPUT_FILE`) in the following format:

```
D55555553
BF917FFFA
AFEC157FA
AFFFAFFFA
A93FAFD52
86AFAFFFA
C7C545556

0,5
0,2

100804020000
```

### Format Breakdown

**Section 1 — Grid (Hex Wall Encoding):**
Each character is a hexadecimal digit representing the open walls of a cell. Walls are encoded as a bitmask:

| Bit | Direction | Value |
|---|---|---|
| Bit 0 | North (Up) | 1 |
| Bit 1 | East (Right) | 2 |
| Bit 2 | South (Down) | 4 |
| Bit 3 | West (Left) | 8 |

A cell with value `F` (= 15 = `1+2+4+8`) has **all four walls open** (all passages). A cell with value `0` has all walls intact.

**Section 2 — Entry and Exit:**
Two lines containing the `x,y` coordinates of the entry and exit points.

**Section 3 — Solution Path (Hex Bitmask):**
A single hexadecimal number representing the solution path. The grid is flattened row by row into a binary string where `1` marks a cell on the solution path and `0` does not. This binary string is then converted to hex.

---



## Reusable Components

Several parts of this codebase are designed to be modular and reusable outside of this project:

**`MazeGenerator` (`maze_generator.py`)**
The generator is decoupled from the renderer and the application controller. It operates purely on `Maze` and `Cell` data structures. You can use `MazeGenerator.generate()` to generate a grid and `MazeGenerator.__dijkstra()` to solve it in any Python project — no `curses` dependency required for the logic itself.



### - Simple Usage
```
import mazegen

maze_gen = mazegen.MazeGenerator(height=15, width=20)

cells = maze_gen.generate(
    make_perfect=True,
    entry_pos=(0, 0),
    exit_pos=(14, 19)
    )

print(cells) # to print the maze cells

for cell in cells:
    if cell.state == mazegen.CellState.PATH:
        print(f"({cell.y}, {cell.x})", end=", ") # to print the maze solution
```
---

## Team & Project Management

### Team Members & Roles

| Member | Role |
|---|---|
| **[sehallil]** | Maze generation algorithm (Recursive Backtracking), Dijkstra's pathfinding, cell/grid logic |
| **[satifi]** | `curses` rendering pipeline, TUI menu, color system, player mode, file I/O |

> *(Update with actual names and role breakdown)*

### Planning & Evolution

**Initial plan:**
We began by splitting the project into two parallel tracks — the algorithmic core (maze generation + solving) and the visual layer (curses rendering + UI). We anticipated finishing the core logic in the first half and polish in the second.

**How it evolved:**
Integration between the generator and renderer took longer than expected, particularly aligning the coordinate systems between logical cells and visual elements. The "42" easter egg was added mid-project and required protecting a region of cells before the DFS started, which introduced edge cases around `ENTRY`/`EXIT` placement. The imperfect maze mode and step-by-step generation view were added as stretch goals near the end.

### What Worked Well

- The separation of the logical `Cell`/`Maze` layer from the visual `Element`/renderer layer made testing and debugging much easier
- Using a hex bitmask for maze serialization is compact, human-readable, and easy to decode programmatically
- The `Makefile` streamlined the development loop significantly

### What Could Be Improved

- The `gen_grid()` function in `maze_generator.py` became quite long and handles both grid initialization and visual mapping — splitting it into smaller helpers would improve readability
- Error handling could be more descriptive (e.g., config validation currently raises a bare `Exception()`)
- The renderer (`Renderer`) and generator are still somewhat coupled through the `Maze` object — a cleaner event/observer pattern could decouple them further
- No unit tests exist for the core generation or pathfinding logic

### Tools Used

| Tool | Purpose |
|---|---|
| **Python 3 / curses** | Core language and terminal UI framework |
| **flake8** | PEP8 linting and code style enforcement |
| **mypy** | Static type checking |
| **make** | Build automation and developer workflow |
| **Git** | Version control and collaboration |

---

## Resources

### Documentation & References

- [Python `curses` documentation](https://docs.python.org/3/library/curses.html) — Official curses module reference
- [Maze Generation Algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm) — Overview of common maze generation approaches
- [Recursive Backtracker — Jamis Buck's Blog](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker.html) — Classic detailed walkthrough of the DFS maze algorithm
- [Dijkstra's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) — Reference for the pathfinding implementation
- [Python `heapq` documentation](https://docs.python.org/3/library/heapq.html) — Used for the priority queue in Dijkstra's implementation
- [Python `enum` documentation](https://docs.python.org/3/library/enum.html) — Used for `CellState` and `PlayerDirection`

### AI Usage

AI (Claude by Anthropic) was used during this project for the following tasks:

- **Debugging `curses` layout issues** — particularly around coordinate system alignment between logical grid positions and terminal screen positions
- **Reviewing type annotations** — ensuring `mypy` compatibility across the codebase
- **Explaining Dijkstra's algorithm** — validating the priority queue implementation and edge case handling