# 📁 Project Structure Guide

This document explains the organization of the Wavetable Generator project - where everything goes and why.

## 📂 Directory Overview

```text
wavetable-generator/
├── maths/       # ← Your generators go here!
├── generator/                  # Engine (usually don't edit)
│   ├── wavetable_synthesis/    # Core library
│   └── wavetable_tests/        # Test suite
├── maths_generated/            # Generated WAV files (output)
├── docs/                      # Documentation
│   └── tech/                  # Tooling notes
├── .venv/                     # Virtual environment (created by setup)
└── [config files]             # Project configuration
```

## 🎨 maths/ - Your Workspace

**This is where you create generators!**

```text
maths/
├── README.md                 # Copy the template, edit the formula
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
# File: maths/my_wave.py

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

## ⚙️ generator/ - Engine

**This is the engine - usually you don't edit these files**

The import name is still `wavetable_synthesis`. The tests live next to the library.

```text
generator/
└── wavetable_synthesis/
    ├── __init__.py               # Package initialization
    ├── __main__.py               # Makes package runnable as module
    ├── py.typed                  # Marks package as type-hinted
    ├── core/                     # Generation engine
    │   ├── __init__.py
    │   ├── base_generator.py     # BaseGenerator class ← Extend this!
    │   ├── decorator_registry.py # Auto-discovery system
    │   ├── wavetable_generator.py # Main generation logic
    │   ├── processing.py         # Audio processing (normalize, DC remove)
    │   ├── constants.py          # Mathematical constants (TAU, etc.)
    │   ├── config.py             # Configuration settings
    │   └── registry.py           # Generator registry management
    ├── export/                   # WAV file export
    │   ├── __init__.py
    │   └── wav.py                # WAV file writing
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

## 🧪 generator/wavetable_tests/ - Test Suite

```text
generator/wavetable_tests/
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
pytest generator/wavetable_tests/

# Run with coverage
pytest generator/wavetable_tests/ --cov=wavetable_synthesis

# Run specific test file
pytest generator/wavetable_tests/test_wavetable_generation.py
```

**Adding tests for your generator:**

```python
# In generator/wavetable_tests/test_wavetable_generation.py

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

## 📦 maths_generated/ - Output Directory

```text
maths_generated/
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
├── development-setup.md            # Dev environment setup
└── tech/                           # Tooling notes
    └── husky.md
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

## 🔧 docs/tech/ - Technical Documentation

```text
docs/tech/
└── husky.md       # Git hooks (husky + lint-staged)
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

### Configuration

- `pyproject.toml` - Python project configuration (dependencies, tools)
- `package.json` - Node tools (husky, Prettier, office-space)
- `package-lock.json` - Locked Node.js dependencies

### Scripts

- `setup.sh` - Quick setup script for first-time users

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

**Location:** `maths/your_name.py`

```python
# maths/my_cool_wave.py
from wavetable_synthesis.core.decorator_registry import register_generator
from wavetable_synthesis.core.base_generator import BaseGenerator

@register_generator("my_cool_wave")
class MyCoolWaveGenerator(BaseGenerator):
    def generate(self, theta, u):
        return np.sin(theta) * (1 - u) + np.sin(3 * theta) * u
```

### Adding Tests

**Location:** `generator/wavetable_tests/test_wavetable_generation.py` (or new file)

```python
# Add to existing test file or create new one
def test_my_cool_wave(generator_registry):
    generator = generator_registry["my_cool_wave"]
    # ... test code ...
```

### Adding Documentation

**For users:** `docs/your_guide.md`

**For developers:** `docs/tech/your_tech_doc.md`

**For general info:** Update `README.md` or create root-level `.md` file

---

## 🚫 What NOT to Put in Git

These are automatically generated or machine-specific:

```text
.venv/                    # Virtual environment
__pycache__/              # Python bytecode
*.pyc                     # Python compiled files
maths_generated/           # Generated WAV files
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

`generator/wavetable_synthesis/core/decorator_registry.py`

### "Where is the WAV export code?"

`generator/wavetable_synthesis/export/wav.py`

### "Where are the mathematical constants?"

`generator/wavetable_synthesis/core/constants.py`

### "Where is the CLI code?"

`generator/wavetable_synthesis/cli/cli.py`

### "Where should my new generator go?"

`maths/your_generator_name.py`

### "Where can I find generator examples?"

- `maths/example.py` - Template
- `maths/sine_to_triangle.py` - Production example
- `maths/square_pwm_tz.py` - Another example

---

## 📖 Project Navigation Tips

### For New Contributors

1. **Start with:** `maths/example.py`
2. **Read:** `README.md` and `QUICKSTART.md`
3. **Study:** Existing generators in `maths/`
4. **Create:** Your generator in `maths/`

### For Documentation Writers

1. **User docs:** `docs/` directory
2. **Technical docs:** `docs/tech/` directory
3. **General info:** Root `.md` files

### For Core Contributors

1. **Core engine:** `generator/wavetable_synthesis/core/`
2. **Export:** `generator/wavetable_synthesis/export/`
3. **CLI:** `generator/wavetable_synthesis/cli/`
4. **Tests:** `generator/wavetable_tests/`

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
4. Generator (maths/*.py) creates waveforms
   ↓
5. Processing (core/processing.py) cleans audio
   ↓
6. Export (export/wav.py) saves WAV file
   ↓
7. WAV file in maths_generated/
```

### Generator Discovery

```text
1. The engine loads each file in maths/
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

- **Generators:** `maths/`
- **Core logic:** `generator/wavetable_synthesis/core/`
- **Tests:** `generator/wavetable_tests/`
- **Docs:** `docs/` or `docs/tech/`

---

**Need help navigating the project? Check the README or CONTRIBUTING guide!**
