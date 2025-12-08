# Wavetable Generator Guide

**Complete guide to creating custom wavetable generators**

This guide teaches you how to create your own wavetable generators from scratch.
Whether you're new to audio programming or an experienced developer, you'll learn
everything you need to make professional wavetables.

---

## 📖 Table of Contents

### Getting Started (15 minutes)

- [What Are Wavetable Generators?](#what-are-wavetable-generators)
- [Quick Start: Your First Generator](#quick-start-your-first-generator)
- [Understanding the Two Key Parameters](#understanding-the-two-key-parameters)

### Core Concepts (20 minutes)

- [Theta (θ): The Phase Parameter](#theta-the-phase-parameter)
- [U: The Morph Parameter](#u-the-morph-parameter)
- [Common Wave Formulas](#common-wave-formulas)

### Practical Guide (30 minutes)

- [Step-by-Step Generator Creation](#step-by-step-generator-creation)
- [Testing Your Generator](#testing-your-generator)
- [Best Practices](#best-practices)

### Advanced Topics (optional)

- [Audio Theory Background](#audio-theory-background)
- [Error Handling](#error-handling-and-robustness)
- [Performance Optimization](#performance-considerations)
- [Advanced Features](#advanced-features)

### Reference

- [Code Examples](#examples-in-the-codebase)
- [Getting Help](#need-help)

---

## What Are Wavetable Generators?

**Simple answer:** Python classes that create audio waveforms using math formulas.

Wavetable generators produce "wavetables" - collections of waveforms that smoothly morph from one shape to another. When loaded into a synthesizer, these create evolving, dynamic sounds.

**Key features:**

- 📐 **Mathematical precision** - Not sampled audio, but calculated waveforms
- 🔄 **Smooth morphing** - Gradual transitions between different shapes
- 🎵 **Synthesizer-ready** - Works with Serum, Vital, Pigments, and more
- 🚀 **Automatic discovery** - Just write the code, it's instantly available

---

## Quick Start: Your First Generator

**Time: 5 minutes**

### Step 1: Copy the Template

```bash
cp wavetable_generators/example.py wavetable_generators/my_wave.py
```

### Step 2: Change Three Things

Open `my_wave.py` and update:

```python
# 1. Change the decorator name
@register_generator("my_wave")  # ← Your generator name

# 2. Change the class name
class MyWave(BaseGenerator):  # ← Your class name

# 3. Update get_info() return values
def get_info(self):
    return {
        "name": "my_wave",
        "description": "My custom waveform",
        "author": "Your Name",
        # ... other fields
    }
```

### Step 3: Write Your Wave Formula

Replace the `generate()` method with your math:

```python
def generate(self, theta, u):
    """Your waveform generator."""
    u = self._validate_u(u)  # Always validate u first

    # Simple example: morph from sine to double-frequency sine
    sine = np.sin(theta)
    double = np.sin(2 * theta)

    return sine * (1 - u) + double * u
```

### Step 4: Test It

```bash
python -m wavetable_synthesis my_wave
```

**Done!** Your generator is automatically discovered and creates a wavetable.

---

## Understanding the Two Key Parameters

Every generator uses two parameters: **theta** and **u**.

### Quick Summary

| Parameter | What It Is                     | Range      | Changes           |
| --------- | ------------------------------ | ---------- | ----------------- |
| **theta** | Phase (position in wave cycle) | 0 to 2π    | Within each frame |
| **u**     | Morph control                  | 0.0 to 1.0 | Between frames    |

**Simple analogy:**

- **Theta** = Where you are in the song (measure, beat, note)
- **U** = Which verse you're singing (verse 1 → chorus → verse 2)

---

## Theta: The Phase Parameter

**What is theta?** Your position in one complete wave cycle.

### Theta Basics

```python
# Theta is an array of 2048 values from 0 to 2π
# Example values:
theta[0] = 0.0      # Start of cycle
theta[512] ≈ 1.57   # Quarter way (π/2)
theta[1024] ≈ 3.14  # Halfway (π)
theta[2047] ≈ 6.28  # End of cycle (2π)
```

### Clock Face Analogy

Think of theta like a clock:

- **0 radians** = 12 o'clock (start)
- **π/2 radians** = 3 o'clock (quarter turn)
- **π radians** = 6 o'clock (halfway)
- **3π/2 radians** = 9 o'clock (three-quarters)
- **2π radians** = 12 o'clock again (full circle)

### Why Radians?

Radians are the natural unit for waves because:

- One complete circle = 2π radians (≈ 6.28)
- Sine and cosine functions expect radians
- Makes the math simpler and more precise

**Quick conversion:** 2π radians = 360 degrees

### Common Theta Patterns

```python
# Pure sine wave
return np.sin(theta)

# Octave higher (double frequency)
return np.sin(2 * theta)

# Octave lower (half frequency)
return np.sin(theta / 2)

# Phase shift (starts at different point)
return np.sin(theta + np.pi)

# Multiple harmonics
fundamental = np.sin(theta)
second_harmonic = np.sin(2 * theta)
third_harmonic = np.sin(3 * theta)
return fundamental + 0.5 * second_harmonic + 0.33 * third_harmonic
```

### Theta Key Takeaways

1. Theta tells you **where** in the wave cycle
2. Use theta as input to `np.sin()`, `np.cos()`, etc.
3. Multiply theta to change frequency (2×theta = octave up)
4. Don't worry about the math - start with examples!

---

## U: The Morph Parameter

**What is u?** A control that smoothly changes between wave shapes.

### U Basics

- **u = 0.0**: Starting waveform (first frame)
- **u = 0.5**: Halfway morphed (middle frame)
- **u = 1.0**: Ending waveform (last frame)

### How U Changes

For a 256-frame wavetable:

```text
Frame 0:   u = 0.000  ← Start shape
Frame 64:  u = 0.250
Frame 128: u = 0.500  ← Halfway
Frame 192: u = 0.750
Frame 255: u = 1.000  ← End shape
```

U stays constant within each frame but changes between frames.

### Using U Effectively

**Simple mixing:**

```python
wave_a = np.sin(theta)
wave_b = np.sin(3 * theta)
return wave_a * (1 - u) + wave_b * u
```

**Controlling harmonics:**

```python
fundamental = np.sin(theta)
harmonics = np.sin(2 * theta) + np.sin(3 * theta)
return fundamental + u * harmonics  # More harmonics as u increases
```

**Pulse width modulation:**

```python
threshold = (u * 2) - 1  # Maps 0-1 to -1 to +1
return np.sign(np.sin(theta) - threshold)
```

### U Key Takeaways

1. Use u to **control** waveform transformation
2. U changes **between** frames (not within)
3. Always validate: `u = self._validate_u(u)`
4. Think of u as a "morph slider" from shape A to shape B

---

## Common Wave Formulas

Copy these formulas directly into your `generate()` method:

### Basic Waveforms

```python
# Sine wave (pure tone)
return np.sin(theta)

# Sawtooth wave (bright, buzzy)
return 2 * (theta / (2 * np.pi) - 0.5)

# Square wave (hollow, clarinet-like)
return np.sign(np.sin(theta))

# Triangle wave (soft, flute-like)
return (2/np.pi) * np.arcsin(np.sin(theta))
```

### Morphing Examples

```python
# Sine to square morph
sine = np.sin(theta)
square = np.sign(np.sin(theta))
return sine * (1 - u) + square * u

# Harmonic growth
wave = np.sin(theta)
for n in range(2, int(2 + u * 5)):  # Add harmonics based on u
    wave += np.sin(n * theta) / n
return wave

# Frequency sweep
frequency = 1 + u * 3  # 1x to 4x frequency
return np.sin(theta * frequency)
```

### Harmonic Series

```python
# Sawtooth-like (all harmonics)
wave = np.zeros_like(theta)
for n in range(1, 8):
    wave += np.sin(n * theta) / n
return wave

# Square-like (odd harmonics only)
wave = np.zeros_like(theta)
for n in range(1, 8, 2):  # 1, 3, 5, 7...
    wave += np.sin(n * theta) / n
return wave

# Triangle-like (odd harmonics, 1/n² amplitude)
wave = np.zeros_like(theta)
for n in range(1, 8, 2):
    wave += np.sin(n * theta) / (n * n)
return wave
```

**Tip:** Start with these formulas, then modify them to create your own sounds!

---

## Step-by-Step Generator Creation

Let's create a complete generator together.

### Example: Pulse Width Modulation Generator

This creates a square wave with adjustable width (PWM effect).

**Step 1: Create the file**

```bash
cp wavetable_generators/example.py wavetable_generators/pwm.py
```

**Step 2: Update the code**

```python
import numpy as np
from numpy.typing import NDArray
from wavetable_synthesis.core.base_generator import BaseGenerator
from wavetable_synthesis.core.decorator_registry import register_generator

@register_generator("pwm")  # Name used in CLI
class PWMGenerator(BaseGenerator):
    """Pulse width modulation square wave generator."""

    def get_info(self):
        return {
            "name": "pwm",
            "id": "pwm",
            "description": "Pulse width modulation square wave",
            "author": "Your Name",
            "tags": ["square", "pwm", "bass"],
            "collections": ["synthesis"],
            "keywords": ["pulse", "width", "square"],
            "free": True,
        }

    def generate(self, theta: NDArray[np.float64], u: float) -> NDArray[np.float64]:
        """Generate PWM waveform.

        Args:
            theta: Phase from 0 to 2π
            u: Pulse width control (0 = thin pulse, 1 = wide pulse)
        """
        # Validate u
        u = self._validate_u(u)

        # Map u to threshold: 0.0 → -0.9, 1.0 → +0.9
        # This prevents the pulse from disappearing at extremes
        threshold = (u * 1.8) - 0.9

        # Create square wave with adjustable threshold
        return np.sign(np.sin(theta) - threshold).astype(np.float64)
```

**Step 3: Test it**

```bash
python -m wavetable_synthesis pwm
```

**Step 4: Verify**

```bash
# Check it appears in the list
python -m wavetable_synthesis --list

# Check the output file
ls wavetable_dist/pwm_*.wav
```

**Congratulations!** You've created a working wavetable generator.

---

## Testing Your Generator

**Important Concept**: U stays the same for an entire frame, but changes between frames.

Imagine your wavetable as a flipbook animation:

- Each page (frame) has a slightly different drawing
- Within each page, the drawing is consistent
- As you flip through pages, the drawing smoothly morphs

```python
# How u changes in a 4-frame wavetable:
# Frame 0: u = 0.0   (sine wave)
# Frame 1: u = 0.33  (mostly sine, some morphing)
# Frame 2: u = 0.67  (mostly morphed, some sine)
# Frame 3: u = 1.0   (fully morphed square wave)

# Within each frame, u is constant for all samples
```

### Why This Matters

When writing your `generate(theta, u)` method:

- Use `u` to control the overall shape of your waveform
- `u` affects the entire frame consistently
- Different frames get different `u` values for morphing

### Quick Test

```bash
# Generate wavetable
python -m wavetable_synthesis my_generator

# Check output
ls wavetable_dist/my_generator_*.wav
```

### Automated Tests

Create a test file in `wavetable_tests/`:

```python
import pytest
import numpy as np
from wavetable_generators.my_generator import MyGenerator

def test_my_generator_output():
    """Test generator produces valid output."""
    gen = MyGenerator()
    theta = np.linspace(0, 2*np.pi, 2048, endpoint=False)

    # Test at u=0
    output = gen.generate(theta, 0.0)
    assert output.shape == (2048,)
    assert np.all(np.isfinite(output))  # No NaN or inf
    assert np.abs(output).max() <= 1.0  # Within [-1, 1]

    # Test at u=1
    output = gen.generate(theta, 1.0)
    assert output.shape == (2048,)
    assert np.all(np.isfinite(output))
```

### Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest wavetable_tests/test_my_generator.py -v

# Check coverage
pytest --cov=wavetable_synthesis --cov-report=term
```

### Working with Generated Files

All export functions return `pathlib.Path` objects for easy file manipulation:

```python
from pathlib import Path
from wavetable_synthesis.export.wav import save_wavetable
import numpy as np

# Save wavetable - returns Path object
data = np.zeros(2048)
filepath = save_wavetable("test", data, output_dir="./my_waves")

# filepath is a Path object with useful methods!
print(filepath.name)          # 'test_1frames_44100Hz_16bit.wav'
print(filepath.stem)          # 'test_1frames_44100Hz_16bit'
print(filepath.suffix)        # '.wav'
print(filepath.parent)        # Path('my_waves')
print(filepath.exists())      # True
print(filepath.stat().st_size)  # File size in bytes

# Use Path operations
backup_path = filepath.with_suffix(".bak")
metadata_path = filepath.with_suffix(".json")

# Iterate over directory
for wav_file in filepath.parent.glob("*.wav"):
    print(f"Found: {wav_file.name}")
```

See [docs/pathlib-guide.md](pathlib-guide.md) for complete Path usage guide.

---

## Best Practices

### Code Quality

**Always validate u:**

```python
def generate(self, theta, u):
    u = self._validate_u(u)  # Uses BaseGenerator helper
    # ... rest of code
```

**Use type hints:**

```python
def generate(
    self,
    theta: NDArray[np.float64],
    u: float
) -> NDArray[np.float64]:
    # Clear types help catch errors
```

**Keep it simple:**

```python
# Good: Clear and direct
def generate(self, theta, u):
    u = self._validate_u(u)
    return np.sin(theta) * (1 - u) + np.sin(2 * theta) * u

# Avoid: Overly complex
def generate(self, theta, u):
    # 50 lines of complicated math that could be simpler
```

### Audio Quality

**Avoid DC offset:**

```python
# Bad: May have DC offset
return np.sign(np.sin(theta))

# Good: Remove DC offset
wave = np.sign(np.sin(theta))
return wave - np.mean(wave)
```

**Normalize amplitude:**

```python
# Ensure output is within [-1, 1]
wave = some_complex_calculation(theta, u)
max_val = np.abs(wave).max()
if max_val > 0:
    wave = wave / max_val
return wave
```

**Watch for clicks:**

```python
# Ensure smooth transitions in morphing
# Use gradual changes, not sudden jumps
threshold = u * 2 - 1  # Smooth: 0→-1, 1→+1
# Not: threshold = 1 if u > 0.5 else -1  # Sudden jump!
```

### Writing Good Documentation

**Write clear docstrings:**

```python
def generate(self, theta, u):
    """Generate waveform with pulse width modulation.

    Args:
        theta: Phase array from 0 to 2π
        u: Pulse width control (0=narrow, 1=wide)

    Returns:
        Waveform samples in range [-1, 1]
    """
```

**Update get_info():**

```python
def get_info(self):
    return {
        "name": "pwm",
        "description": "Pulse width modulation square wave",
        "author": "Your Name",
        "tags": ["square", "pwm", "bass"],  # Helps users find it
        "keywords": ["pulse", "width", "modulation"],
    }
```

---

## Audio Theory Background

### Frequency and Pitch

- **Frequency** = How many wave cycles per second (Hz)
- **Higher frequency** = Higher pitch
- **Double frequency** = One octave higher

```python
# Fundamental frequency
wave = np.sin(theta)

# Octave higher (2x frequency)
wave = np.sin(2 * theta)

# Fifth above (3x frequency)
wave = np.sin(3 * theta)
```

### Harmonics

Harmonics are integer multiples of the fundamental frequency:

- **1st harmonic** (fundamental): `np.sin(theta)`
- **2nd harmonic** (octave): `np.sin(2 * theta)`
- **3rd harmonic** (octave + fifth): `np.sin(3 * theta)`

More harmonics = brighter, richer sound:

```python
# Simple sine (one harmonic)
wave = np.sin(theta)

# Rich sawtooth (many harmonics)
wave = np.zeros_like(theta)
for n in range(1, 8):
    wave += np.sin(n * theta) / n
```

### Waveform Characteristics

| Waveform | Harmonics            | Sound Quality         |
| -------- | -------------------- | --------------------- |
| Sine     | None (pure tone)     | Smooth, flute-like    |
| Triangle | Odd harmonics (weak) | Soft, mellow          |
| Square   | Odd harmonics        | Hollow, clarinet-like |
| Sawtooth | All harmonics        | Bright, buzzy         |

### Phase and Amplitude

- **Phase** = Position in the cycle (theta)
- **Amplitude** = Height of the wave (volume)

```python
# Change amplitude (volume)
wave = 0.5 * np.sin(theta)  # Quieter

# Change phase (timing)
wave = np.sin(theta + np.pi)  # Inverted
```

---

## Advanced Features

### Wavetable Scanning

Wavetables work by scanning through frames with u:

```text
Note played → u value → Select frame → Play frame in loop
C3 (low)    → u=0.0   → Frame 0     → Simple waveform
C5 (mid)    → u=0.5   → Frame 128   → Morphed waveform
C7 (high)   → u=1.0   → Frame 255   → Complex waveform
```

Design your generator so **higher u values** create **brighter, richer** sounds.

### Performance Tips

**This is an offline generator** - wavetables are pre-rendered, not real-time.

**Infrastructure should be efficient**, but generators can prioritize clarity:

```python
# Fine for offline generation:
def generate(self, theta, u):
    wave = np.zeros_like(theta)
    for n in range(1, 8):
        wave += np.sin(n * theta) / n  # Clear loop
    return wave

# More efficient, but less clear:
def generate(self, theta, u):
    n = np.arange(1, 8).reshape(-1, 1)
    return np.sum(np.sin(n * theta) / n, axis=0)  # Vectorized
```

**Choose clarity first**, efficiency second (unless generating is very slow).

### Advanced Math Techniques

**Ring modulation:**

```python
carrier = np.sin(theta)
modulator = np.sin(theta * u * 10)  # Variable frequency
return carrier * modulator
```

**Frequency modulation:**

```python
modulator = np.sin(theta * u * 5)
carrier = np.sin(theta + modulator)
return carrier
```

**Phase distortion:**

```python
distorted_theta = theta + u * np.sin(theta * 2)
return np.sin(distorted_theta)
```

**Additive synthesis:**

```python
def generate(self, theta, u):
    wave = np.zeros_like(theta)

    # Define harmonic amplitudes
    harmonics = [
        (1, 1.0),      # Fundamental: full amplitude
        (2, 0.5 * u),  # 2nd harmonic grows with u
        (3, 0.3 * u),  # 3rd harmonic grows with u
        (4, 0.2 * u),  # 4th harmonic grows with u
    ]

    for n, amp in harmonics:
        wave += amp * np.sin(n * theta)

    return wave
```

---

## Error Handling and Robustness

### Common Edge Cases

```python
def generate(self, theta, u):
    # Validate u
    u = self._validate_u(u)

    # Handle empty theta
    if len(theta) == 0:
        return np.array([], dtype=np.float64)

    # Your generator code
    wave = np.sin(theta) * (1-u) + np.sin(2*theta) * u

    # Normalize to prevent clipping
    max_val = np.abs(wave).max()
    if max_val > 0:
        wave = wave / max_val

    return wave
```

### Watch Out For

- **NaN values**: From invalid math (0/0, sqrt(-1))
- **Infinite values**: From division by zero
- **DC offset**: Should average to ~0
- **Clipping**: Keep output in [-1, 1]

---

## Performance Considerations

### Use NumPy Vectorization

```python
# Good: Vectorized (fast)
wave = np.sin(theta) + 0.5 * np.sin(2*theta)

# Slow: Python loops
wave = np.zeros_like(theta)
for i in range(len(theta)):
    wave[i] = np.sin(theta[i]) + 0.5 * np.sin(2*theta[i])
```

### Pre-compute Constants

```python
class MyGenerator(BaseGenerator):
    def __init__(self):
        # Pre-compute expensive constants
        self.harmonic_weights = np.array([1.0, 0.5, 0.33, 0.25])

    def generate(self, theta, u):
        u = self._validate_u(u)
        wave = np.zeros_like(theta)

        for n, weight in enumerate(self.harmonic_weights, 1):
            wave += weight * np.sin(n * theta)

        return wave
```

---

## Quick Reference

### Quick Commands

```bash
# List all generators
python -m wavetable_synthesis --list

# Generate specific wavetable
python -m wavetable_synthesis generator_name

# Generate all wavetables
python -m wavetable_synthesis --batch

# Run tests
pytest

# Type check
mypy wavetable_synthesis/ --strict
```

### File Locations

```text
wavetable_generators/      ← Your generator goes here
├── example.py            ← Template to copy
├── sine_to_triangle.py   ← Working example
└── my_generator.py       ← Your new generator

wavetable_dist/           ← Generated WAV files
├── example_256f_2048s.wav
└── my_generator_256f_2048s.wav
```

### Common NumPy Functions

```python
# Trigonometric
np.sin(theta)      # Sine wave
np.cos(theta)      # Cosine wave
np.tan(theta)      # Tangent

# Utility
np.sign(x)         # Returns -1, 0, or 1
np.clip(x, min, max)  # Clamp to range
np.linspace(start, stop, num)  # Evenly spaced array

# Array operations
np.zeros_like(theta)  # Array of zeros
np.mean(array)        # Average
np.abs(array)         # Absolute values
np.max(array)         # Maximum
```

### Error Messages

**"Generator not found"**
→ Check `@register_generator("name")` decorator

**"Invalid u value"**
→ Use `u = self._validate_u(u)`

**"Output contains NaN"**
→ Check for division by zero

**"Output clipping"**
→ Normalize: `wave / np.abs(wave).max()`

---

## Examples in the Codebase

Look at working generators for inspiration:

- **`example.py`** - Template with 6 commented examples
- **`sine_to_triangle.py`** - Simple mathematical morph
- **`square_pwm_tz.py`** - PWM square wave generator

---

## Need Help?

### Documentation Links

- **README.md** - Project overview and setup
- **QUICKSTART.md** - 2-minute introduction
- **CONTRIBUTING.md** - How to contribute
- **docs/development-setup.md** - Development environment
- **docs/radian-pi-phase-frequency.md** - Math concepts

### Quick Debugging

**Generator not working?**

1. Does it appear in `--list`?
2. Does `generate()` return a NumPy array?
3. Are values within [-1, 1]?
4. Did you validate u?

**Sound not right?**

1. Check for DC offset: `wave - np.mean(wave)`
2. Normalize: `wave / np.abs(wave).max()`
3. Test at u=0, u=0.5, u=1.0
4. Listen to the WAV file

**Tests failing?**

1. Run `pytest -v` for details
2. Check virtual environment is active
3. Verify imports are correct
4. Ensure theta is in radians (0 to 2π)

---

## Summary

**To create a generator:**

1. Copy `example.py`
2. Change name, class, and `get_info()`
3. Write your wave formula in `generate()`
4. Test with `python -m wavetable_synthesis name`

**Remember:**

- Theta = position in wave (0 to 2π)
- U = morph control (0.0 to 1.0)
- Always validate u
- Keep output in [-1, 1]
- Simple is better than complex

**Start simple, experiment, have fun!** 🎵
