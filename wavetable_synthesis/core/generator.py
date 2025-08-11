"""
Core wavetable generation interface.

Streamlined high-level API for wavetable generation.
"""

import numpy as np
from numpy.typing import NDArray

from .constants import DEFAULT_FRAME_SIZE, DEFAULT_FRAMES
from .types import GeneratorInput
from .wavetable_generator import WavetableGenerator


def generate_wavetable(
    generator: GeneratorInput,
    frames: int = DEFAULT_FRAMES,
    frame_size: int = DEFAULT_FRAME_SIZE,
) -> NDArray[np.float32]:
    """Generate a wavetable with professional audio quality.

    This is the main interface for wavetable generation. Supports both
    function-based and class-based generators with the (theta, u) signature.

    Args:
        generator: Generator function or class instance with signature (theta, u)
        frames: Number of frames in the wavetable
        frame_size: Number of samples per frame

    Returns:
        Generated wavetable as 1D numpy array

    Example:
        >>> from generators.sine_to_triangle import (
        ...     SineToTriangleGenerator
        ... )
        >>> gen = SineToTriangleGenerator()
        >>> wavetable = generate_wavetable(gen, frames=64, frame_size=2048)
        >>> print(f"Generated {len(wavetable)} samples")
    """
    wt_gen = WavetableGenerator.create_simple(frames, frame_size)
    return wt_gen.generate(generator)
