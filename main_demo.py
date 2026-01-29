#!/usr/bin/env python3
"""
main_demo.py
Simple CLI interface for maze generation, solving, and visualization.
Usage: python3 main_demo.py [options]
"""

import argparse
import sys
from pathlib import Path
from generator import MazeGenerator
from solver import find_solution_path
from visualizer import TerminalVisualizer


class Config:
    """Simple config object for MazeGenerator."""
    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.entry = (0, 0)
        self.exit = (width - 1, height - 1)
        self.perfect = True
        self.algorithm = "prim"
        self.seed = seed


def load_config_file(path: str = "config.txt") -> dict:
    """Load simple key=value config from `config.txt`.

    Returns a dict with keys uppercased.
    """
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


def generate_and_display(width, height, colors=False, show_solution=True,
                         animate=False, step_by_step=False, seed=None):
    """Generate maze, solve it, and display."""
    print(f"\n📍 Generating {width}x{height} maze...")

    config = Config(width, height, seed=seed)
    gen = MazeGenerator(config, verbose=False)
    maze = gen.generate()

    print("🔍 Solving maze...")
    maze.solution_path = find_solution_path(maze)

    print(f"✓ Solution found: {len(maze.solution_path)} steps\n")

    # Display based on mode
    viz = TerminalVisualizer(maze, use_colors=colors,
                             show_solution=show_solution)

    if animate:
        print("▶ Playing animated solution...\n")
        viz.display_solution_animated(delay=0.2)
    elif step_by_step:
        print("▶ Tracing solution step by step...\n")
        viz.display_solution_step_by_step(delay=0.3)
    else:
        viz.display()


def interactive_mode():
    """Interactive mode to choose maze size."""
    print("\n" + "=" * 60)
    print("MAZE GENERATOR & SOLVER - INTERACTIVE MODE")
    print("=" * 60)

    print("\nChoose maze size:")
    print("  1. Tiny (5x5)")
    print("  2. Small (8x8)")
    print("  3. Medium (15x15)")
    print("  4. Large (20x20)")
    print("  5. Huge (30x30)")

    try:
        choice = input("\nEnter choice (1-5): ").strip()

        sizes = {
            '1': 5,
            '2': 8,
            '3': 15,
            '4': 20,
            '5': 30
        }

        if choice not in sizes:
            print("❌ Invalid choice!")
            return

        size = sizes[choice]

        print("\nDisplay options:")
        print("  1. Simple (no colors)")
        print("  2. With colors")
        print("  3. Animated solution")
        print("  4. Step-by-step trace")

        mode_choice = input("\nEnter mode (1-4): ").strip()

        if mode_choice == '1':
            generate_and_display(size, size, colors=False)
        elif mode_choice == '2':
            generate_and_display(size, size, colors=True)
        elif mode_choice == '3':
            generate_and_display(size, size, colors=True, animate=True)
        elif mode_choice == '4':
            generate_and_display(size, size, colors=True, step_by_step=True)
        else:
            print("❌ Invalid mode!")

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Maze Generator, Solver & Visualizer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main_demo.py --size 10              # Standard 10x10 maze
  python3 main_demo.py --size 20 --colors     # 20x20 with colors
  python3 main_demo.py --size 12 --animate    # Animated solution
  python3 main_demo.py --interactive          # Interactive mode
  make run                                     # Using Makefile
  make huge                                    # Generate 50x50 maze
        """
    )

    parser.add_argument('--size', type=int, default=None,
                        help='Maze size (overrides config.txt when provided)')
    parser.add_argument('--colors', action='store_true',
                        help='Use colored output')
    parser.add_argument('--seed', type=int, default=None,
                        help='Random seed for reproducibility')
    parser.add_argument('--animate', action='store_true',
                        help='Animate solution path')
    parser.add_argument('--step-by-step', action='store_true',
                        help='Show solution step-by-step')
    parser.add_argument('--interactive', action='store_true',
                        help='Interactive mode')
    parser.add_argument('--no-solution', action='store_true',
                        help='Hide solution path markers')

    args = parser.parse_args()

    try:
        if args.interactive:
            interactive_mode()
        else:
            # Load config.txt if present and use values as defaults
            cfg = load_config_file()

# Determine size: CLI --size takes precedence, otherwise use config WIDTH/HEI
            if args.size is not None:
                size = args.size
            else:
                try:
                    size_w = int(cfg.get('WIDTH', 10))
                    size_h = int(cfg.get('HEIGHT', 10))
    # If WIDTH and HEIGHT are equal, use that as size; otherwise prefer WIDTH
                    size = size_w if size_w == size_h else max(size_w, size_h)
                except Exception:
                    size = 10

            # Validate size
            if size < 3 or size > 200:
                print(f"❌ Size must be between 3 and 200 (got {size})")
                sys.exit(1)

            # Entry/exit from config if present
            entry = None
            exitp = None
            if 'ENTRY' in cfg:
                try:
                    ex, ey = cfg['ENTRY'].split(',')
                    entry = (int(ex.strip()), int(ey.strip()))
                except Exception:
                    entry = None
            if 'EXIT' in cfg:
                try:
                    sx, sy = cfg['EXIT'].split(',')
                    exitp = (int(sx.strip()), int(sy.strip()))
                except Exception:
                    exitp = None

            # Build config object using size and optional entry/exit
        # Determine seed: CLI seed takes precedence, otherwise try config SEED
            seed_val = None
            if args.seed is not None:
                seed_val = args.seed
            else:
                if 'SEED' in cfg:
                    try:
                        seed_val = int(cfg['SEED'])
                    except Exception:
                        seed_val = None

            cfg_obj = Config(size, size, seed=seed_val)
            if entry:
                cfg_obj.entry = entry
            if exitp:
                cfg_obj.exit = exitp

            # Generate and display
            generate_and_display(
                cfg_obj.width, cfg_obj.height,
                colors=args.colors,
                show_solution=not args.no_solution,
                animate=args.animate,
                step_by_step=args.step_by_step,
                seed=cfg_obj.seed
            )

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
