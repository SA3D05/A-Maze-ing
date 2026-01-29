.PHONY: run demo small large huge test clean help

help:
	@echo "Maze Generator & Solver - Available Commands"
	@echo ""
	@echo "  make run          - Run standard 10x10 maze with solution"
	@echo "  make animated     - Run animated solution trace"
	@echo "  make test         - Run syntax & functionality tests"
	@echo "  make clean        - Remove generated maze files"
	@echo "  make help         - Show this help message"
	@echo ""

run:
	# Run the manual snippet which generates, solves, and animates the maze
	python3 run_manual.py

run-config: run
	@echo "(alias) run-config -> run (uses run_manual.py)"

animated:
	python3 main_demo.py --animate --colors


test:
	python3 -m compileall . -q && echo "✓ All files compiled"
	python3 -c "from generator import MazeGenerator; from solver import find_solution_path; from visualizer import TerminalVisualizer; print('✓ All modules import OK')"

clean:
	rm -f *.txt maze*.hex test_*.txt my_maze.txt
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	echo "✓ Cleaned up generated files"
