PYTHON = python3
PIP = pip3

.PHONY: install run debug clean lint lint-strict build validate

install:
	$(PIP) install flake8 mypy
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e .

run:
	PYTHONPATH=. $(PYTHON) app/a_maze_ing.py

debug:
	PYTHONPATH=. $(PYTHON) -m pdb app/a_maze_ing.py

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf *.egg-info
	rm -rf build/ dist/
	rm -f maze.txt

build:
	$(PIP) install --upgrade build
	$(PYTHON) -m build
	@echo "Build complete. Check the 'dist/' folder for your .whl and .tar.gz files."

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

validate:
	PYTHONPATH=. $(PYTHON) output_validator.py maze.txt