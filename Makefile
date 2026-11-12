.PHONY: test lint build

test:
	python -m pytest tests

lint:
	python -m compileall pkg cmd internal

build:
	python -m build
