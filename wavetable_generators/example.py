"""
Example Wavetable Generator - Your Template for Creating New Generators

This file serves two purposes:
1. Working example generator that creates multi-harmonic wavetables
2. Template you can copy and modify to create your own generators

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK START: CREATE YOUR OWN GENERATOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Copy this file
   cp wavetable_generators/example.py wavetable_generators/my_wave.py

Step 2: Change three things in your new file
   - @register_generator("example")  → @register_generator("my_wave")
   - class Example                   → class MyWave
   - get_info() return values        → your generator info

Step 3: Write your wave formula
   - Edit the generate() method
   - Replace the example code with your math

Step 4: Test it
   python -m wavetable_synthesis my_wave

That's it! Your generator is automatically discovered and ready to use.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT THIS EXAMPLE DOES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Morphs smoothly between a pure sine wave and a sawtooth wave using the u parameter.
This demonstrates basic waveform morphing and linear interpolation techniques.

- u = 0.0: Pure sine wave (smooth, fundamental frequency only)
- u = 0.5: Mix of sine and sawtooth waves
- u = 1.0: Pure sawtooth wave (bright, rich harmonics)
"""

from typing import Any

import numpy as np
from numpy.typing import NDArray

from wavetable_synthesis.core.base_generator import BaseGenerator
from wavetable_synthesis.core.decorator_registry import register_generator

# ═══════════════════════════════════════════════════════════════════
# STEP 1: Register your generator with a unique name
# ═══════════════════════════════════════════════════════════════════
# This decorator makes your generator discoverable by the CLI.
# Change "example" to your generator name (lowercase_with_underscores).
# This is the name you'll use: python -m wavetable_synthesis YOUR_NAME


@register_generator("example")  # ← CHANGE THIS
class Example(BaseGenerator):  # ← CHANGE THIS (use PascalCase)
    """Sine to sawtooth morphing generator.

    Morphs smoothly between a pure sine wave and a sawtooth wave using
    the u parameter. This demonstrates basic waveform morphing and
    linear interpolation techniques.

    This demonstrates:
    - Waveform morphing (sine ↔ sawtooth)
    - Linear interpolation
    - Basic synthesis techniques
    """

    # ═══════════════════════════════════════════════════════════════════
    # STEP 2: Add your generator metadata
    # ═══════════════════════════════════════════════════════════════════

    def get_info(self) -> dict[str, Any]:
        """Info about this generator for documentation and UI display."""
        return {
            "name": "example",
            "id": "example",
            "description": "Sine to sawtooth morphing generator",
            "author": "Wavetable Synthesis Project",
            "tags": ["example", "morphing", "sine", "sawtooth"],
            "collections": ["examples"],
            "keywords": ["morphing", "sine", "sawtooth", "interpolation"],
            "free": True,
        }

    # ═══════════════════════════════════════════════════════════════════
    # STEP 3: Configure audio processing (optional)
    # ═══════════════════════════════════════════════════════════════════

    def get_processing(self) -> dict[str, bool]:
        """Configure audio processing options for this generator."""
        return {
            "wt_normalise": True,  # Normalize wavetable
            "wt_dc_remove": True,  # Remove DC from wavetable
            "wf_normalise": True,  # Normalize each frame
            "wf_dc_remove": True,  # Remove DC from frames
        }

    # ═══════════════════════════════════════════════════════════════════
    # STEP 4: Implement your wave generation algorithm
    # ═══════════════════════════════════════════════════════════════════
    # This is where the magic happens! Replace the code below with your
    # own mathematical wave formula.

    def generate(
        self,
        theta: NDArray[np.float64],
        u: float,
    ) -> NDArray[np.float64]:
        """Generate waveform morphing between sine and sawtooth.

        Uses linear interpolation to smoothly transition between:
        - Sine wave: np.sin(theta) - smooth, pure fundamental
        - Sawtooth wave: 2*(theta/(2π) - 0.5) - bright, rich harmonics

        Args:
            theta: Phase array from 0 to 2π
            u: Morph parameter from 0.0 (sine) to 1.0 (sawtooth)

        Returns:
            Morphed waveform as float64 array
        """
        # Generate the two base waveforms
        sine_wave = np.sin(theta)  # Pure sine wave

        # Sawtooth wave: linear ramp from -1 to 1 over one cycle
        # Formula: 2 * (theta / (2π) - 0.5) simplifies to theta/π - 1
        sawtooth_wave = theta / np.pi - 1.0

        # Linear interpolation between sine and sawtooth based on u
        # u = 0.0: pure sine, u = 1.0: pure sawtooth
        mix = sine_wave * (1.0 - u) + sawtooth_wave * u

        # Normalize to ensure peak amplitude is 1.0
        peak = np.max(np.abs(mix))
        if peak > 0:
            mix = mix / peak

        output = mix

        return output.astype(np.float64)
