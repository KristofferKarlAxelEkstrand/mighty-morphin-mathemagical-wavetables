# Python - Core Programming Language

## What is Python?

Python is the primary programming language used in this project.
It's a high-level, interpreted language known for its clean syntax, powerful standard library,
and excellent support for scientific computing and audio processing.

This project uses **Python 3.10+** with modern features like type hints, dataclasses, and pattern matching.

## Why We Use Python

**Scientific Computing**: Python has excellent libraries for numerical computations (NumPy) and audio processing (soundfile), making it perfect for wavetable synthesis.

**Readable Code**: Python's clear syntax makes mathematical algorithms easy to understand and maintain - critical for an educational project.

**Type Safety**: Modern Python (3.10+) with type hints provides strong type checking while keeping code readable.

**Modern Tooling**: Fast, efficient tools like Ruff for linting/formatting, mypy for type checking, and pytest for testing.

**Cross-Platform**: Works on Windows, macOS, and Linux without code changes.

## Core Libraries

**NumPy (≥2.0.0)**

- IEEE 754 double-precision floating-point calculations
- Vectorized array operations for performance
- Mathematical functions (sin, cos, arcsin, etc.)
- Phase and waveform generation

**soundfile (≥0.13.0)**

- WAV file export (16/24/32-bit)
- Professional audio format support
- Sample rate and bit depth control

## Development Tools

**Ruff** - Ultra-fast linter and formatter

- Replaces Black, isort, Flake8, and many Pylint rules
- 10-100x faster than traditional tools
- Auto-fixes most issues
- Zero configuration needed

**mypy** - Static type checker

- Strict mode enabled
- Catches type errors before runtime
- Full type hint coverage required

**pytest** - Testing framework

- 90%+ code coverage required
- Fast, expressive test syntax
- Comprehensive test suite

**Bandit** - Security linter

- Detects security issues
- Integrated into pre-commit hooks

## Modern Python Features Used

**Type Hints (Full Coverage)**

```python
from numpy.typing import NDArray
import numpy as np

def generate(
    self,
    theta: NDArray[np.float64],
    u: float,
) -> NDArray[np.float64]:
    """Generate waveform with type safety."""
    ...
```

**Dataclasses (Clean Data Structures)**

```python
from dataclasses import dataclass, field

@dataclass
class MyGenerator(BaseGenerator):
    name: str = "my_generator"
    tags: list[str] = field(default_factory=lambda: ["example"])
```

**Decorators (Auto-Registration)**

```python
@register_generator("sine_to_triangle")
class SineToTriangleGenerator(BaseGenerator):
    """Automatically registered on import."""
    ...
```

## Development Dependencies

```toml
[project.optional-dependencies]
dev = [
    # Testing
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    # Linting and formatting
    "ruff>=0.9.0",
    # Type checking
    "mypy>=1.13.0",
    # Security
    "bandit[toml]>=1.8.0",
    # Pre-commit hooks
    "pre-commit>=4.0.0",
]
```

## Code Quality Commands

### Linting and Formatting

```bash
# Check code quality
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .

# Or use Make
make lint
make format
```

### Type Checking

```bash
# Check types
mypy wavetable_synthesis/ --strict

# Or use Make
make type-check
```

### Testing

```bash
# Run tests
pytest wavetable_tests/

# With coverage
pytest wavetable_tests/ --cov=wavetable_synthesis

# Or use Make
make test
make test-cov
```

### All Checks

```bash
make quality
```

## CI/CD Integration

All quality checks run automatically in GitHub Actions:

- Ruff linting and formatting
- mypy type checking
- pytest with coverage
- Bandit security scanning

## Best Practices

1. **Type Everything**: All functions must have complete type hints
2. **Test Everything**: Maintain 90%+ test coverage
3. **Format Automatically**: Let Ruff handle formatting
4. **Use Modern Features**: Leverage Python 3.10+ capabilities
5. **Keep It Simple**: Clear code over clever code

## Resources

- [Python Documentation](https://docs.python.org/3/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
