# Development Environment Setup

This project uses modern Python tooling for consistent code quality across all contributors.

## Automatic Setup

When you open this project in VS Code:

1. **Python formatting and linting** runs automatically on save (Ruff)
2. **Markdown/JSON formatting** runs automatically on save (Prettier)
3. **Type checking** runs automatically (mypy)
4. **Virtual environment** is automatically detected

## EditorConfig

The `.editorconfig` file ensures consistent settings across different editors:

- **Python**: 4 spaces, line length 128
- **Markdown**: 2 spaces, line length 200
- **JSON/YAML**: 2 spaces
- **UTF-8 encoding**, LF line endings

## VS Code Extensions (Recommended)

For the best experience, install these extensions:

- **Python** (ms-python.python) - Language support
- **Ruff** (charliermarsh.ruff) - Fast linting and formatting
- **Pylance** (ms-python.vscode-pylance) - IntelliSense and type checking
- **Prettier** (esbenp.prettier-vscode) - Markdown/JSON formatting
- **EditorConfig** (editorconfig.editorconfig) - Cross-editor consistency

## Pre-commit Hooks

The project uses pre-commit hooks to run quality checks before commits:

- Python files: Ruff formatting and linting, mypy type checking
- Markdown: Prettier + markdownlint
- JSON/YAML: Prettier
- Security: Bandit checks

Install with: `pre-commit install`

## Manual Commands

If needed, you can run checks manually:

```bash
# Format all files
make format

# Python formatting and linting
source .venv/Scripts/activate && ruff format . && ruff check --fix .

# Check types
source .venv/Scripts/activate && mypy wavetable_synthesis/ --strict

# Or use Make for all checks
make quality
```

## Consistency Benefits

- **Modern tooling**: 10-100x faster than legacy tools
- **Team consistency**: Everyone gets the same formatting
- **CI/CD ready**: Code is always properly formatted
- **Editor agnostic**: Works with VS Code, Vim, Emacs, etc.
- **Automated**: No manual formatting required
