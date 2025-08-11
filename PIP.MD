# pip Reference Guide

Essential pip commands and best practices for Python package management.

## Package Management

### List Packages

```bash
# List all installed packages
pip list

# List outdated packages
pip list --outdated

# Show details about a specific package
pip show package-name
```

### Installing Packages

```bash
# Install a specific package
pip install package-name

# Install a specific version
pip install package-name==1.2.3

# Install with version constraints
pip install "package-name>=1.0.0,<2.0.0"

# Install from requirements file
pip install -r requirements.txt

# Install project in development mode (editable)
pip install -e .

# Install with optional dependencies
pip install -e ".[dev]"
pip install -e ".[web]"
pip install -e ".[dev,web,docs]"
```

### Upgrading Packages

```bash
# Upgrade specific package
pip install --upgrade package-name

# Upgrade pip itself
pip install --upgrade pip

# Upgrade all packages in pyproject.toml (development mode)
pip install -e ".[dev]" --upgrade

# Use pip-review for batch upgrades (optional tool - install separately)
pip install pip-review        # First, install pip-review
pip-review                    # List outdated packages
pip-review --interactive      # Choose which to upgrade
pip-review --auto             # Upgrade all automatically
```

### Uninstalling Packages

```bash
# Uninstall a package
pip uninstall package-name

# Uninstall multiple packages
pip uninstall package1 package2

# Uninstall all packages (use with caution!)
pip freeze | xargs pip uninstall -y
```

## Virtual Environments

### Creating and Using Virtual Environments

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/Scripts/activate    # Windows (Git Bash)
.venv\Scripts\activate          # Windows (CMD)
source .venv/bin/activate       # Linux/Mac

# Deactivate virtual environment
deactivate

# Check which Python is active
which python                     # Linux/Mac/Git Bash
where python                     # Windows CMD
```

### Auto-Activation in This Project

This project automatically activates the virtual environment when you enter the directory (if you have the code added to your `~/.bashrc`).

The auto-activation is configured in:

-  `.envrc` - for direnv users
-  `auto_activate.sh` - manual activation script
-  Your `~/.bashrc` - automatic activation on directory change

### Why Use Virtual Environments?

-  Isolate project dependencies
-  Avoid version conflicts between projects
-  Easy to reproduce environments
-  Keep system Python clean
-  **Auto-activation** when entering project directory

## Requirements Management

### Generating Requirements Files

```bash
# Generate requirements.txt from current environment
pip freeze > requirements.txt

# Generate minimal requirements (direct dependencies only)
pip list --not-required --format=freeze > requirements.txt
```

### Working with pyproject.toml (Modern Python)

This project uses `pyproject.toml` instead of `requirements.txt`:

```toml
[project]
dependencies = [
    "numpy>=2.0.0",
    "soundfile>=0.13.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    "black>=24.0.0",
]
```

Install with:

```bash
pip install -e .              # Install base dependencies
pip install -e ".[dev]"       # Install with dev dependencies
```

## Useful Commands

### Package Information

```bash
# Check pip version
pip --version

# Get help for a command
pip help install

# List files installed by a package
pip show --files package-name

# Search PyPI for packages (deprecated, use pypi.org website)
# pip search is no longer available
```

### Dependency Analysis

```bash
# Show dependency tree (requires pipdeptree - install separately)
pip install pipdeptree
pipdeptree

# Check for dependency conflicts
pip check

# Show what would be installed (dry run)
pip install --dry-run package-name
```

### Cache Management

```bash
# Show cache information
pip cache info

# List cached packages
pip cache list

# Remove all cache
pip cache purge

# Install without using cache
pip install --no-cache-dir package-name
```

## Best Practices

### 1. Always Use Virtual Environments

Never install packages globally. Use virtual environments for isolation.

### 2. Pin Dependencies for Production

Use specific versions in production:

```bash
numpy==2.3.4
```

Use version ranges for development:

```bash
numpy>=2.0.0
```

### 3. Keep Dependencies Updated

Regularly check for updates:

```bash
pip list --outdated
```

### 4. Use Editable Installs for Development

Install your project in development mode:

```bash
pip install -e ".[dev]"
```

This allows you to modify code without reinstalling.

### 5. Document Dependencies

Keep `pyproject.toml` or `requirements.txt` up to date.

### 6. Upgrade pip Regularly

```bash
pip install --upgrade pip
```

### 7. Use Version Control

Add to `.gitignore`:

```gitignore
.venv/
*.pyc
__pycache__/
```

Never commit virtual environments to git.

## Troubleshooting

### Common Issues

**Package won't install:**

```bash
# Try upgrading pip first
pip install --upgrade pip

# Install with verbose output
pip install -v package-name

# Force reinstall
pip install --force-reinstall package-name
```

**Permission errors:**

```bash
# Use virtual environment instead of --user or sudo
python -m venv .venv
source .venv/Scripts/activate
pip install package-name
```

**Dependency conflicts:**

```bash
# Check for conflicts
pip check

# Show dependency tree (requires pipdeptree - install separately)
pip install pipdeptree
pipdeptree
```

**SSL/Certificate errors:**

```bash
# Upgrade certifi
pip install --upgrade certifi

# Or temporarily use trusted host (not recommended)
pip install --trusted-host pypi.org package-name
```

## Quick Reference

| Command                         | Description                          |
| ------------------------------- | ------------------------------------ |
| `pip list`                      | List installed packages              |
| `pip list --outdated`           | Show packages with updates available |
| `pip install package`           | Install a package                    |
| `pip install --upgrade package` | Upgrade a package                    |
| `pip uninstall package`         | Remove a package                     |
| `pip show package`              | Show package details                 |
| `pip check`                     | Verify dependencies                  |
| `pip freeze`                    | Output installed packages            |
| `pip install -e .`              | Install project in editable mode     |
| `pip install -e ".[dev]"`       | Install with optional dependencies   |

## Project-Specific Commands

For this wavetable-synthesis project:

```bash
# Initial setup
source .venv/Scripts/activate
pip install --upgrade pip
pip install -e ".[dev]"

# Check for updates
pip list --outdated

# Upgrade all packages
pip install -e ".[dev]" --upgrade

# Optional: Use pip-review for easier upgrade management
pip install pip-review
pip-review                    # Check for outdated packages
pip-review --interactive      # Choose which to upgrade

# Run tests after upgrade
pytest

# Check types
mypy src/wavetable_synthesis

# Check code quality
pylint src/wavetable_synthesis
```

## Additional Resources

-  [pip Documentation](https://pip.pypa.io/)
-  [Python Packaging Guide](https://packaging.python.org/)
-  [PyPI - Python Package Index](https://pypi.org/)
-  [pip-review Tool](https://github.com/jgonggrijp/pip-review)
