# Project Modernization Guide

This document explains the modern tooling and improvements made to the Mighty Morphin Mathemagical Wavetables project, and how to use them.

## What's New?

We've modernized the development workflow with faster, more efficient tools while maintaining backward compatibility with existing workflows.

### Modern Tools Added

1.  **Ruff** - Ultra-fast Python linter and formatter (replaces Black, isort, Flake8, many Pylint rules)
2.  **Pre-commit hooks** - Automated code quality checks before commits
3.  **Make/Just** - Convenient task runners for common commands
4.  **Dev containers** - Ready-to-use development environment for VS Code/GitHub Codespaces
5.  **uv** - Optional ultra-fast package installer (10-100x faster than pip)

## Quick Comparison

### Linting and Formatting

**Before (Legacy - still works):**

```bash
black wavetable_synthesis/
isort wavetable_synthesis/
flake8 wavetable_synthesis/
pylint wavetable_synthesis/
```

**After (Modern - recommended):**

```bash
ruff check --fix wavetable_synthesis/
ruff format wavetable_synthesis/
# Or simply:
make format
```

**Why Ruff?**

-  ⚡ **10-100x faster** - Written in Rust
-  🔧 **Auto-fixes** - Fixes most issues automatically
-  🎯 **All-in-one** - Replaces 4+ tools
-  📦 **Zero config** - Works out of the box

### Task Running

**Before:**

```bash
# Manual commands
pytest wavetable_tests/
black wavetable_synthesis/
mypy wavetable_synthesis/
python -m wavetable_synthesis --list
```

**After:**

```bash
# Using Make
make test
make format
make type-check
make list

# Or using Just (modern alternative)
just test
just format
just type-check
just list
```

### Package Installation

**Before:**

```bash
pip install -e ".[dev]"  # Takes 30-60 seconds
```

**After (optional - using uv):**

```bash
uv pip install -e ".[dev]"  # Takes 2-5 seconds
```

## Migration Path

You can adopt these tools gradually:

### Phase 1: Try the Tools (No Commitment)

```bash
# Install ruff and try it
pip install ruff
ruff check wavetable_synthesis/

# Use Make for convenience
make lint
make format
```

### Phase 2: Use Pre-commit Hooks

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Now your code is checked automatically before each commit
git commit -m "my changes"  # Hooks run automatically
```

### Phase 3: Adopt Fully (Optional)

-  Update your personal workflow to use Ruff instead of Black/isort/Flake8
-  Use Make or Just for common tasks
-  Consider switching to uv for faster dependency installation

## Detailed Tool Guides

### 1. Ruff - Modern Linting

**Installation:**

```bash
pip install ruff
# Already included in dev dependencies
```

**Basic Usage:**

```bash
# Check code
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .

# Check what would be formatted
ruff format --check .
```

**Configuration:** See `[tool.ruff]` in `pyproject.toml`

**Documentation:** <https://docs.astral.sh/ruff/>

### 2. Pre-commit Hooks

**Installation:**

```bash
pip install pre-commit
pre-commit install
```

**Usage:**

```bash
# Hooks run automatically on git commit

# Run manually on all files
pre-commit run --all-files

# Update hooks to latest versions
pre-commit autoupdate
```

**What's Checked:**

-  Ruff linting and formatting
-  Type checking with mypy
-  Trailing whitespace
-  File endings
-  YAML/JSON/TOML syntax
-  Markdown linting
-  Security checks

**Configuration:** See `.pre-commit-config.yaml`

### 3. Make - Task Runner

**Usage:**

```bash
# Show all commands
make help

# Common tasks
make install-dev    # Install dev dependencies
make test           # Run tests
make lint           # Check code quality
make format         # Format code
make quality        # Run all quality checks
make list           # List generators
```

**Benefits:**

-  Consistent commands across projects
-  No need to remember complex command arguments
-  Works on Linux, macOS, Windows (with Git Bash)

**Configuration:** See `Makefile`

### 4. Just - Modern Task Runner

**Installation:**

```bash
# macOS
brew install just

# Cargo (all platforms)
cargo install just

# Other: https://github.com/casey/just#installation
```

**Usage:**

```bash
# Show all recipes
just --list

# Run tasks (same as Make)
just test
just format
just run sine_to_triangle
```

**Benefits:**

-  Simpler, cleaner syntax than Make
-  Better error messages
-  Cross-platform without special setup
-  Supports command arguments: `just run sine_to_triangle`

**Configuration:** See `justfile`

### 5. uv - Fast Package Installer

**Installation:**

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Usage:**

```bash
# Replace pip with uv pip
uv pip install -e ".[dev]"

# Much faster than pip!
```

**Benefits:**

-  10-100x faster than pip
-  Drop-in replacement
-  No changes to pyproject.toml needed

**Documentation:** See `docs/uv-guide.md`

### 6. Dev Containers

**What is it?**

A pre-configured development environment that runs in a container.

**Usage:**

1.  Open project in VS Code
2.  Click "Reopen in Container" when prompted
3.  Everything is set up automatically!

**Benefits:**

-  Consistent environment across machines
-  No manual setup needed
-  Works in GitHub Codespaces
-  Includes all tools and extensions

**Configuration:** See `.devcontainer/devcontainer.json`

## Frequently Asked Questions

### Do I have to use these new tools?

No! All legacy tools (Black, isort, Flake8, Pylint) still work. The new tools are optional but recommended for better performance.

### Will my existing workflow break?

No! We've maintained full backward compatibility. You can continue using your existing commands.

### Can I use both old and new tools?

Yes! You can mix and match. For example, use Ruff for formatting but still use Pylint for linting.

### Which tools should I adopt first?

Recommended order:

1.  **Make/Just** - Easiest to adopt, immediate productivity boost
2.  **Ruff** - Significantly faster linting/formatting
3.  **Pre-commit hooks** - Catches issues before they reach CI
4.  **uv** - Faster installs (optional)

### How do I test the new tools?

```bash
# Try Ruff
make lint
make format

# Try Make
make test
make quality

# Try pre-commit (without installing hooks)
pre-commit run --all-files
```

### Will CI still pass if I use Ruff locally?

Yes! CI currently uses the legacy tools (Black, isort, etc.). Your Ruff-formatted code will pass all checks.

### When will the project switch to Ruff in CI?

We'll transition gradually after gathering feedback. Legacy tools will be supported during the transition.

## Performance Comparison

### Linting Speed

```bash
# Legacy (4 separate tools)
time (black --check . && isort --check . && flake8 . && pylint .)
# ~15-30 seconds

# Modern (single tool)
time ruff check .
# ~0.5-2 seconds
```

### Package Installation Speed

```bash
# pip
time pip install -e ".[dev]"
# ~30-60 seconds

# uv
time uv pip install -e ".[dev]"
# ~2-5 seconds
```

## Additional Resources

-  **DEVELOPMENT.md** - Detailed development guide with modern tools
-  **docs/uv-guide.md** - Complete uv installation and usage guide
-  **Makefile** - See all available Make commands
-  **justfile** - See all available Just recipes
-  **.pre-commit-config.yaml** - Pre-commit hook configuration
-  **pyproject.toml** - Ruff configuration under `[tool.ruff]`

## Feedback and Questions

Have questions or feedback about the new tools?

-  Open an issue on GitHub
-  Ask in GitHub Discussions
-  Check the documentation links above

## Summary

The project now supports modern Python development tools while maintaining full backward compatibility. Adopt them at your own pace!

**Key Benefits:**

-  ⚡ 10-100x faster linting and formatting
-  🔧 Automated code quality checks
-  📦 Faster package installation
-  🎯 Simpler, more consistent workflows
-  ♻️ Zero breaking changes - legacy tools still work

Happy coding! 🎵
