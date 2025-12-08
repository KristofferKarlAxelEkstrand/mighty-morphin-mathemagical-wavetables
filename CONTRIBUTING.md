# Contributing to Mighty Morphin Mathemagical Wavetables

Thank you for your interest in contributing! This project welcomes contributions from everyone, whether you're adding a new generator, fixing a bug, improving documentation, or suggesting new features.

## 🎯 Ways to Contribute

- **Create new wavetable generators** - Share your wave formulas
- **Improve documentation** - Make it clearer and more helpful
- **Fix bugs** - Help keep the code clean and working
- **Add tests** - Improve code coverage and reliability
- **Suggest features** - Tell us what would make this better

## 🚀 Quick Start for Contributors

### 1. Fork and Clone

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/mighty-morphin-mathemagical-wavetables.git
cd mighty-morphin-mathemagical-wavetables
```

### 2. Set Up Development Environment

```bash
# Run the setup script
bash setup.sh

# Or manually:
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
pip install -e ".[dev]"
```

### 3. Create a Branch

```bash
# Create a branch for your contribution
git checkout -b feature/my-new-generator
# or
git checkout -b fix/bug-description
```

### 4. Make Your Changes

Follow the guidelines below based on what you're contributing.

### 5. Test Your Changes

```bash
# Run all tests
pytest wavetable_tests/

# Run with coverage
pytest wavetable_tests/ --cov=wavetable_synthesis

# Check types
mypy wavetable_synthesis/ --strict

# Check code style
ruff check wavetable_synthesis/ wavetable_generators/

# Or use Make for all checks
make quality
```

### 6. Submit a Pull Request

- Push your branch to your fork
- Open a Pull Request on GitHub
- Describe your changes clearly
- Link any related issues

---

## 📝 Contributing Guidelines

### Code Style

We use modern, fast code quality tools:

- **Ruff** for linting and formatting
- **mypy** for type checking (strict mode)
- **pre-commit** for automated checks

**Format your code:**

```bash
# Format and fix issues with Ruff
ruff format wavetable_generators/ wavetable_synthesis/
ruff check --fix wavetable_generators/ wavetable_synthesis/

# Or use Make:
make format
```

**Why Ruff?**

- ⚡ 10-100x faster than traditional tools
- 🔧 Auto-fixes most issues
- 🎯 Replaces multiple tools in one
- 📦 Zero configuration needed

### Type Hints

All code must have complete type hints:

```python
def generate(
    self,
    theta: NDArray[np.float64],
    u: float,
) -> NDArray[np.float64]:
    """Generate waveform with type safety."""
    ...
```

### Documentation

- All public functions need docstrings
- Use clear, simple language
- Include examples where helpful
- Update relevant documentation files

---

## 🎨 Creating a New Generator

The easiest way to contribute! Here's how:

### Step 1: Create Your Generator File

```bash
cp wavetable_generators/example.py wavetable_generators/your_name.py
```

### Step 2: Implement Your Generator

```python
import numpy as np
from numpy.typing import NDArray

from wavetable_synthesis.core.base_generator import BaseGenerator
from wavetable_synthesis.core.decorator_registry import register_generator


@register_generator("your_name")
class YourGenerator(BaseGenerator):
    """One-line description of your waveform.

    More detailed description of what this generator does,
    what makes it unique, and how the morphing works.
    """

    def get_info(self) -> dict[str, Any]:
        """Get generator metadata."""
        return {
            "name": "your_name",
            "id": "your_name",
            "description": "Your waveform description",
            "author": "Your Name",
            "tags": ["category", "type"],
            "collections": ["collection_name"],
            "keywords": ["keyword1", "keyword2"],
            "free": True,
        }

    def generate(
        self,
        theta: NDArray[np.float64],
        u: float,
    ) -> NDArray[np.float64]:
        """Generate waveform.

        Args:
            theta: Phase array (0 to 2π) representing one complete cycle
            u: Morph parameter (0.0 to 1.0) controlling transformation

        Returns:
            Generated waveform as float64 array
        """
        # Validate u parameter
        u = self._validate_u(u)

        # Your wave generation logic here
        # Example: morph from sine to square
        sine_wave = np.sin(theta)
        square_wave = np.sign(np.sin(theta))

        return sine_wave * (1 - u) + square_wave * u
```

### Generator Requirements

- ✅ Must extend `BaseGenerator`
- ✅ Must use `@register_generator("unique_name")` decorator
- ✅ Must implement `generate(theta, u)` method
- ✅ Must return `NDArray[np.float64]`
- ✅ Should validate `u` parameter with `self._validate_u(u)`
- ✅ Should include comprehensive docstrings
- ✅ Should handle edge cases gracefully

### Best Practices for Generators

**DO:**

- Use vectorized NumPy operations
- Keep code readable and well-commented
- Validate input parameters
- Handle edge cases (u=0, u=1)
- Return normalized values (-1 to 1)
- Add helpful docstrings

**DON'T:**

- Use loops when vectorization is possible
- Return NaN or infinite values
- Assume u is always valid (validate it!)
- Leave magic numbers unexplained

### Step 3: Test Your Generator

```bash
# Generate a wavetable
python -m wavetable_synthesis your_name

# Verify it appears in the list
python -m wavetable_synthesis --list

# Run the test suite
pytest wavetable_tests/ -v
```

### Step 4: Add Tests (Optional but Appreciated)

Create tests in `wavetable_tests/`:

```python
def test_your_generator(generator_registry):
    """Test your new generator."""
    generator = generator_registry["your_name"]

    # Test basic generation
    theta = np.linspace(0, 2*np.pi, 2048, endpoint=False)
    result = generator.generate(theta, 0.5)

    # Verify output
    assert isinstance(result, np.ndarray)
    assert len(result) == len(theta)
    assert np.all(np.isfinite(result))
    assert np.max(np.abs(result)) <= 1.0

    # Test edge cases
    result_zero = generator.generate(theta, 0.0)
    result_one = generator.generate(theta, 1.0)

    assert np.all(np.isfinite(result_zero))
    assert np.all(np.isfinite(result_one))
```

---

## 🐛 Reporting Bugs

Found a bug? Please help us fix it!

### Before Reporting

- Check if the bug was already reported
- Try to reproduce it with the latest version
- Gather information about your setup

### Bug Report Template

**Description:**
Clear description of what the bug is.

**To Reproduce:**

1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:**
What you expected to happen.

**Actual Behavior:**
What actually happened.

**Environment:**

- OS: [e.g., Windows 11, macOS 14, Ubuntu 22.04]
- Python Version: [e.g., 3.10.5]
- Package Version: [e.g., 0.1.0]

**Additional Context:**
Any other relevant information.

---

## 💡 Suggesting Features

Have an idea? We'd love to hear it!

### Feature Request Template

**Problem:**
What problem does this feature solve?

**Proposed Solution:**
How would you like to see it implemented?

**Alternatives:**
Other approaches you've considered.

**Additional Context:**
Any other relevant information, examples, or mockups.

---

## 📖 Contributing Documentation

Documentation is just as important as code!

### What to Document

- New generators you create
- Complex concepts that need explanation
- Common problems and their solutions
- Usage examples and tutorials

### Documentation Style

- **Clear and simple** - No jargon unless necessary
- **Practical examples** - Show, don't just tell
- **Accurate** - Test all code examples
- **Well-structured** - Use headings and formatting

### Documentation Files

- `README.md` - Project overview
- `QUICKSTART.md` - Fast introduction
- `docs/wavetable_generators.md` - Generator creation guide
- `docs/radian-pi-phase-frequency.md` - Math concepts
- `PIP.MD` - Python package management

---

## 🧪 Testing Guidelines

### Writing Tests

- Use `pytest` framework
- Test both success and failure cases
- Test edge cases (empty inputs, extreme values)
- Use fixtures from `conftest.py`

### Coverage Goals

- Maintain at least 90% code coverage
- All new code should include tests
- Tests should be clear and maintainable

### Running Tests

```bash
# Run all tests
pytest wavetable_tests/

# Run with coverage report
pytest wavetable_tests/ --cov=wavetable_synthesis --cov-report=term-missing

# Run specific test file
pytest wavetable_tests/test_wavetable_generation.py

# Run with verbose output
pytest wavetable_tests/ -v
```

---

## 🔍 Code Review Process

### What We Look For

- ✅ Code follows style guidelines
- ✅ All tests pass
- ✅ Type hints are complete
- ✅ Documentation is updated
- ✅ Changes are well-explained
- ✅ No breaking changes (or clearly documented)

### Review Timeline

- We aim to review PRs within a few days
- Complex changes may take longer
- Be patient and responsive to feedback

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later), the same license as the project.

---

## 🤝 Code of Conduct

### Our Standards

- **Be respectful** - Treat everyone with kindness
- **Be constructive** - Focus on improving the project
- **Be collaborative** - Work together, help each other
- **Be patient** - Remember we're all learning

### Unacceptable Behavior

- Harassment or discrimination of any kind
- Trolling, insulting, or inflammatory comments
- Personal or political attacks
- Any other unprofessional conduct

### Enforcement

Project maintainers have the right to remove, edit, or reject comments, commits, code, issues, and other contributions that don't align with this Code of Conduct.

---

## 📞 Questions?

- **Documentation:** Check `docs/` folder
- **Examples:** Look at existing generators in `wavetable_generators/`
- **Issues:** Open an issue on GitHub
- **Discussion:** Start a discussion on GitHub

---

## 🎉 Recognition

Contributors will be recognized in:

- Project README
- Release notes
- Generator metadata (for generator authors)

Thank you for helping make this project better! Every contribution, no matter how small, is valuable.

---

**Happy Contributing! 🎵**
