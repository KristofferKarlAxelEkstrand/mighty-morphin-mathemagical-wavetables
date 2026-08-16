# 🎵 Mighty Morphin Mathemagical Wavetables

[![CI](https://github.com/KristofferKarlAxelEkstrand/mighty-morphin-mathemagical-wavetables/actions/workflows/ci.yml/badge.svg)](https://github.com/KristofferKarlAxelEkstrand/mighty-morphin-mathemagical-wavetables/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**Use math to create sound!**

Create wavetables for any synthesizer that supports wavetable loading — using mathematical formulas.

Generate clean, morphing waveforms for Serum, Vital, Pigments, and other wavetable synthesizers.

This open-source project exists for three main reasons:

- To provide a simple way to create expressive wavetables using mathematics.
- To help learners understand math concepts such as radians, π, sine, and cosine.
- To offer a small, approachable Python project that is suitable for first-time open-source contributors.

In spirit, it’s a bit like creating sounds with a Casio fx-82LB calculator and then loading them into a synthesizer to hear the result.

## 🎯 What Is This?

This tool creates **wavetables** - collections of waveforms that smoothly transform from one shape to another. Perfect for:

- 🎹 **Musicians**: Generate unique sounds for your synthesizers
- 📚 **Learners**: Understand sound synthesis through code
- 🔬 **Researchers**: Create mathematically-precise waveforms
- 🎨 **Sound Designers**: Experiment with custom wave shapes

**Key Features:**

- ✨ Mathematical precision (not sampled audio)
- 🔄 Smooth morphing between wave shapes
- 📦 Professional WAV export (16/24/32-bit)
- 🚀 Easy to create your own generators
- 🎓 Educational and well-documented

## ⚡ Quick Start

### Generate Your First Wavetable (30 Seconds)

```bash
# Generate a sine-to-triangle morphing wavetable
python -m wavetable_synthesis sine_to_triangle
```

**What you'll see:**

```text
Generating sine_to_triangle wavetable...
   Frames: 256, Rate: 44100Hz, Bits: 16
Success! File: maths_generated/sine_to_triangle_256frames_44100Hz_16bit.wav
```

Your wavetable is ready! Load it into any wavetable synthesizer.

---

### See What's Available

```bash
python -m wavetable_synthesis --list
```

**Output shows all generators:**

```text
Available Wavetable Generators:
========================================
  example              - Multi-harmonic example generator
  sine_to_triangle     - Morphs from sine to triangle wave
  square_pwm_tz        - Square wave with adjustable pulse width
```

---

### Try Different Generators

```bash
# Square wave with adjustable width
python -m wavetable_synthesis square_pwm_tz

# Multi-harmonic example
python -m wavetable_synthesis example
```

---

### Customize Settings

```bash
# Higher quality (more frames, higher sample rate, more bits)
python -m wavetable_synthesis sine_to_triangle --frames 512 --rate 96000 --bits 32

# Standard quality (smaller file size)
python -m wavetable_synthesis square_pwm_tz --frames 256 --rate 44100 --bits 16

# Save to specific folder
python -m wavetable_synthesis sine_to_triangle --output ./my_waves
```

---

---

### Batch Generate All Wavetables

```bash
# Generate all wavetables with multiple configurations
python -m wavetable_synthesis --batch
```

This creates wavetables for all generators in multiple quality settings.

---

## 🎨 Create Your Own Wavetable

Want to make your own wave shapes? It's simple!

### Step 1: Copy the Template

```bash
cp maths/example.py maths/my_wave.py
```

### Step 2: Edit Your Generator

Open `my_wave.py` and customize it:

```python
import numpy as np
from wavetable_synthesis.core.decorator_registry import register_generator
from wavetable_synthesis.core.base_generator import BaseGenerator

@register_generator("my_wave")  # Change this name
class MyWaveGenerator(BaseGenerator):
    name = "my_wave"
    description = "My custom waveform"

    def generate(self, theta, u):
        # theta = phase (0 to 2π)
        # u = morph parameter (0 to 1)

        # Your wave formula here - simple example:
        return np.sin(theta) * (1 - u) + np.sin(2 * theta) * u
```

### Step 3: Generate It

```bash
python -m wavetable_synthesis my_wave
```

**That's it!** Your generator is automatically discovered and ready to use.

**Learn more:** See [docs/wavetable_generators.md](docs/wavetable_generators.md) for detailed guide.

---

## 📋 Available Generators

- **sine_to_triangle** - Morphs from sine to triangle wave
- **square_pwm_tz** - Square wave with adjustable pulse width
- **example** - Multi-harmonic template you can customize

---

## ⚙️ Command Options

```bash
python -m wavetable_synthesis [generator] [options]

Options:
  --frames N     Number of morphing steps (default: 256)
  --rate N       Sample rate: 44100, 48000, 96000 (default: 44100)
  --bits N       Bit depth: 16, 24, 32 (default: 16)
  --output DIR   Where to save files (default: maths_generated)
  --list         Show all available generators
  --batch        Generate all wavetables with all configurations
```

**Examples:**

```bash
# High quality export
python -m wavetable_synthesis sine_to_triangle --frames 512 --rate 96000 --bits 32

# Batch generate everything
python -m wavetable_synthesis --batch
```

---

## 🔧 How It Works

1. **Generate phase array** - Create 2048 values from 0 to 2π for one waveform cycle
2. **Apply your formula** - Calculate waveform shape using `generate(theta, u)` method
3. **Process audio** - Remove DC offset, normalize volume for professional quality
4. **Repeat & morph** - Create 256 frames with smooth `u` transitions (0.0 → 1.0)
5. **Export WAV** - Save as professional WAV file for any synthesizer

---

## 📁 Project Structure

```text
wavetable-generator/
├── maths/                      # Your wave formulas (edit these)
│   ├── example.py             # Template + working generator
│   ├── sine_to_triangle.py    # Production generators
│   └── square_pwm_tz.py
├── generator/                  # Engine (usually don't edit)
│   ├── wavetable_synthesis/    # Core library
│   └── wavetable_tests/        # Test suite
├── docs/                      # Documentation & guides
│   └── tech/                  # Tooling notes
└── maths_generated/            # Generated WAV files (output)
```

---

## 🛠️ Installation & Setup

### Quick Setup (Recommended)

```bash
# Clone or download the repository
git clone <repository>
cd wavetable-generator

# Run the setup script (creates venv and installs everything)
bash setup.sh
```

The setup script:

- Creates a Python virtual environment (`.venv`)
- Installs the package in development mode
- Installs Node tools (`npm install`) so husky git hooks work

### Manual Setup (Alternative)

```bash
# Clone the repository
git clone <repository>
cd wavetable-generator

# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate          # Linux/macOS
# source .venv/Scripts/activate    # Windows Git Bash

# Install package in development mode
pip install -e .
```

### Development Setup (Optional)

Install extra tools for contributing:

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dev dependencies (pytest, ruff, mypy, etc.)
pip install -e ".[dev]"

# Install husky git hooks (needs Node 22+)
npm install

# Run tests to verify installation
pytest generator/wavetable_tests/
```

---

## 🚀 Modern Development

Fast, streamlined development tools:

### Quick Commands

```bash
make help          # Show all available commands
make test          # Run tests
make lint          # Check code quality with Ruff
make format        # Format code with Ruff
make quality       # Run all quality checks
```

### Ruff - Fast Linting & Formatting

[Ruff](https://docs.astral.sh/ruff/) - 10-100x faster than traditional tools:

```bash
ruff check --fix .    # Check and auto-fix issues
ruff format .         # Format code
```

### Git Hooks

`npm install` installs husky. Hooks run on `git commit`.

### Development Container

Open in VS Code or GitHub Codespaces for instant, pre-configured setup.

**Learn More:** [DEVELOPMENT.md](DEVELOPMENT.md)

---

## 📚 Learning Resources

**Getting Started:**

- [QUICKSTART.md](QUICKSTART.md) - Get running in 5 minutes
- [docs/wavetable_generators.md](docs/wavetable_generators.md) - Complete generator guide

**Understanding the Math:**

- [docs/radian-pi-phase-frequency.md](docs/radian-pi-phase-frequency.md) - Phase, frequency, and radians explained

**Development:**

- [DEVELOPMENT.md](DEVELOPMENT.md) - Development workflow
- [docs/development-setup.md](docs/development-setup.md) - Environment setup
- [docs/pathlib-guide.md](docs/pathlib-guide.md) - Modern path handling
- [docs/tech/husky.md](docs/tech/husky.md) - Git hooks
- [AGENTS.md](AGENTS.md) - For AI assistants and automated tools

---

## 🐛 Troubleshooting

### Virtual Environment Not Activating

**Windows Git Bash:**

```bash
source .venv/Scripts/activate
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**

```bash
source .venv/bin/activate
```

### Generator Not Found

Make sure your generator file is in the `maths/` directory and has the `@register_generator()` decorator.

### Import Errors

```bash
# Reinstall the package
pip install -e .
```

### WAV Files Not Playing

WAV files are raw audio - they need to be loaded into a wavetable synthesizer (Serum, Vital, Pigments, etc.) to hear them.

### Need More Help?

- Check the documentation in `docs/`
- Look at working examples in `maths/`
- Review test files in `generator/wavetable_tests/` for usage patterns

---

## 🎓 Key Concepts

**Wavetable:** A collection of single-cycle waveforms that smoothly morph from one to another

**Frame:** One single-cycle waveform (2048 samples) within the wavetable

**Theta (θ):** Phase array from 0 to 2π representing one complete waveform cycle

**U parameter:** Morphing control (0.0 to 1.0) that changes between frames

**Morphing:** Smooth transformation from one waveform shape to another

---

## 🚀 What's Next?

1. **Generate your first wavetable** - Try the quick start above
2. **Explore existing generators** - See what's possible
3. **Read the math guide** - Understand phase and frequency
4. **Create your own generator** - Start with `example.py`
5. **Share your creations** - Contribute back to the project!

---

Created by Kristoffer Ekstrand at [https://adventurekid.se/](https://adventurekid.se/).

Check out AKWF for more wavetables.

## 📄 License

This project is licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later).

You are free to use, modify, and distribute this software under the terms of the GPL-3.0 license.
See the [LICENSE](LICENSE) file for the full license text.

**Key Points:**

- ✅ Free to use, modify, and distribute
- ✅ Source code must remain open and available
- ✅ Derivative works must also be GPL-3.0 licensed
- ✅ No warranty provided

For more information about the GPL-3.0 license, visit: <https://www.gnu.org/licenses/gpl-3.0.html>

---

**Made with ❤️ for musicians, learners, and sound explorers**

Generate wavetables with mathematical precision!
