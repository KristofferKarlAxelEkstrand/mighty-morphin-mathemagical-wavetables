.PHONY: help install install-dev clean test test-cov lint format type-check quality pre-commit run list validate batch build docs

# Default target - show help
help:
	@echo "🎵 Mighty Morphin Mathemagical Wavetables - Development Commands"
	@echo "=================================================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  make install          Install package in development mode"
	@echo "  make install-dev      Install with all dev dependencies"
	@echo "  make pre-commit       Install pre-commit hooks"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test            Run all tests"
	@echo "  make test-cov        Run tests with coverage report"
	@echo "  make test-verbose    Run tests with verbose output"
	@echo ""
	@echo "Code Quality Commands:"
	@echo "  make lint            Run Ruff linter (modern, fast)"
	@echo "  make format          Format code with Ruff"
	@echo "  make type-check      Run mypy type checker"
	@echo "  make quality         Run all quality checks"
	@echo ""
	@echo "Legacy Linting (for comparison):"
	@echo "  make lint-legacy     Run Black, isort, Flake8, Pylint"
	@echo ""
	@echo "Generator Commands:"
	@echo "  make list            List all available generators"
	@echo "  make validate        Validate all generators"
	@echo "  make run GEN=name    Run specific generator (e.g., make run GEN=sine_to_triangle)"
	@echo "  make batch           Generate all wavetables"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean           Remove build artifacts and cache files"
	@echo "  make update-deps     Update dependencies to latest versions"
	@echo ""

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	@echo "✅ Development dependencies installed"

pre-commit:
	pre-commit install
	@echo "✅ Pre-commit hooks installed"

# Testing
test:
	pytest wavetable_tests/

test-cov:
	pytest wavetable_tests/ --cov=wavetable_synthesis --cov-report=term-missing --cov-report=html

test-verbose:
	pytest wavetable_tests/ -v

# Code Quality - Modern (Ruff)
lint:
	ruff check wavetable_synthesis/ wavetable_generators/ wavetable_tests/

format:
	ruff format wavetable_synthesis/ wavetable_generators/ wavetable_tests/
	ruff check --fix wavetable_synthesis/ wavetable_generators/ wavetable_tests/

type-check:
	mypy wavetable_synthesis/ --strict

quality: lint type-check
	@echo "✅ All quality checks passed!"

# Legacy linting (for comparison and gradual migration)
lint-legacy:
	black --check wavetable_synthesis/ wavetable_generators/ wavetable_tests/
	isort --check-only --profile black wavetable_synthesis/ wavetable_generators/ wavetable_tests/
	flake8 wavetable_synthesis/ wavetable_generators/ wavetable_tests/
	pylint wavetable_synthesis/ wavetable_generators/

format-legacy:
	black wavetable_synthesis/ wavetable_generators/ wavetable_tests/
	isort --profile black wavetable_synthesis/ wavetable_generators/ wavetable_tests/

# Generator Commands
list:
	python -m wavetable_synthesis --list

validate:
	python -m wavetable_synthesis --validate

run:
	@if [ -z "$(GEN)" ]; then \
		echo "❌ Error: Please specify a generator name with GEN=name"; \
		echo "Example: make run GEN=sine_to_triangle"; \
		exit 1; \
	fi
	python -m wavetable_synthesis $(GEN)

batch:
	python -m wavetable_synthesis --batch

# Utilities
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned build artifacts and cache files"

update-deps:
	pip install --upgrade pip
	pip install --upgrade -e ".[dev]"
	@echo "✅ Dependencies updated"

# CI/CD simulation
ci: quality test-cov
	@echo "✅ CI checks passed!"
