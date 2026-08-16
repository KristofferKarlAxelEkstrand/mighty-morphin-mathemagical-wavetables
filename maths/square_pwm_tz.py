"""
Through-zero PWM square wave generator for MAWT.

Implements a square wave using a comparator approach.
"""

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from wavetable_synthesis.core.base_generator import BaseGenerator
from wavetable_synthesis.core.decorator_registry import register_generator


@register_generator("square_pwm_tz")
@dataclass
class SquarePWMTZGenerator(BaseGenerator):
    """Through-zero PWM square wave generator.

    This class provides a clean, extensible interface for generating
    through-zero PWM square waveforms using a comparator approach.
    """

    def get_info(self) -> dict[str, Any]:
        """Get generator metadata for documentation and UI display.

        Returns comprehensive information about this generator including
        identification, description, authorship, and categorization.

        Returns:
            Dictionary containing:
            - name: Generator identifier string
            - id: Unique identifier (typically lowercase name)
            - description: Human-readable description
            - author: Creator/maintainer information
            - tags: List of category tags for the generator
            - collections: List of collections this generator belongs to
            - keywords: List of search keywords
            - free: Boolean indicating if the generator is freely available
        """
        return {
            "name": "Square PWM TZ",
            "id": "square_pwm_tz",
            "description": "Through-zero PWM square wave via comparator",
            "author": "Kristoffer Ekstrand",
            "tags": ["PWM", "square", "through-zero"],
            "collections": ["PWM"],
            "keywords": ["PWM", "square", "through-zero"],
            "free": True,
        }

    # Function to generate the wavetable one sample at a time
    def generate(
        self,
        theta: NDArray[np.float64],
        u: float,
    ) -> NDArray[np.float64]:
        """Generate through-zero PWM square waveform using comparator approach.

        Implements pulse width modulation by comparing a sine wave against a
        threshold value. Uses hard sign comparator with epsilon protection
        for numerical stability and professional audio quality.

        Args:
            theta: Phase array (2π * t) for one complete cycle
            u: Morph parameter [0, 1] - maps to pulse width [-1, 1]

        Returns:
            Generated square waveform as float64 array with ±1.0 amplitude

        Mathematical Formula:
            pw = 2u - 1  (maps u ∈ [0,1] to pw ∈ [-1,1])
            y = sign(sin(θ) - pw) with epsilon protection
        """
        # Map morph parameter u ∈ [0,1] to pulse width pw ∈ [-1,1] with clamping
        pw = 2.0 * u - 1.0  # Linear mapping: u=0 → pw=-1, u=1 → pw=+1
        pw = max(-1.0, min(1.0, pw))  # Clamp to valid range for numerical stability
        tau = pw  # Threshold parameter for comparator

        # Generate base sine wave for PWM comparison
        s = np.sin(theta)
        eps = 1e-12  # Epsilon for numerical stability in zero detection

        # Implement through-zero PWM using hard sign comparator
        # y = sign(sin(θ) - τ) where τ controls pulse width
        d = s - tau
        y = np.where(d > eps, 1.0, np.where(d < -eps, -1.0, 0.0))

        return np.asarray(y, dtype=np.float64)
