# Understanding Radians, Pi, and Phase

**Simple guide to the math behind wavetable synthesis**

This guide explains the mathematical concepts you'll use when creating wavetables. Don't worry if math isn't your thing - we'll use simple analogies and practical examples.

---

## Quick Reference

Before diving in, here's what you need to know:

| Concept       | What It Means                 | Example                    |
| ------------- | ----------------------------- | -------------------------- |
| **Radian**    | Natural way to measure angles | 2π radians = full circle   |
| **Theta (θ)** | Your position in a wave cycle | 0 to 2π                    |
| **Phase**     | Where you are in the waveform | Like time on a clock       |
| **Frequency** | How fast the wave cycles      | 440 Hz = 440 cycles/second |

**Bottom line:** Radians make wave math simple. Use them and everything just works.

---

## What Are Radians?

**Simple answer:** A natural way to measure angles based on circles.

### Degrees vs Radians

You probably know degrees:

-  Full circle = 360°
-  Right angle = 90°
-  Half circle = 180°

Radians are similar, but use π (pi):

-  Full circle = 2π radians (about 6.28)
-  Right angle = π/2 radians (about 1.57)
-  Half circle = π radians (about 3.14)

### Quick Conversions

| Degrees | Radians     | What It Is         |
| ------- | ----------- | ------------------ |
| 0°      | 0           | Start              |
| 90°     | π/2 ≈ 1.57  | Quarter turn       |
| 180°    | π ≈ 3.14    | Half turn          |
| 270°    | 3π/2 ≈ 4.71 | Three-quarter turn |
| 360°    | 2π ≈ 6.28   | Full circle        |

### Why Use Radians?

**Radians make wave math simpler.** Here's why:

1.  **Sine and cosine work naturally with radians**
2.  **One full wave cycle = 2π radians** (no conversion needed)
3.  **All the formulas are cleaner**

```python
# With radians (simple)
wave = np.sin(theta)

# With degrees (needs conversion)
wave = np.sin(np.radians(theta))
```

**Rule of thumb:** If you're working with waves, use radians.

---

## The Clock Analogy

**Think of radians like a clock face** - it makes everything easier to visualize.

### Radian Clock

```text
        12:00 (π/2)
           │
           │
   9:00 ───┼─── 3:00
    (π)    │    (0)
           │
        6:00 (3π/2)
```

**Reading the clock:**

-  **3:00** = 0 radians (or 2π) - Start position
-  **12:00** = π/2 radians - Quarter way
-  **9:00** = π radians - Halfway
-  **6:00** = 3π/2 radians - Three-quarters
-  **3:00 again** = 2π radians - Full circle

### How Sine Waves Use the Clock

As you go around the clock, sine and cosine give you the waveform:

| Clock Position | Radians | sin(θ) | cos(θ) | Wave Height   |
| -------------- | ------- | ------ | ------ | ------------- |
| 3:00 (right)   | 0       | 0.0    | 1.0    | Zero          |
| 12:00 (top)    | π/2     | 1.0    | 0.0    | Peak          |
| 9:00 (left)    | π       | 0.0    | -1.0   | Zero again    |
| 6:00 (bottom)  | 3π/2    | -1.0   | 0.0    | Trough        |
| 3:00 (right)   | 2π      | 0.0    | 1.0    | Back to start |

**Key insight:** `sin(θ)` gives you the **height** of your wave at each position.

---

## What is Phase?

**Phase = your position in the wave cycle.**

### Simple Explanation

Think of phase like these familiar things:

**Like a song:**

-  Phase tells you **where you are** in the song
-  0 = beginning
-  π = middle
-  2π = end (back to beginning)

**Like a clock:**

-  Phase tells you **what time it is** in the cycle
-  Each wave cycle is like the hour hand going around once
-  Phase wraps around: after 2π, you're back to 0

**Like reading a book:**

-  Phase tells you **which page** you're on in the cycle
-  Each cycle is one chapter
-  When you finish (2π), the next cycle starts at page 1 (0)

### Phase in Your Generator

When you write a generator, `theta` is your phase array:

```python
def generate(self, theta, u):
    # theta = [0, 0.003, 0.006, 0.009, ..., 6.28]
    # These are phase values from 0 to 2π

    # At each phase, calculate the wave height
    return np.sin(theta)
```

**What theta contains:**

-  2048 numbers from 0 to just under 2π
-  Each number is a position in your wave cycle
-  Evenly spaced (like frames in a flipbook)

---

## Understanding Pi (π)

**π is just a number: approximately 3.14159**

### Why π Appears Everywhere

π shows up in circles (and waves are circular):

-  **Circumference of circle** = 2πr
-  **Full wave cycle** = 2π radians
-  **Half a cycle** = π radians

### Common π Values You'll Use

| Expression | Value   | What It Means     |
| ---------- | ------- | ----------------- |
| π/4        | ≈ 0.785 | Eighth of a cycle |
| π/2        | ≈ 1.571 | Quarter cycle     |
| π          | ≈ 3.142 | Half cycle        |
| 3π/2       | ≈ 4.712 | Three-quarters    |
| 2π         | ≈ 6.283 | Full cycle        |

### Using π in Code

```python
import numpy as np

# NumPy provides π as np.pi
full_cycle = 2 * np.pi  # ≈ 6.283

# Common wave operations
sine = np.sin(theta)
shifted = np.sin(theta + np.pi)  # 180° phase shift
octave_up = np.sin(2 * theta)    # Double frequency
```

---

## Frequency Explained Simply

**Frequency = how many times the wave repeats per second.**

### The Basics

-  **1 Hz** = 1 cycle per second
-  **440 Hz** = 440 cycles per second (musical A note)
-  **44,100 Hz** = sample rate (how many samples per second)

### Frequency in Wavetables

Your wavetable defines **one cycle**. The synthesizer plays it at different speeds:

```text
Low note (110 Hz)  → Plays your cycle 110 times/second
Mid note (440 Hz)  → Plays your cycle 440 times/second
High note (880 Hz) → Plays your cycle 880 times/second
```

### Harmonics and Frequency

Harmonics are integer multiples of the base frequency:

```python
fundamental = np.sin(theta)      # Base frequency (1x)
octave = np.sin(2 * theta)       # Double frequency (2x)
fifth_above = np.sin(3 * theta)  # Triple frequency (3x)

# More harmonics = brighter sound
bright_wave = fundamental + 0.5 * octave + 0.33 * fifth_above
```

**Key insight:** Multiply theta by a number to change frequency.

---

## Practical Examples

### Example 1: Simple Sine Wave

```python
import numpy as np

def generate(self, theta, u):
    """Generate a pure sine wave."""
    # theta goes from 0 to 2π
    # sin(theta) gives us the wave height at each position
    return np.sin(theta)
```

### Example 2: Octave Higher

```python
def generate(self, theta, u):
    """Generate a sine wave one octave higher."""
    # Multiply theta by 2 = double the frequency
    return np.sin(2 * theta)
```

### Example 3: Phase Shift

```python
def generate(self, theta, u):
    """Generate a phase-shifted sine wave."""
    # Add π to shift by 180 degrees (inverts the wave)
    return np.sin(theta + np.pi)
```

### Example 4: Morphing Waves

```python
def generate(self, theta, u):
    """Morph from sine to triple-frequency sine."""
    # u controls the mix: 0 = sine, 1 = triple frequency
    sine = np.sin(theta)
    triple = np.sin(3 * theta)
    return sine * (1 - u) + triple * u
```

### Example 5: Harmonic Series

```python
def generate(self, theta, u):
    """Build a wave from multiple harmonics."""
    wave = np.sin(theta)  # Fundamental

    # Add harmonics (makes it brighter)
    wave += 0.5 * np.sin(2 * theta)  # Octave
    wave += 0.33 * np.sin(3 * theta)  # Fifth
    wave += 0.25 * np.sin(4 * theta)  # Two octaves

    return wave
```

---

## Common Patterns

### Pattern: Frequency Multiplication

```python
# Original frequency
np.sin(theta)

# Double (octave up)
np.sin(2 * theta)

# Triple (octave + fifth)
np.sin(3 * theta)

# Half (octave down)
np.sin(theta / 2)
```

### Pattern: Phase Shifting

```python
# Original
np.sin(theta)

# Shift by 90° (same as cosine)
np.sin(theta + np.pi/2)

# Shift by 180° (inverted)
np.sin(theta + np.pi)

# Shift by 270°
np.sin(theta + 3*np.pi/2)
```

### Pattern: Harmonic Mixing

```python
# Simple (one harmonic)
wave = np.sin(theta)

# Rich (multiple harmonics)
wave = (np.sin(theta) +
        0.5 * np.sin(2 * theta) +
        0.33 * np.sin(3 * theta))
```

---

## Common Mistakes

### Mistake 1: Using Degrees

```python
# Wrong! np.sin() expects radians
wrong = np.sin(180)  # This is NOT 180 degrees!

# Right: use π for half circle
right = np.sin(np.pi)  # This equals 0
```

### Mistake 2: Forgetting 2π

```python
# Wrong: using 360 instead of 2π
wrong_cycle = 360

# Right: full cycle is 2π radians
right_cycle = 2 * np.pi  # ≈ 6.28
```

### Mistake 3: Confusing Phase and Frequency

```python
# Phase = WHERE you are in the cycle
phase = theta  # Array of positions [0 to 2π]

# Frequency = HOW FAST you move through cycles
frequency_multiplier = 2  # Makes wave go 2x faster
return np.sin(frequency_multiplier * theta)
```

---

## Essential Formulas

### Essential Conversions

| From                        | To    | Formula                       |
| --------------------------- | ----- | ----------------------------- |
| Degrees → Radians           | Any   | `radians = degrees * π / 180` |
| Radians → Degrees           | Any   | `degrees = radians * 180 / π` |
| Frequency → Phase increment | Audio | `2 * π * freq / sample_rate`  |

### Common Values

| Description    | Radians | Approx |
| -------------- | ------- | ------ |
| No rotation    | 0       | 0      |
| Quarter turn   | π/2     | 1.57   |
| Half turn      | π       | 3.14   |
| Three-quarters | 3π/2    | 4.71   |
| Full turn      | 2π      | 6.28   |

### Wave Formulas

| Wave Type | Formula             | Harmonics       |
| --------- | ------------------- | --------------- |
| Sine      | `np.sin(theta)`     | 1 (fundamental) |
| Octave up | `np.sin(2 * theta)` | 2nd harmonic    |
| Fifth up  | `np.sin(3 * theta)` | 3rd harmonic    |
| Complex   | Sum of harmonics    | Multiple        |

---

## Summary

**Key Takeaways:**

1.  **Radians are natural for waves** - Use them, not degrees
2.  **2π = one full cycle** - Goes from 0 to 2π and wraps
3.  **Theta = position in cycle** - Array from 0 to 2π
4.  **Phase = where you are** - Like time on a clock
5.  **Frequency = how fast** - Multiply theta to change speed
6.  **π is just a number** - About 3.14, makes circles work

**For Wavetable Generators:**

-  `theta` is your phase array (0 to 2π)
-  Use `np.sin(theta)` to get wave height
-  Multiply theta to change frequency
-  Add to theta to shift phase
-  Mix waves using `u` parameter

**Start simple:** Copy a working example and experiment. The math will make sense as you use it!

---

## Need More Help?

-  **Try the examples** - Copy and run them to see what happens
-  **Experiment** - Change numbers and listen to the results
-  **Ask questions** - Math is easier when you're making sounds
-  **Read other docs** - Check `wavetable_generators.md` for more examples

Remember: **You don't need to master all the math to create great wavetables.** Start with the examples and build from there!
