#!/bin/bash
# Setup script for wavetable-generator project
# Run this after cloning: bash setup.sh

set -e  # Exit on any error

echo "🎵 Wavetable Generator Setup"
echo "================================"
echo ""

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
source .venv/Scripts/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip

# Install package in development mode
echo "📥 Installing wavetable-synthesis package..."
pip install -e .

# Install development dependencies (optional)
read -p "Install development dependencies (pytest, pylint, mypy, etc.)? (Y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo "📥 Installing development dependencies..."
    pip install pytest pytest-cov pylint mypy flake8 black
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source .venv/Scripts/activate"
echo ""
echo "Quick start commands:"
echo "  python -m wavetable_synthesis --list            # List generators"
echo "  python -m wavetable_synthesis sine_to_triangle  # Generate wavetable"
echo "  python -m pytest wavetable_tests/               # Run tests"
echo ""
