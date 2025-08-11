"""
Sine to triangle morph generator for MAWT.

Provides smooth morphing between sine and triangle waveforms.
"""

import math
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from wavetable_synthesis.core.base_generator import BaseGenerator
from wavetable_synthesis.core.decorator_registry import register_generator


@register_generator("sine_to_triangle")
@dataclass
class SineToTriangleGenerator(BaseGenerator):
    """Sine to triangle morph generator.

    This class provides a clean, extensible interface for generating
    sine-to-triangle morphing waveforms. It's designed to be easy
    for contributors to understand and extend.
    """

    def get_info(self) -> dict[str, Any]:
        """Info about this generator for documentation and UI display."""
        return {
            "name": "sine_to_triangle",
            "id": "sine_to_triangle",
            "description": "Sine to triangle morph generator",
            "author": "Kristoffer Ekstrand",
            "tags": ["morph", "sine", "triangle"],
            "collections": ["morphing"],
            "keywords": ["sine", "triangle", "morph"],
            "free": True,
        }

    # Function to generate the wavetable one sample at a time
    def generate(
        self,
        theta: NDArray[np.float64],
        u: float,
    ) -> NDArray[np.float64]:
        """Generate sine-to-triangle morph waveform with mathematical precision.

        Implements smooth morphing between pure sine and triangle waveforms using
        inverse sine transformation for the triangle component. Uses IEEE 754
        double precision throughout for professional audio quality.

        Args:
            theta: Phase array (2π * t) for one complete cycle
            u: Morph parameter [0, 1] - 0=pure sine, 1=pure triangle

        Returns:
            Generated waveform as float64 array, normalized to ±1.0 range

        Mathematical Formula:
            sine(θ) = sin(θ)
            triangle(θ) = (2/π) * arcsin(sin(θ))
            result(θ, u) = (1-u) * sine(θ) + u * triangle(θ)
        """
        # Generate base waveforms using precise mathematical formulations
        sine = np.sin(theta)  # Pure sinusoidal component
        tri = (2.0 / math.pi) * np.arcsin(sine)  # Triangle via inverse sine transform

        # Perform linear morphing between waveforms with IEEE 754 precision
        y = (1.0 - u) * sine + u * tri

        return np.asarray(y, dtype=np.float64)
