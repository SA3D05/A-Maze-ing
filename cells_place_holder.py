"""Compatibility shim: provide `cells_maze_10` and `cells_maze_3` by
generating mazes via `generator.MazeGenerator` and converting to
`model.Cell` objects expected by the rest of the codebase.
"""

from generator import MazeGenerator
from model import Cell as ModelCell
from pathlib import Path


def _make_cells(
        width: int, height: int, seed: int | None = None) -> list[ModelCell]:
    """Generate and convert generator cells into `model.Cell` instances."""
    class Config:
        pass

    cfg = Config()
    cfg.width = width
    cfg.height = height
    cfg.entry = (0, 0)
    cfg.exit = (width - 1, height - 1)
    cfg.perfect = True
    cfg.algorithm = "prim"
    cfg.seed = seed

    gen = MazeGenerator(cfg, verbose=False)
    gen_maze = gen.generate()

    converted = []
    for y in range(height):
        for x in range(width):
            gcell = gen_maze.cells[y][x]
            up_open = not gcell.walls[0]
            right_open = not gcell.walls[1]
            down_open = not gcell.walls[2]
            left_open = not gcell.walls[3]
            converted.append(ModelCell(y, x, up_open, down_open, left_open,
                                       right_open))

    return converted


def _load_config(path: str = "config.txt") -> dict:
    """Load simple KEY=VALUE config into a dict (keys uppercased)."""
    cfg = {}
    p = Path(path)
    if not p.exists():
        return cfg

    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        k, v = line.split('=', 1)
        cfg[k.strip().upper()] = v.strip()

    return cfg


# Generate `cells_maze` dynamically from `config.txt` when available.
# Falls back to 10x10 when the config is missing or invalid.
_cfg = _load_config()
_width = int(_cfg.get('WIDTH', 10))
_height = int(_cfg.get('HEIGHT', 10))
_seed = None
if 'SEED' in _cfg:
    try:
        _seed = int(_cfg['SEED'])
    except Exception:
        _seed = None

cells_maze = _make_cells(_width, _height, seed=_seed)

__all__ = ['cells_maze', '_make_cells']
