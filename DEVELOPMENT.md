# Development Guide

This guide provides detailed instructions for setting up a modern development environment for Mighty Morphin Mathemagical Wavetables.

## Quick Start

### Prerequisites

-  **Python 3.10+** (3.10, 3.11, 3.12, or 3.13)
-  **Git** for version control
-  **Optional:** `pyenv` for Python version management
-  **Optional:** `just` for modern task running (alternative to `make`)

### Automatic Setup

```bash
# Clone the repository
git clone https://github.com/KristofferKarlAxelEkstrand/mighty-morphin-mathemagical-wavetables.git
cd mighty-morphin-mathemagical-wavetables

# Run setup script
bash setup.sh
```

### Manual Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows (Git Bash):
source .venv/Scripts/activate
# On Linux/macOS:
source .venv/bin/activate

# Install package with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Modern Development Tools

### Ruff - Fast Python Linter & Formatter

We use [Ruff](https://docs.astral.sh/ruff/) as our primary linting and formatting tool. It's 10-100x faster than traditional tools and replaces:

-  Black (code formatter)
-  isort (import sorting)
-  Flake8 (style checker)
-  Many pylint rules

**Why Ruff?**

-  ⚡ **Blazing fast** - Written in Rust
-  🔧 **Auto-fix** - Automatically fixes most issues
-  🎯 **All-in-one** - Replaces multiple tools
-  📦 **Zero config** - Works out of the box
-  🔄 **Drop-in replacement** - Compatible with existing tools

**Usage:**

```bash
# Lint code
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .

# Both format and fix
make format
# or
just format
```

### Task Runners

We provide two task runners for convenience:

#### Make (Traditional)

```bash
make help              # Show all available commands
make install-dev       # Install dev dependencies
make test              # Run tests
make lint              # Run linter
make format            # Format code
make quality           # Run all quality checks
```

#### Just (Modern Alternative)

[Just](https://github.com/casey/just) is a modern, cross-platform task runner with better syntax than Make.

Install: `cargo install just` or see [installation guide](https://github.com/casey/just#installation)

```bash
just                   # Show all recipes
just install-dev       # Install dev dependencies
just test              # Run tests
just lint              # Run linter
just format            # Format code
just quality           # Run all quality checks
just run sine_to_triangle  # Run a specific generator
```

### Pre-commit Hooks

We use [pre-commit](https://pre-commit.com/) to automatically check code before commits:

```bash
# Install hooks (one-time setup)
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Update hooks to latest versions
pre-commit autoupdate
```

**What gets checked:**

-  Ruff linting and formatting
-  Type checking with mypy
-  Trailing whitespace
-  File endings
-  YAML/JSON/TOML syntax
-  Markdown linting
-  Security checks with Bandit

### Python Version Management

#### Using .python-version

We include a `.python-version` file for tools like `pyenv` and `asdf`:

```bash
# With pyenv installed:
pyenv install 3.10
pyenv local 3.10

# With asdf installed:
asdf install python 3.10
```

#### Using pyenv (Recommended)

```bash
# Install pyenv (macOS)
brew install pyenv

# Install pyenv (Linux)
curl https://pyenv.run | bash

# Install Python 3.10
pyenv install 3.10

# Set local version
pyenv local 3.10
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-new-feature
```

### 2. Make Changes

Edit code following our style guide (Ruff will help enforce this).

### 3. Run Quality Checks

```bash
# Quick check with Ruff
just lint

# Full quality check
just quality

# Run tests
just test-cov
```

### 4. Commit Changes

Pre-commit hooks will run automatically:

```bash
git add .
git commit -m "feat: add new feature"
```

### 5. Push and Create PR

```bash
git push origin feature/my-new-feature
```

## Testing

### Running Tests

```bash
# Run all tests
pytest wavetable_tests/

# With coverage
pytest wavetable_tests/ --cov=wavetable_synthesis --cov-report=html

# Verbose output
pytest wavetable_tests/ -v

# Specific test file
pytest wavetable_tests/test_wavetable_generation.py

# Specific test function
pytest wavetable_tests/test_wavetable_generation.py::test_sine_to_triangle
```

### Using Make/Just

```bash
make test              # Run tests
make test-cov          # Run with coverage
make test-verbose      # Verbose output

just test              # Run tests
just test-cov          # Run with coverage
just test-verbose      # Verbose output
```

### Coverage Requirements

-  Maintain **90%+ code coverage**
-  All new code should include tests
-  Test both success and failure cases

## Code Quality

### Linting and Formatting

```bash
# Check code style (Ruff)
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .

# All in one (recommended)
make format
# or
just format
```

### Type Checking

```bash
# Check types
mypy wavetable_synthesis/ --strict

# Using Make/Just
make type-check
just type-check
```

### Legacy Tools (for migration period)

```bash
# Run legacy tools
make lint-legacy
make format-legacy

just lint-legacy
just format-legacy
```

## Creating New Generators

See [docs/wavetable_generators.md](docs/wavetable_generators.md) for detailed instructions.

Quick version:

```bash
# Copy template
cp wavetable_generators/example.py wavetable_generators/my_generator.py

# Edit the file
# ... implement your generator ...

# Test it
python -m wavetable_synthesis my_generator

# Run tests
pytest wavetable_tests/ -k my_generator
```

## IDE Setup

### VS Code (Recommended)

The project includes `.vscode/settings.json` with recommended settings:

1.  Install Python extension
2.  Install Ruff extension (recommended)
3.  Reload window
4.  Settings will be applied automatically

**Recommended Extensions:**

-  Python (ms-python.python)
-  Ruff (charliermarsh.ruff)
-  Pylance (ms-python.vscode-pylance)
-  Better TOML (bungcip.better-toml)

### PyCharm

1.  Open project
2.  Configure Python interpreter to `.venv/bin/python`
3.  Enable Ruff in settings (if plugin available)
4.  Configure mypy external tool

## Dependency Management

### Installing Dependencies

```bash
# Production dependencies only
pip install -e .

# With dev dependencies
pip install -e ".[dev]"

# Update all dependencies
make update-deps
just update-deps
```

### Adding Dependencies

1.  Add to `pyproject.toml` under `dependencies` or `dev`
2.  Install: `pip install -e ".[dev]"`
3.  Update lockfile if using pip-tools or poetry

## Troubleshooting

### Virtual Environment Issues

```bash
# Remove and recreate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # or .venv/Scripts/activate on Windows
pip install -e ".[dev]"
```

### Pre-commit Hook Issues

```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install

# Clear cache
pre-commit clean
pre-commit run --all-files
```

### Ruff Not Found

```bash
# Install Ruff
pip install ruff

# Or reinstall dev dependencies
pip install -e ".[dev]"
```

### Import Errors

```bash
# Reinstall in editable mode
pip install -e .
```

## Performance Tips

### Use Ruff Instead of Multiple Tools

```bash
# Slow (multiple tools)
black . && isort . && flake8 . && pylint .

# Fast (single tool)
ruff check --fix . && ruff format .
```

### Parallel Testing

```bash
# Run tests in parallel
pytest wavetable_tests/ -n auto
```

## Additional Resources

-  [Ruff Documentation](https://docs.astral.sh/ruff/)
-  [Just Documentation](https://github.com/casey/just)
-  [Pre-commit Documentation](https://pre-commit.com/)
-  [pytest Documentation](https://docs.pytest.org/)
-  [MyPy Documentation](https://mypy.readthedocs.io/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## Need Help?

-  Check existing issues on GitHub
-  Review documentation in `docs/`
-  Look at existing code examples
-  Ask questions in GitHub Discussions
