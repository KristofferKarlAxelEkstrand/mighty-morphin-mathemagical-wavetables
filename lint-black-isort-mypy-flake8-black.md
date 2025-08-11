# Python Code Quality Tools

This document explains the linting and formatting tools used in the wavetable synthesis project.

## Overview

The project uses a comprehensive set of Python code quality tools to ensure consistent, readable, and maintainable code:

-  **Black** - Code formatter (uncompromising)
-  **isort** - Import organizer
-  **mypy** - Static type checker
-  **flake8** - Style guide enforcement
-  **pylint** - Code quality analyzer

## Tools Configuration

### Black (Code Formatter)

**Purpose**: Automatically formats Python code to a consistent style.

**Configuration**:

-  Line length: 88 characters
-  Target Python versions: 3.10+
-  String quotes: Double quotes preferred

**Usage**:

```bash
# Format specific files
python -m black file.py

# Format entire directories
python -m black wavetable_synthesis/ wavetable_generators/ wavetable_tests/

# Check what would be changed (dry run)
python -m black --check wavetable_synthesis/
```

**VS Code Integration**:

-  Formats on save automatically
-  Uses `ms-python.black-formatter` extension
-  Configured in `.vscode/settings.json`

### isort (Import Organizer)

**Purpose**: Sorts and organizes Python imports alphabetically and by type.

**Configuration**:

-  Profile: `black` (compatible with Black formatting)
-  Multi-line imports: Vertical hanging indent
-  Known first party: `wavetable_synthesis`

**Usage**:

```bash
# Sort imports in specific files
python -m isort file.py

# Sort imports in entire directories
python -m isort wavetable_synthesis/ wavetable_generators/ wavetable_tests/

# Check what would be changed (dry run)
python -m isort --check-only wavetable_synthesis/
```

**VS Code Integration**:

-  Organizes imports on save automatically
-  Uses `ms-python.isort` extension
-  Triggered by `source.organizeImports` code action

### mypy (Static Type Checker)

**Purpose**: Checks Python code for type errors and inconsistencies.

**Configuration**:

-  Mode: `--strict` (maximum type checking)
-  Python version: 3.10+
-  Error codes: Enabled
-  Platform: Configurable

**Usage**:

```bash
# Type check specific files
python -m mypy file.py

# Type check entire package
python -m mypy wavetable_synthesis/

# Type check with detailed error codes
python -m mypy wavetable_synthesis/ --strict --show-error-codes

# Type check with HTML report
python -m mypy wavetable_synthesis/ --html-report mypy-report/
```

**VS Code Integration**:

-  Runs automatically on save
-  Uses `ms-python.mypy-type-checker` extension
-  Shows inline type hints with Pylance

### flake8 (Style Guide Enforcement)

**Purpose**: Enforces PEP 8 style guide and catches common errors.

**Configuration**:

-  Max line length: 88 characters (matches Black)
-  Excluded files: Auto-generated files
-  Extended ignore rules: Configurable

**Usage**:

```bash
# Check specific files
python -m flake8 file.py

# Check entire directories
python -m flake8 wavetable_synthesis/ wavetable_generators/ wavetable_tests/

# Show statistics
python -m flake8 wavetable_synthesis/ --statistics

# Show only errors (no warnings)
python -m flake8 wavetable_synthesis/ --select=E
```

**VS Code Integration**:

-  Runs automatically on save
-  Uses `ms-python.flake8` extension
-  Shows problems in VS Code Problems panel

### pylint (Code Quality Analyzer)

**Purpose**: Comprehensive code quality analysis and bug detection.

**Configuration**:

-  Score threshold: Enabled
-  Reports: Text output
-  Extensions: Custom checks disabled

**Usage**:

```bash
# Analyze specific files
python -m pylint file.py

# Analyze entire directories
python -m pylint wavetable_synthesis/ wavetable_generators/ wavetable_tests/

# Show only score
python -m pylint wavetable_synthesis/ --score-only

# Generate HTML report
python -m pylint wavetable_synthesis/ --output-format=json | pylint-json2html -o pylint-report.html
```

**VS Code Integration**:

-  Runs automatically on save
-  Uses `ms-python.pylint` extension
-  Shows detailed problems with severity levels

## Combined Usage

### Format and Lint All Code

```bash
# One-liner to format and lint everything
python -m black wavetable_synthesis/ wavetable_generators/ wavetable_tests/ && \
python -m isort wavetable_synthesis/ wavetable_generators/ wavetable_tests/ && \
python -m pylint wavetable_synthesis/ wavetable_generators/ wavetable_tests/ && \
python -m mypy wavetable_synthesis/ && \
python -m flake8 wavetable_synthesis/ wavetable_generators/ wavetable_tests/
```

### VS Code Tasks

Use these VS Code tasks for common operations:

-  **Format & Lint All** (`Ctrl+Shift+B`) - Complete format and lint cycle
-  **Format Python** - Format with Black and isort only
-  **Type Check (mypy)** - Run mypy type checking
-  **Lint Python** - Run pylint analysis

### NPM Scripts

Use these npm scripts for manual quality checks:

```bash
# Python linting and formatting
npm run lint:py              # Run flake8 on Python files
npm run lint:py:fix          # Format Python files with Black and isort
npm run type:check           # Run mypy type checking
npm run quality:check        # Run pylint code quality analysis

# Combined operations
npm run format:fix           # Format all files (Markdown, JSON, YAML, Python)
```

**Note**: All Python scripts automatically use the virtual environment (`.venv`) - no manual activation required.

### Pre-commit Hooks

The project uses husky and lint-staged for automatic quality checks:

```bash
# Run all pre-commit checks manually
npm run format:fix && npm run lint:md:fix

# Install hooks (runs automatically with npm install)
npm run prepare
```

**Pre-commit checks include:**

-  **Python files**: Black formatting, isort import sorting, flake8 linting
-  **Markdown files**: Prettier formatting, markdownlint
-  **Config files**: Prettier formatting (JSON, YAML, YML)

## Quality Standards

### Code Style

-  **Black formatting**: 88 character line length
-  **isort imports**: Alphabetical, grouped by type
-  **PEP 8 compliance**: Enforced by flake8
-  **Type hints**: Required for all functions and methods

### Quality Metrics

-  **pylint score**: Target > 9.0/10
-  **Test coverage**: Target > 90%
-  **mypy**: Zero type errors
-  **flake8**: Zero style violations

### File Organization

-  **Imports**: Standard library, third-party, local (blank lines between groups)
-  **Line length**: 88 characters maximum
-  **Docstrings**: Google/NumPy style for all public functions
-  **Type hints**: Full type annotation for parameters and return values

## Troubleshooting

### Common Issues

**Black and isort conflicts**:

```bash
# Run isort after Black to ensure compatibility
python -m black file.py && python -m isort file.py
```

**mypy import errors**:

```bash
# Ensure all dependencies are installed
pip install -e .[dev]
```

**pylint false positives**:

```bash
# Use noqa comments for justified exceptions
def function_with_pragma():  # noqa: some-error-code
    pass
```

### VS Code Issues

**Formatters not working**:

1.  Check Python interpreter is set to `.venv/Scripts/python`
2.  Ensure extensions are installed and enabled
3.  Reload VS Code window

**Linting errors not showing**:

1.  Check language server is Pylance
2.  Verify linting is enabled in settings
3.  Check Python path in VS Code

## Integration with CI/CD

For continuous integration, use these commands:

```yaml
# GitHub Actions example
- name: Lint and Format
  run: |
    python -m black --check wavetable_synthesis/ wavetable_generators/ wavetable_tests/
    python -m isort --check-only wavetable_synthesis/ wavetable_generators/ wavetable_tests/
    python -m flake8 wavetable_synthesis/ wavetable_generators/ wavetable_tests/
    python -m mypy wavetable_synthesis/
    python -m pylint wavetable_synthesis/ wavetable_generators/ wavetable_tests/ --score-only --fail-under=9.0
```

## Best Practices

1.  **Run formatters before committing** - Use pre-commit hooks
2.  **Fix linter errors immediately** - Don't accumulate technical debt
3.  **Use type hints consistently** - Helps catch bugs early
4.  **Review automated changes** - Formatters aren't always perfect
5.  **Keep configurations in sync** - Update tool configs together

## Tool Versions

Current versions in `pyproject.toml`:

-  black: Latest compatible
-  isort: Latest compatible
-  mypy: Latest compatible
-  flake8: Latest compatible
-  pylint: Latest compatible

Update regularly with:

```bash
pip install --upgrade black isort mypy flake8 pylint
```
