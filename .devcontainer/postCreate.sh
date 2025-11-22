#!/bin/bash
# Post-create script for development container
# This runs after the container is created

set -e

echo "🎵 Setting up Mighty Morphin Mathemagical Wavetables development environment..."

# Upgrade pip
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip

# Install package with dev dependencies
echo "📥 Installing package with dev dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
pre-commit install

echo "✅ Development environment setup complete!"
echo ""
echo "Quick start commands:"
echo "  make help           # Show all available commands"
echo "  just --list         # Show Just recipes (if Just is installed)"
echo "  make test           # Run tests"
echo "  make lint           # Check code style with Ruff"
echo "  make format         # Format code with Ruff"
echo ""
