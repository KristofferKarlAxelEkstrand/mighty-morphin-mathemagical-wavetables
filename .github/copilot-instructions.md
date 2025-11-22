# GitHub Copilot Instructions

This document provides instructions for GitHub Copilot coding agent when working with the Mighty Morphin Mathemagical Wavetables project.

## Project Overview

**Mighty Morphin Mathemagical Wavetables** is a Python library for generating professional audio wavetables using mathematical synthesis techniques. The project emphasizes:

- **Educational Focus**: Learning programming, mathematics, and audio concepts
- **Clean Code**: Modern Python with comprehensive testing and documentation
- **Mathematical Purity**: All wavetables created through formulas, not samples

## Tech Stack

- **Python 3.10+** with type hints
- **NumPy 2.0+** for numerical computations
- **SoundFile** for WAV file I/O
- **pytest** for testing (90%+ coverage required)
- **Modern packaging** with pyproject.toml
- **Linting**: Black, isort, MyPy, Pylint, Flake8

## Key Commands

### Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Windows/Git Bash
source .venv/bin/activate      # Linux/macOS

# Install in development mode
pip install -e .[dev]
```

### Testing
```bash
# Run all tests with coverage
pytest --cov=wavetable_synthesis --cov-report=html

# Run specific test file
pytest wavetable_tests/test_wavetable_generation.py
```

### Code Quality
```bash
# Format code
black wavetable_synthesis/ wavetable_generators/ wavetable_tests/
isort --profile black wavetable_synthesis/ wavetable_generators/ wavetable_tests/

# Type checking
mypy --strict wavetable_synthesis/

# Linting
flake8 wavetable_synthesis/ wavetable_generators/ wavetable_tests/
pylint wavetable_synthesis/ wavetable_generators/ wavetable_tests/
```

### Generate Wavetables
```bash
# List available generators
python -m wavetable_synthesis --list

# Generate single wavetable
python -m wavetable_synthesis example

# Generate all wavetables
python -m wavetable_synthesis --batch
```

## Project Structure

```
wavetable_synthesis/     # Core library
├── cli/                # Command-line interface
├── core/               # Base classes and processing
│   ├── base_generator.py
│   ├── decorator_registry.py
│   ├── generator.py
│   └── processing.py
└── export/             # WAV file export

wavetable_generators/   # Generator implementations
├── example.py          # Template generator
├── linear_interpolation.py
├── sine_to_triangle.py
└── square_pwm_tz.py

wavetable_tests/        # Comprehensive test suite
```

## Code Quality Standards

### Type Hints
- Use full type annotations with `numpy.typing.NDArray`
- All public functions must have type hints
- Use `mypy --strict` for type checking

### Testing
- Maintain minimum 90% test coverage
- Use pytest fixtures from `conftest.py`
- Test both success and error cases
- Follow existing test patterns

### Code Style
- Black formatting with 128 character line length
- Import sorting with isort (Black profile)
- Follow existing code patterns
- Clear, descriptive variable names
- Comprehensive docstrings

## Guidelines for Changes

### When Adding Features
1. **Check existing code first** - Follow established patterns
2. **Add tests** - Write tests before or alongside implementation
3. **Update documentation** - Keep docs in sync with code
4. **Run quality checks** - Black, isort, mypy, pylint, flake8
5. **Verify coverage** - Ensure 90%+ test coverage

### When Creating Generators
1. **Copy example.py** as a template
2. **Extend BaseGenerator** class
3. **Implement generate(theta, u)** method
   - `theta`: phase array (0 to 2π)
   - `u`: morph parameter (0 to 1)
4. **Use decorator** `@register_generator("name")`
5. **Add validation** with `_validate_u(u)`
6. **Write tests** in `wavetable_tests/`
7. **Test CLI** with `python -m wavetable_synthesis generator_name`

### Files Not to Modify
- `.github/agents/` - Agent configuration files
- `.husky/` - Pre-commit hooks
- `package-lock.json` - Auto-generated npm lockfile
- `node_modules/` - Dependencies (not in repo)
- `.venv/` - Virtual environment (not in repo)

### Performance Philosophy
- **Offline generation** - Not real-time, pre-rendering is acceptable
- **Core efficiency** - Keep processing, export, CLI performant
- **Generator clarity** - Prioritize readability over speed in generators
- **Educational value** - Code should be clear for beginners

## Common Tasks

### Bug Fixes
1. Identify the issue with existing tests
2. Add a test that reproduces the bug
3. Fix the issue with minimal changes
4. Verify all tests pass
5. Check code quality with linters

### Documentation Updates
1. Update relevant markdown files in `docs/`
2. Update docstrings in code
3. Keep AGENTS.md in sync if needed
4. Verify markdown formatting

### Refactoring
1. Ensure tests cover existing behavior
2. Make incremental changes
3. Run tests frequently
4. Maintain type safety
5. Keep coverage above 90%

## Communication Style

When working on this project:

- **Keep it simple** - Use everyday language, not jargon
- **Be a teacher** - Explain what you're doing and why
- **Stay grounded** - No decorative language or emojis
- **Be precise** - Technically correct, accurate code examples

See AGENTS.md for detailed communication guidelines.

## Additional Resources

- **AGENTS.md** - Comprehensive agent instructions
- **CONTRIBUTING.md** - Contribution guidelines
- **docs/** - User documentation
- **docs_tech/** - Technical documentation
- **QUICKSTART.md** - Quick start guide
