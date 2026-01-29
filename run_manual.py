#!/usr/bin/env python3

from generator import MazeGenerator
from main_demo import Config, load_config_file
from solver import find_solution_path
from visualizer import TerminalVisualizer


def main():
    # Load config.txt and use values when present
    cfg_data = load_config_file()

    try:
        w = int(cfg_data.get('WIDTH', 5))
        h = int(cfg_data.get('HEIGHT', 5))
    except Exception:
        w, h = 5, 5

    seed = None
    if 'SEED' in cfg_data:
        try:
            seed = int(cfg_data['SEED'])
        except Exception:
            seed = None

    cfg = Config(w, h, seed=seed)
    # Optional entry/exit override
    if 'ENTRY' in cfg_data:
        try:
            ex, ey = cfg_data['ENTRY'].split(',')
            cfg.entry = (int(ex.strip()), int(ey.strip()))
        except Exception:
            pass
    if 'EXIT' in cfg_data:
        try:
            sx, sy = cfg_data['EXIT'].split(',')
            cfg.exit = (int(sx.strip()), int(sy.strip()))
        except Exception:
            pass

    mg = MazeGenerator(cfg, verbose=False)
    maze = mg.generate()
    maze.solution_path = find_solution_path(maze)
    print('Solution path:', maze.solution_path)
    viz = TerminalVisualizer(maze, use_colors=False, show_solution=True,
                             solution_style='arrow')
    viz.display_solution_animated(delay=0.20)


if __name__ == '__main__':
    main()
