# Development Environment Setup

This project uses consistent formatting and linting settings to ensure code quality across all contributors.

## Automatic Setup

When you open this project in VS Code:

1.  **Python formatting** runs automatically on save (Black + isort)
2.  **Markdown/JSON formatting** runs automatically on save (Prettier)
3.  **Linting** runs automatically on save (pylint, mypy, flake8)
4.  **Virtual environment** is automatically detected

## EditorConfig

The `.editorconfig` file ensures consistent settings across different editors:

-  **Python**: 4 spaces, line length 88
-  **Markdown**: 2 spaces, line length 200
-  **JSON/YAML**: 2 spaces
-  **UTF-8 encoding**, LF line endings

## VS Code Extensions (Recommended)

For the best experience, install these extensions:

-  **Python** (ms-python.python) - Language support
-  **Pylint** (ms-python.pylint) - Linting
-  **Black Formatter** (ms-python.black-formatter) - Formatting
-  **Prettier** (esbenp.prettier-vscode) - Markdown/JSON formatting
-  **EditorConfig** (editorconfig.editorconfig) - Cross-editor consistency

## Pre-commit Hooks

The project uses husky and lint-staged to run formatting and linting before commits:

-  Python files: Black formatting + isort import sorting
-  Markdown: Prettier + markdownlint
-  JSON/YAML: Prettier

Run `npm install` to set up the hooks.

## Manual Commands

If needed, you can run formatting/linting manually:

```bash
# Format all files
npm run format:fix

# Python formatting
source .venv/Scripts/activate && black . && isort .

# Check linting
source .venv/Scripts/activate && pylint wavetable_synthesis/ --score=no
```

## Consistency Benefits

-  **Team consistency**: Everyone gets the same formatting
-  **CI/CD ready**: Code is always properly formatted
-  **Editor agnostic**: Works with VS Code, Vim, Emacs, etc.
-  **Automated**: No manual formatting required
