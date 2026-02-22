PYTHON = python3
DEBUGGER= pdb
PIP = pip3
ENTRY_POINT = a_maze_ing.py
CONFIG = config.txt

.PHONY: install run clean lint build help

help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies and setup the package"
	@echo "  make run      - Run the maze generator with config.txt"
	@echo "  make clean    - Remove cache and temporary files"
	@echo "  make lint     - Run flake8 and mypy for code quality"
	@echo "  make build    - Package the project for distribution"


install:
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy curses-menu # adding common dependencies
	@echo "Installation complete."

debug:
	@$(PYTHON) -m $(DEBUGGER) $(ENTRY_POINT) $(CONFIG)


run:
	@$(PYTHON) $(ENTRY_POINT) $(CONFIG)


clean:
	rm -rf `find . -name __pycache__`
	rm -rf .mypy_cache
	rm -rf *.egg-info
	rm -rf dist/ build/
	rm -f maze.txt
	@echo "Cleanup complete."


lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

build:
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build
	@echo "Build complete. Check the 'dist/' folder."