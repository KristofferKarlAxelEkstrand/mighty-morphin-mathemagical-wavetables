"""Linear interpolation generator using the new t parameter.

This generator demonstrates how to use the normalized t parameter (0-1)
for simple linear interpolation between two waveforms.
"""

import numpy as np
from numpy.typing import NDArray

from wavetable_synthesis.core.base_generator import BaseGenerator
from wavetable_synthesis.core.decorator_registry import register_generator


@register_generator("linear_interpolation")
class LinearInterpolation(BaseGenerator):
    """Generator that morphs between sine and square using linear interpolation."""

    @classmethod
    def get_metadata(cls) -> dict[str, str | list[str] | bool]:
        return {
            "name": "linear_interpolation",
            "description": "Linear interpolation between sine and square",
            "author": "Wavetable Project",
            "version": "1.0.0",
            "tags": ["morph", "sine", "square", "linear", "interpolation"],
            "collections": ["educational", "morphing"],
            "keywords": ["linear", "interpolation", "morph"],
            "free": True,
        }

    def generate(
        self,
        theta: NDArray[np.float64],
        u: float,
    ) -> NDArray[np.float64]:
        """Generate waveform using linear interpolation with u parameter.

        This demonstrates morphing between sine and square waves using the u parameter.
        The morphing creates smooth transitions between the two waveforms.

        Args:
            theta: Phase array (0 to 2π) for one complete cycle
            u: Morph parameter [0, 1] - controls overall waveform shape

        Returns:
            Generated waveform as float64 array
        """
        # Create start and end waveforms
        sine_wave = np.sin(theta)
        square_wave = np.sign(np.sin(theta))

        # Use u for linear interpolation between waveforms
        # This creates smooth morphing from sine to square
        waveform = sine_wave * (1.0 - u) + square_wave * u

        # Ensure proper return type
        result: NDArray[np.float64] = waveform.astype(np.float64)
        return result
