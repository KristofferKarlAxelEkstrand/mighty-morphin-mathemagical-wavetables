# Python - Core Programming Language

## What is Python?

Python is the primary programming language used in this project. It's a high-level, interpreted language known for its clean syntax, powerful
standard library, and excellent support for scientific computing and audio processing.

This project uses **Python 3.10+** with modern features like type hints, dataclasses, and pattern matching.

## Why We Use Python

**Scientific Computing**: Python has excellent libraries for numerical computations (NumPy) and audio processing (soundfile), making it perfect for wavetable synthesis.

**Readable Code**: Python's clear syntax makes mathematical algorithms easy to understand and maintain - critical for an educational project.

**Type Safety**: Modern Python (3.10+) with type hints provides strong type checking while keeping code readable.

**Rich Ecosystem**: Extensive tooling for testing (pytest), linting (pylint, flake8), type checking (mypy), and formatting (black).

**Cross-Platform**: Works on Windows, macOS, and Linux without code changes.

## How We Use Python in This Project

### Core Libraries

**NumPy (≥2.0.0)**

-  IEEE 754 double-precision floating-point calculations
-  Vectorized array operations for performance
-  Mathematical functions (sin, cos, arcsin, etc.)
-  Phase and waveform generation

**soundfile (≥0.13.0)**

-  WAV file export (16/24/32-bit)
-  Professional audio format support
-  Sample rate and bit depth control

### Project Structure

```text
wavetable_synthesis/          # Main package
├── core/                     # Core generation engine
│   ├── base_generator.py     # Abstract base class
│   ├── wavetable_generator.py # Generation pipeline
│   ├── processing.py         # Audio processing utilities
│   └── constants.py          # Mathematical constants
├── export/                   # WAV export functionality
│   └── wav.py               # File export logic
└── cli/                     # Command-line interface
    └── cli.py               # User-facing CLI

wavetable_generators/        # Generator implementations
├── example.py               # Template and working example
├── sine_to_triangle.py      # Production generators
└── square_pwm_tz.py

wavetable_tests/             # Comprehensive test suite
├── conftest.py              # Pytest fixtures
└── test_*.py                # Test modules
```

### Modern Python Features Used

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

**Abstract Base Classes (Interface Contracts)**

```python
from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    @abstractmethod
    def generate(self, theta, u) -> NDArray[np.float64]:
        """All generators must implement this."""
        ...
```

### Development Environment

**Virtual Environment (.venv)**

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows Git Bash)
source .venv/Scripts/activate

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install package in development mode
pip install -e .
```

**Development Tools**

-  `pytest` - Testing framework with fixtures and coverage
-  `pytest-cov` - Code coverage reporting (90% target)
-  `mypy` - Static type checking (strict mode)
-  `pylint` - Code quality linting (9.8+ score target)
-  `flake8` - Style guide enforcement (PEP 8)
-  `black` - Automatic code formatting (88 char line length)
-  `isort` - Import statement sorting

### Package Management

**pyproject.toml (Modern Python Packaging)**

```toml
[project]
name = "wavetable-synthesis"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "numpy>=2.0.0",
    "soundfile>=0.13.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    "mypy>=1.13.0",
    "pylint>=3.3.0",
    "flake8>=7.0.0",
    "black>=24.0.0",
]
```

**Editable Installation**

```bash
# Install in development mode (changes take effect immediately)
pip install -e .

# Install with development tools
pip install -e ".[dev]"
```

## Quality Standards

### Type Checking (mypy --strict)

**Zero type errors required**

```bash
mypy wavetable_synthesis/ --strict
```

Configuration in `pyproject.toml`:

-  `disallow_untyped_defs = true`
-  `disallow_incomplete_defs = true`
-  `warn_return_any = true`
-  Full type coverage on all functions

### Code Quality (pylint)

**9.8+ score target (currently 9.95)**

```bash
pylint wavetable_synthesis/ --fail-under=9.8
```

Configuration:

-  88 character line length (Black compatible)
-  NumPy extension support
-  Specific disabled checks for test files

### Code Style (flake8 + black)

**PEP 8 compliance with Black formatting**

```bash
# Check style
flake8 wavetable_synthesis/

# Auto-format
black wavetable_synthesis/
```

### Testing (pytest)

**90% coverage minimum (currently 90%)**

```bash
# Run tests with coverage
pytest wavetable_tests/ --cov=wavetable_synthesis --cov-report=term-missing

# Verbose output
pytest wavetable_tests/ -v

# Run specific test file
pytest wavetable_tests/test_wavetable_generation.py
```

Configuration in `pyproject.toml`:

-  Dynamic test fixtures
-  Coverage reporting
-  Test discovery patterns

## Python-Specific Patterns

### Decorator-Based Registry

Generators self-register using decorators:

```python
# In decorator_registry.py
_DECORATOR_REGISTRY: Dict[str, Any] = {}

def register_generator(name: str):
    def decorator(cls):
        _DECORATOR_REGISTRY[name] = cls()
        return cls
    return decorator

# Usage
@register_generator("my_wave")
class MyWaveGenerator(BaseGenerator):
    ...
```

### NumPy Vectorization

All audio operations use vectorized NumPy for performance:

```python
# Good: Vectorized (fast)
waveform = np.sin(theta) + 0.5 * np.sin(2 * theta)

# Bad: Loop-based (slow)
for i in range(len(theta)):
    waveform[i] = np.sin(theta[i])
```

### IEEE 754 Precision

All calculations use double precision internally:

```python
# Generate phase with float64 precision
t = np.arange(frame_size, dtype=np.float64) / frame_size
theta = TAU * t  # TAU = 2π

# Convert to float32 only for export
return table.flatten().astype(np.float32)
```

### Module Entry Point

Package can be run as a module:

```bash
python -m wavetable_synthesis sine_to_triangle
```

Implemented via `__main__.py`:

```python
from wavetable_synthesis.cli.cli import main

if __name__ == "__main__":
    main()
```

## Performance Characteristics

**Generation Speed**: 100+ Msamples/sec

**Memory Efficiency**: Float64 calculations with float32 export

**Optimization**: Pure NumPy vectorized operations with SIMD awareness

**Python Performance Notes**:

-  NumPy operations are C-speed (compiled)
-  Vectorized operations avoid Python interpreter overhead
-  Float64 internally provides IEEE 754 precision
-  Float32 export reduces file size without quality loss

## Common Commands

### Development Workflow

```bash
# Setup
python -m venv .venv
source .venv/Scripts/activate
pip install -e ".[dev]"

# Development
python -m wavetable_synthesis --list
python -m wavetable_synthesis sine_to_triangle

# Quality checks
pytest wavetable_tests/ --cov=wavetable_synthesis
mypy wavetable_synthesis/ --strict
pylint wavetable_synthesis/ --fail-under=9.8
black wavetable_synthesis/ --check
flake8 wavetable_synthesis/

# Auto-format
black wavetable_synthesis/
isort wavetable_synthesis/
```

### Package Installation

```bash
# User installation
pip install -e .

# Development installation
pip install -e ".[dev]"

# Web features (optional)
pip install -e ".[web]"

# Documentation tools (optional)
pip install -e ".[docs]"
```

## Benefits for This Project

1.  **Clear Code**: Python's readability makes mathematical algorithms easy to understand
2.  **Strong Types**: Type hints catch errors before runtime
3.  **Fast Computation**: NumPy provides C-speed performance
4.  **Rich Testing**: Pytest makes comprehensive testing simple
5.  **Professional Quality**: Tools ensure consistent, high-quality code
6.  **Educational Value**: Clean code helps users learn synthesis concepts

## Troubleshooting

**Import errors?**

```bash
# Ensure package is installed in development mode
pip install -e .
```

**Type errors?**

```bash
# Check with mypy
mypy wavetable_synthesis/ --strict
```

**Test failures?**

```bash
# Run tests with verbose output
pytest wavetable_tests/ -v --tb=short
```

**Virtual environment issues?**

```bash
# Recreate virtual environment
rm -rf .venv
python -m venv .venv
source .venv/Scripts/activate
pip install -e ".[dev]"
```

## Summary

Python is the foundation of this project, providing **clean, type-safe code** for mathematical audio synthesis. With modern features, excellent
libraries, and comprehensive tooling, Python enables both **professional wavetable generation** and **educational exploration** of synthesis concepts.
