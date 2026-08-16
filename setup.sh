#!/bin/bash
# Setup script for wavetable-generator project
# Run this after cloning: bash setup.sh

set -e  # Exit on any error

echo "🎵 Wavetable Generator Setup"
echo "================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
    VENV_ACTIVATE=".venv/Scripts/activate"
else
    VENV_ACTIVATE=".venv/bin/activate"
fi

# Check if venv already exists
if [ -d ".venv" ]; then
    echo "⚠️  Virtual environment already exists (.venv)"
    read -p "Delete and recreate? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing old virtual environment..."
        rm -rf .venv
    else
        echo "❌ Setup cancelled. Using existing .venv"
        exit 0
    fi
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv .venv

# Activate it
echo "✨ Activating virtual environment..."
source "$VENV_ACTIVATE"

# Upgrade pip
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip

# Install package in development mode
echo "📥 Installing wavetable-synthesis package..."
pip install -e .

# Install development dependencies (optional)
read -p "Install development dependencies (pytest, ruff, mypy, etc.)? (Y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo "📥 Installing development dependencies..."
    pip install -e ".[dev]"
fi

# Node tools: husky (git hooks), prettier, markdownlint, office-space
if command -v npm >/dev/null 2>&1; then
    echo "📥 Installing Node tools (husky, prettier)..."
    npm install
    # husky sets core.hooksPath to .husky/_. Drop a leftover Python hook.
    rm -f .git/hooks/pre-commit
    echo "✅ Husky git hooks installed"
else
    echo "⚠️  npm not found. Skip git hooks."
    echo "   Install Node 22+ and run: npm install"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
if [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
    echo "  source .venv/Scripts/activate"
else
    echo "  source .venv/bin/activate"
fi
echo ""
echo "Quick start commands:"
echo "  python -m wavetable_synthesis --list            # List generators"
echo "  python -m wavetable_synthesis sine_to_triangle  # Generate wavetable"
echo "  pytest generator/wavetable_tests/              # Run tests"
echo ""
echo "Modern development commands (recommended):"
echo "  make help      # Show all available commands (using Make)"
echo ""
echo "Linting and formatting:"
echo "  ruff check .         # Check code style (modern, fast)"
echo "  ruff format .        # Format code"
echo "  make format          # Format with Ruff"
echo ""
