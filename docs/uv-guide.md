# uv - Extremely Fast Python Package Installer

<https://github.com/astral-sh/uv>

This guide shows how to use uv with this project for faster dependency installation.

## Installation

### macOS/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### With pip

```bash
pip install uv
```

## Usage

### Create virtual environment

```bash
uv venv
```

### Activate virtual environment (same as regular venv)

```bash
source .venv/bin/activate  # Linux/macOS
source .venv/Scripts/activate  # Windows Git Bash
```

### Install dependencies (much faster than pip!)

```bash
uv pip install -e ".[dev]"
```

### Sync dependencies from pyproject.toml

```bash
uv pip sync pyproject.toml
```

### Install a package

```bash
uv pip install ruff
```

### Upgrade all dependencies

```bash
uv pip install --upgrade -e ".[dev]"
```

## Benefits

- 10-100x faster than pip for dependency resolution
- Compatible with existing pip workflows
- No changes needed to pyproject.toml
- Drop-in replacement for pip commands

## Migration from pip

Replace `pip` with `uv pip` in your commands:

```bash
# Before (pip)
pip install -e ".[dev]"

# After (uv)
uv pip install -e ".[dev]"
```

## CI/CD Integration

Add to GitHub Actions workflow:

```yaml
- name: Install uv
  run: curl -LsSf https://astral.sh/uv/install.sh | sh

- name: Install dependencies with uv
  run: uv pip install -e ".[dev]"
```

## Notes

- uv is from the same team that created Ruff
- Written in Rust for maximum performance
- Fully compatible with pip and existing tools
- No lock file needed (uses pyproject.toml)
