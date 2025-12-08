# ⚡ Quick Start Guide - Mighty Morphin Mathemagical Wavetables

**Get your first wavetable in under 2 minutes!**

---

## ✅ Prerequisites

- **Python 3.10 or newer** installed
- **Git** (for cloning the repository)
- **5 minutes** of your time

Check your Python version:

```bash
python --version
# Should show: Python 3.10.x or newer
```

---

## 📦 Step 1: Install (First Time Only)

### Option A: Quick Setup Script (Recommended)

```bash
# Clone the repository
git clone <repository>
cd mighty-morphin-mathemagical-wavetables

# Run the setup script (does everything automatically)
bash setup.sh
```

**What the script does:**

- ✅ Creates Python virtual environment
- ✅ Installs all dependencies
- ✅ Sets up the package

### Option B: Manual Setup

### Option B: Manual Installation

```bash
# Clone the repository
git clone <repository>
cd mighty-morphin-mathemagical-wavetables

# Create virtual environment
python -m venv .venv

# Activate it (Windows Git Bash)
source .venv/Scripts/activate

# Install package
pip install -e .
```

---

## 🎵 Step 2: Generate Your First Wavetable

```bash
# Make sure you're in the mighty-morphin-mathemagical-wavetables directory
cd mighty-morphin-mathemagical-wavetables

# Generate a sine-to-triangle morphing wavetable
python -m wavetable_synthesis sine_to_triangle
```

**You should see:**

```text
Generating sine_to_triangle wavetable...
   Frames: 256, Rate: 44100Hz, Bits: 16
Success! File: wavetable_dist/sine_to_triangle_256frames_44100Hz_16bit.wav
```

**Congratulations!** 🎉 You just created your first wavetable!

---

## 📂 Step 3: Find Your Wavetable

Your wavetable is saved here:

```text
mighty-morphin-mathemagical-wavetables/
└── wavetable_dist/
    └── sine_to_triangle_256frames_44100Hz_16bit.wav  ← Your file!
```

**Next steps:**

- Load this WAV file into any wavetable synthesizer (Serum, Vital, Pigments, etc.)
- Play with the wavetable position to hear it morph from sine to triangle
- Experiment with filters, effects, and modulation

---

## 🔍 Explore What's Available

See all the generators you can use:

```bash
python -m wavetable_synthesis --list
```

**Output:**

```text
Available Wavetable Generators:
========================================
  example              - Multi-harmonic example generator
  sine_to_triangle     - Morphs from sine to triangle wave
  square_pwm_tz        - Square wave with adjustable pulse width

Total: 3 generators
```

---

## 🎨 Try Different Generators

Each generator creates a different type of waveform:

```bash
# Square wave with pulse width modulation
python -m wavetable_synthesis square_pwm_tz

# Multi-harmonic example (great for learning)
python -m wavetable_synthesis example
```

---

## ⚙️ Customize Your Wavetables

### Quality Settings

```bash
# High quality (for mastering)
python -m wavetable_synthesis sine_to_triangle --frames 512 --rate 96000 --bits 32

# Standard quality (smaller files)
python -m wavetable_synthesis sine_to_triangle --frames 256 --rate 44100 --bits 16
```

**What these options mean:**

- `--frames`: Number of morphing steps (64, 128, 256, 512)
- `--rate`: Sample rate in Hz (44100, 48000, 96000)
- `--bits`: Bit depth (16, 24, 32)

### Custom Output Location

```bash
# Save to specific folder
python -m wavetable_synthesis sine_to_triangle --output ./my_sounds
```

### Batch Generate Everything

```bash
# Generate ALL wavetables with multiple configurations
python -m wavetable_synthesis --batch
```

**Warning:** This creates many files (100+) in various quality settings!

---

## 🚀 Create Your Own Generator

Ready to make your own waveforms? Follow these simple steps:

### Step 1: Copy the Template

```bash
# Create new generator file
cp wavetable_generators/example.py wavetable_generators/my_wave.py
```

### Step 2: Edit Your Generator

Open `wavetable_generators/my_wave.py` and customize:

```python
import numpy as np
from wavetable_synthesis.core.decorator_registry import register_generator
from wavetable_synthesis.core.base_generator import BaseGenerator

@register_generator("my_wave")  # Change this name
class MyWaveGenerator(BaseGenerator):
    name = "my_wave"  # Change this
    description = "My custom wave"  # Describe your wave

    def generate(self, theta, u):
        """Generate your waveform.

        Args:
            theta: Phase array (0 to 2π) - where in the cycle
            u: Morph parameter (0 to 1) - controls transformation

        Returns:
            Waveform as numpy array
        """
        # Simple morph example: sine → double frequency sine
        sine_wave = np.sin(theta)
        double_sine = np.sin(2 * theta)

        # Mix them based on u parameter
        return sine_wave * (1 - u) + double_sine * u
```

### Step 3: Test It

```bash
python -m wavetable_synthesis my_wave
```

**That's it!** Your generator is automatically discovered and works immediately.

---

## 🎓 Common Patterns

### Simple Waves

```python
# Pure sine wave
return np.sin(theta)

# Sawtooth wave
return 2 * (theta / (2 * np.pi) - 0.5)

# Square wave
return np.sign(np.sin(theta))
```

### Morphing Examples

```python
# Morph between two waveforms
wave1 = np.sin(theta)
wave2 = np.sin(3 * theta)
return wave1 * (1 - u) + wave2 * u

# Add harmonics based on u
return np.sin(theta) + u * np.sin(2 * theta)
```

---

## 🐛 Troubleshooting

### "Command not found: python"

Try `python3` instead of `python`:

```bash
python3 -m wavetable_synthesis sine_to_triangle
```

### "No module named 'wavetable_synthesis'"

Make sure you installed the package:

```bash
pip install -e .
```

### Virtual Environment Not Activated

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

- Check the file is in `wavetable_generators/` directory
- Make sure you have the `@register_generator("name")` decorator
- File name doesn't matter - decorator name does!

---

## 📚 Next Steps

**Learn More:**

- 📖 [README.md](README.md) - Complete project overview
- 🎯 [docs/wavetable_generators.md](docs/wavetable_generators.md) - Detailed generator guide
- 🔢 [docs/radian-pi-phase-frequency.md](docs/radian-pi-phase-frequency.md) - Understand the math

**Get Help:**

```bash
# Show all command options
python -m wavetable_synthesis --help

# List all available generators
python -m wavetable_synthesis --list
```

---

**Happy wavetable generation!** 🎵
