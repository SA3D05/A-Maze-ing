help:
	@echo "Maze Generator & Solver - Available Commands"
	@echo ""
	@echo "  make run          - Run standard 10x10 maze with solution"
	@echo "  make animated     - Run animated solution trace"
	@echo "  make help         - Show this help message"
	@echo ""

run:
	python3 a_maze_ing.py

.PUHONY: help run