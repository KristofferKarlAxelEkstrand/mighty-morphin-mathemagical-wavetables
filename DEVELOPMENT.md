# Development Guide

Modern development setup for Mighty Morphin Mathemagical Wavetables.

## Quick Start

### Prerequisites

- **Python 3.10+** (3.10, 3.11, 3.12, or 3.13)
- **Git** for version control

### Setup

```bash
# Clone the repository
git clone https://github.com/KristofferKarlAxelEkstrand/mighty-morphin-mathemagical-wavetables.git
cd mighty-morphin-mathemagical-wavetables

# Run setup script (recommended)
bash setup.sh

# Or manually:
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or: source .venv/Scripts/activate  # Windows Git Bash
pip install -e ".[dev]"
pre-commit install
```

## Development Tools

### Ruff - Fast Linting & Formatting

[Ruff](https://docs.astral.sh/ruff/) is our all-in-one linter and formatter - 10-100x faster than traditional tools.

```bash
# Check code quality
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .

# Or use Make:
make lint
make format
```

### Make - Task Runner

All common commands are available via Make:

```bash
make help          # Show all available commands
make install-dev   # Install dev dependencies
make test          # Run tests
make test-cov      # Run tests with coverage
make lint          # Check code quality
make format        # Format code
make quality       # Run all quality checks
make list          # List generators
make run GEN=name  # Run specific generator
```

### Pre-commit Hooks

Automatically check code quality before commits:

```bash
# Install hooks (one-time)
pre-commit install

# Hooks run automatically on git commit
git commit -m "your message"

# Run manually
pre-commit run --all-files
```

**What gets checked:**

- Ruff linting and formatting
- Type checking with mypy
- File quality (trailing whitespace, EOF, etc.)
- YAML/JSON/TOML syntax
- Markdown linting
- Security checks with Bandit

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-feature
```

### 2. Make Changes

Edit code following the project style (Ruff enforces this).

### 3. Test & Lint

```bash
make format    # Format code
make test      # Run tests
make quality   # Check quality
```

### 4. Commit

```bash
git add .
git commit -m "feat: add new feature"
# Pre-commit hooks run automatically
```

### 5. Push

```bash
git push origin feature/my-feature
```

## Testing

```bash
# Run all tests
pytest wavetable_tests/
# or: make test

# With coverage
pytest wavetable_tests/ --cov=wavetable_synthesis --cov-report=html
# or: make test-cov

# Verbose output
pytest wavetable_tests/ -v

# Specific test file
pytest wavetable_tests/test_wavetable_generation.py
```

**Coverage requirement:** 90%+

## Code Quality

### Linting

```bash
# Check code style
ruff check .

# Auto-fix issues
ruff check --fix .

# Using Make
make lint
```

### Formatting

```bash
# Format code
ruff format .

# Format and fix
make format
```

### Type Checking

```bash
# Check types
mypy wavetable_synthesis/ --strict

# Using Make
make type-check
```

### All Checks

```bash
make quality
```

## Creating Generators

Quick guide - see [docs/wavetable_generators.md](docs/wavetable_generators.md) for details.

```bash
# 1. Copy template
cp wavetable_generators/example.py wavetable_generators/my_generator.py

# 2. Edit and implement
# - Extend BaseGenerator
# - Use @register_generator("name")
# - Implement generate(theta, u)

# 3. Test it
python -m wavetable_synthesis my_generator
make test
```

## IDE Setup

### VS Code

Recommended extensions (auto-configured in `.vscode/settings.json`):

- Python (ms-python.python)
- Ruff (charliermarsh.ruff)
- Pylance (ms-python.vscode-pylance)

### Dev Containers

Open in VS Code with dev containers for instant setup - everything pre-configured.

## Python Version Management

The project includes a `.python-version` file for tools like `pyenv`:

```bash
# With pyenv
pyenv install 3.10
pyenv local 3.10

# With asdf
asdf install python 3.10
```

## Common Tasks

```bash
# Setup
make install-dev       # Install dependencies
make pre-commit        # Install git hooks

# Development
make test              # Run tests
make format            # Format code
make lint              # Check quality
make quality           # All quality checks

# Generators
make list              # List generators
make run GEN=example   # Run generator
make validate          # Validate all
make batch             # Generate all

# Utilities
make clean             # Clean build artifacts
make update-deps       # Update dependencies
```

## Troubleshooting

### Virtual Environment Issues

```bash
# Remove and recreate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Pre-commit Hook Issues

```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install

# Clear cache
pre-commit clean
```

### Import Errors

```bash
# Reinstall in editable mode
pip install -e .
```

## Resources

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Pre-commit Documentation](https://pre-commit.com/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.
