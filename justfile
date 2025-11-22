# Justfile - Modern task runner for Mighty Morphin Mathemagical Wavetables
# Install just: https://github.com/casey/just
# Usage: just <recipe>
# List recipes: just --list

# Default recipe (shows help)
default:
    @just --list

# Install package in development mode
install:
    pip install -e .

# Install with all dev dependencies
install-dev:
    pip install -e ".[dev]"
    @echo "✅ Development dependencies installed"

# Install pre-commit hooks
pre-commit:
    pre-commit install
    @echo "✅ Pre-commit hooks installed"

# Run all tests
test:
    pytest wavetable_tests/

# Run tests with coverage report
test-cov:
    pytest wavetable_tests/ --cov=wavetable_synthesis --cov-report=term-missing --cov-report=html

# Run tests with verbose output
test-verbose:
    pytest wavetable_tests/ -v

# Run Ruff linter
lint:
    ruff check wavetable_synthesis/ wavetable_generators/ wavetable_tests/

# Format code with Ruff
format:
    ruff format wavetable_synthesis/ wavetable_generators/ wavetable_tests/
    ruff check --fix wavetable_synthesis/ wavetable_generators/ wavetable_tests/

# Run mypy type checker
type-check:
    mypy wavetable_synthesis/ --strict

# Run all quality checks
quality: lint type-check
    @echo "✅ All quality checks passed!"

# Legacy linting (for comparison)
lint-legacy:
    black --check wavetable_synthesis/ wavetable_generators/ wavetable_tests/
    isort --check-only --profile black wavetable_synthesis/ wavetable_generators/ wavetable_tests/
    flake8 wavetable_synthesis/ wavetable_generators/ wavetable_tests/
    pylint wavetable_synthesis/ wavetable_generators/

# Legacy formatting
format-legacy:
    black wavetable_synthesis/ wavetable_generators/ wavetable_tests/
    isort --profile black wavetable_synthesis/ wavetable_generators/ wavetable_tests/

# List all available generators
list:
    python -m wavetable_synthesis --list

# Validate all generators
validate:
    python -m wavetable_synthesis --validate

# Run a specific generator (e.g., just run sine_to_triangle)
run generator:
    python -m wavetable_synthesis {{generator}}

# Generate all wavetables with batch mode
batch:
    python -m wavetable_synthesis --batch

# Remove build artifacts and cache files
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

# Update dependencies to latest versions
update-deps:
    pip install --upgrade pip
    pip install --upgrade -e ".[dev]"
    @echo "✅ Dependencies updated"

# Simulate CI checks
ci: quality test-cov
    @echo "✅ CI checks passed!"

# Show project info
info:
    @echo "🎵 Mighty Morphin Mathemagical Wavetables"
    @echo "=========================================="
    @echo "Python version: $(python --version)"
    @echo "Package version: 0.1.0"
    @echo ""
    @python -m wavetable_synthesis --list
