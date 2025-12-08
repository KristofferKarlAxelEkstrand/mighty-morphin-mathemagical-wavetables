#!/bin/bash
# Post-create script for development container
# This runs after the container is created

set -e

echo "Setting up Mighty Morphin Mathemagical Wavetables development environment..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install package with dev dependencies
echo "Installing package with dev dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks (only if .git exists)
if [ -d ".git" ]; then
    echo "Installing pre-commit hooks..."
    pre-commit install || echo "Warning: pre-commit install failed, continuing..."
else
    echo "Skipping pre-commit hooks (no .git directory)"
fi

echo "Development environment setup complete!"
echo ""
echo "Quick start commands:"
echo "  make help           # Show all available commands"
echo "  make test           # Run tests"
echo "  make lint           # Check code style with Ruff"
echo "  make format         # Format code with Ruff"
echo ""
