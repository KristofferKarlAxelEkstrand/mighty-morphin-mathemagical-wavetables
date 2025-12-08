# 📁 Project Structure Guide

This document explains the organization of the Wavetable Generator project - where everything goes and why.

## 📂 Directory Overview

```text
wavetable-generator/
├── wavetable_generators/       # ← Your generators go here!
├── wavetable_synthesis/        # Core library (don't edit)
├── wavetable_tests/           # Test suite
├── wavetable_dist/            # Generated WAV files (output)
├── docs/                      # Documentation
├── docs_tech/                 # Technical documentation
├── .venv/                     # Virtual environment (created by setup)
└── [config files]             # Project configuration
```

## 🎨 wavetable_generators/ - Your Workspace

**This is where you create generators!**

```text
wavetable_generators/
├── __init__.py               # Makes this a Python package
├── example.py                # Template + working generator ← Start here!
├── sine_to_triangle.py       # Production example
├── square_pwm_tz.py          # Another production example
└── your_generator.py         # ← Your new generators go here!
```

**What belongs here:**

- ✅ All custom wavetable generators
- ✅ Your experimental generators
- ✅ Production-ready generators

**How it works:**

- Each file contains one generator class
- Use `@register_generator("name")` decorator
- Generators are automatically discovered
- File name doesn't matter - decorator name does!

**Example:**

```python
# File: wavetable_generators/my_wave.py

from wavetable_synthesis.core.decorator_registry import register_generator
from wavetable_synthesis.core.base_generator import BaseGenerator

@register_generator("my_wave")  # This name is what you use in CLI
class MyWaveGenerator(BaseGenerator):
    def generate(self, theta, u):
        return np.sin(theta)  # Your formula here
```

Then use it:

```bash
python -m wavetable_synthesis my_wave
```

---

## ⚙️ wavetable_synthesis/ - Core Library

**This is the engine - usually you don't edit these files**

```text
wavetable_synthesis/
├── __init__.py               # Package initialization
├── __main__.py               # Makes package runnable as module
├── py.typed                  # Marks package as type-hinted
│
├── core/                     # Generation engine
│   ├── __init__.py
│   ├── base_generator.py     # BaseGenerator class ← Extend this!
│   ├── decorator_registry.py # Auto-discovery system
│   ├── wavetable_generator.py # Main generation logic
│   ├── processing.py         # Audio processing (normalize, DC remove)
│   ├── constants.py          # Mathematical constants (TAU, etc.)
│   ├── config.py             # Configuration settings
│   └── registry.py           # Generator registry management
│
├── export/                   # WAV file export
│   ├── __init__.py
│   └── wav.py                # WAV file writing
│
└── cli/                      # Command-line interface
    ├── __init__.py
    ├── cli.py                # Main CLI logic
    └── test_cli.py           # CLI tests
```

**When to edit core files:**

- Adding new processing features
- Extending BaseGenerator functionality
- Adding new export formats
- Improving CLI features

**Most users never need to edit these files!**

---

## 🧪 wavetable_tests/ - Test Suite

```text
wavetable_tests/
├── conftest.py                    # Pytest fixtures and configuration
├── test_wavetable_generation.py   # Core generation tests
├── test_integration.py            # Integration tests
└── test_advanced.py               # Advanced feature tests
```

**What belongs here:**

- ✅ Unit tests for core functionality
- ✅ Integration tests
- ✅ Generator-specific tests
- ✅ Regression tests for bugs

**Running tests:**

```bash
# Run all tests
pytest wavetable_tests/

# Run with coverage
pytest wavetable_tests/ --cov=wavetable_synthesis

# Run specific test file
pytest wavetable_tests/test_wavetable_generation.py
```

**Adding tests for your generator:**

```python
# In wavetable_tests/test_wavetable_generation.py

def test_my_generator(generator_registry):
    """Test my new generator."""
    generator = generator_registry["my_wave"]

    theta = np.linspace(0, 2*np.pi, 2048, endpoint=False)
    result = generator.generate(theta, 0.5)

    assert isinstance(result, np.ndarray)
    assert len(result) == len(theta)
    assert np.all(np.isfinite(result))
```

---

## 📦 wavetable_dist/ - Output Directory

```text
wavetable_dist/
├── sine_to_triangle_256frames_44100Hz_16bit.wav
├── square_pwm_tz_256frames_44100Hz_16bit.wav
└── [your generated wavetables].wav
```

**What belongs here:**

- ✅ Generated WAV files (output)
- ✅ Automatically created by the generator

**Naming convention:**

```text
{generator_name}_{frames}frames_{sample_rate}Hz_{bit_depth}bit.wav
```

**This directory:**

- Created automatically when you generate wavetables
- Can be changed with `--output` flag
- Should be in `.gitignore` (output files don't belong in git)

---

## 📚 docs/ - User Documentation

```text
docs/
├── wavetable_generators.md         # Complete generator guide
├── radian-pi-phase-frequency.md    # Math concepts explained
└── development-setup.md            # Dev environment setup
```

**What belongs here:**

- ✅ User-facing documentation
- ✅ Tutorials and guides
- ✅ Educational content
- ✅ Examples and walkthroughs

**Documentation style:**

- Clear and simple language
- Practical examples
- Educational focus
- Well-organized

---

## 🔧 docs_tech/ - Technical Documentation

```text
docs_tech/
├── python.md      # Python language and tools
└── husky.md       # Git hooks automation
```

**What belongs here:**

- ✅ Tool documentation
- ✅ Technical reference material
- ✅ Development tooling guides

---

## 📋 Root Directory Files

### Documentation

- `README.md` - Project overview and quick start
- `QUICKSTART.md` - Fast introduction (5 minutes)
- `CONTRIBUTING.md` - Contribution guidelines
- `CHANGELOG.md` - Version history
- `AGENTS.md` - For AI assistants and tools
- `PIP.MD` - Python package management reference

### Configuration

- `pyproject.toml` - Python project configuration (dependencies, tools)
- `package.json` - Node.js dependencies (for Prettier, husky)
- `package-lock.json` - Locked Node.js dependencies

### Scripts

- `setup.sh` - Quick setup script for first-time users
- `auto_activate.sh` - Auto-activation script for virtual environment

### IDE Configuration

- `.vscode/` - VS Code settings and tasks
- `.editorconfig` - Editor configuration
- `wavetable-generator.code-workspace` - VS Code workspace

### Git Configuration

- `.gitignore` - Files to ignore in git
- `.husky/` - Git hook scripts

### Python Configuration

- `.venv/` - Virtual environment (created by setup, not in git)
- `wavetable_synthesis.egg-info/` - Package metadata (created by pip)

---

## 🎯 Where Does My Code Go?

### Creating a New Generator

**Location:** `wavetable_generators/your_name.py`

```python
# wavetable_generators/my_cool_wave.py
from wavetable_synthesis.core.decorator_registry import register_generator
from wavetable_synthesis.core.base_generator import BaseGenerator

@register_generator("my_cool_wave")
class MyCoolWaveGenerator(BaseGenerator):
    def generate(self, theta, u):
        return np.sin(theta) * (1 - u) + np.sin(3 * theta) * u
```

### Adding Tests

**Location:** `wavetable_tests/test_wavetable_generation.py` (or new file)

```python
# Add to existing test file or create new one
def test_my_cool_wave(generator_registry):
    generator = generator_registry["my_cool_wave"]
    # ... test code ...
```

### Adding Documentation

**For users:** `docs/your_guide.md`

**For developers:** `docs_tech/your_tech_doc.md`

**For general info:** Update `README.md` or create root-level `.md` file

---

## 🚫 What NOT to Put in Git

These are automatically generated or machine-specific:

```text
.venv/                    # Virtual environment
__pycache__/              # Python bytecode
*.pyc                     # Python compiled files
wavetable_dist/           # Generated WAV files
*.egg-info/               # Package metadata
htmlcov/                  # Coverage reports
.coverage                 # Coverage data
.pytest_cache/            # Pytest cache
node_modules/             # Node.js dependencies
```

Check `.gitignore` for complete list.

---

## 🔍 Finding Things

### "Where is the generator registry?"

`wavetable_synthesis/core/decorator_registry.py`

### "Where is the WAV export code?"

`wavetable_synthesis/export/wav.py`

### "Where are the mathematical constants?"

`wavetable_synthesis/core/constants.py`

### "Where is the CLI code?"

`wavetable_synthesis/cli/cli.py`

### "Where should my new generator go?"

`wavetable_generators/your_generator_name.py`

### "Where can I find generator examples?"

- `wavetable_generators/example.py` - Template
- `wavetable_generators/sine_to_triangle.py` - Production example
- `wavetable_generators/square_pwm_tz.py` - Another example

---

## 📖 Project Navigation Tips

### For New Contributors

1. **Start with:** `wavetable_generators/example.py`
2. **Read:** `README.md` and `QUICKSTART.md`
3. **Study:** Existing generators in `wavetable_generators/`
4. **Create:** Your generator in `wavetable_generators/`

### For Documentation Writers

1. **User docs:** `docs/` directory
2. **Technical docs:** `docs_tech/` directory
3. **General info:** Root `.md` files

### For Core Contributors

1. **Core engine:** `wavetable_synthesis/core/`
2. **Export:** `wavetable_synthesis/export/`
3. **CLI:** `wavetable_synthesis/cli/`
4. **Tests:** `wavetable_tests/`

---

## 🎓 Understanding the Architecture

### Data Flow

```text
1. User runs CLI command
   ↓
2. CLI (cli/cli.py) parses arguments
   ↓
3. Registry (core/registry.py) finds generator
   ↓
4. Generator (wavetable_generators/*.py) creates waveforms
   ↓
5. Processing (core/processing.py) cleans audio
   ↓
6. Export (export/wav.py) saves WAV file
   ↓
7. WAV file in wavetable_dist/
```

### Generator Discovery

```text
1. Python imports wavetable_generators/
   ↓
2. @register_generator decorator runs
   ↓
3. Generator added to registry automatically
   ↓
4. CLI can use it immediately
```

---

## ✅ Best Practices

### File Organization

- **One generator per file** - Keeps things simple
- **Clear file names** - Describe the waveform
- **Consistent style** - Follow existing patterns

### Naming Conventions

- **Generators:** lowercase_with_underscores
- **Classes:** PascalCase
- **Functions:** lowercase_with_underscores
- **Constants:** UPPERCASE_WITH_UNDERSCORES

### Code Location

- **Generators:** `wavetable_generators/`
- **Core logic:** `wavetable_synthesis/core/`
- **Tests:** `wavetable_tests/`
- **Docs:** `docs/` or `docs_tech/`

---

**Need help navigating the project? Check the README or CONTRIBUTING guide!**
