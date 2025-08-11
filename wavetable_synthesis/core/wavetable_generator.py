"""
Streamlined wavetable generator.

High-performance wavetable generation with professional audio quality.
Simplified for optimal performance and maintainability.
"""

from typing import Any

import numpy as np
from numpy.typing import NDArray

from .constants import DEFAULT_FRAME_SIZE, DEFAULT_FRAMES, EPSILON, TAU
from .processing import (
    align_to_zero_crossing,
    clamp_amplitude,
    normalize_waveform,
    remove_dc_offset,
    remove_wavetable_dc_offset,
)


class WavetableGenerator:
    """High-performance wavetable generator with professional audio processing.

    Streamlined design focused on performance and simplicity while maintaining
    professional audio quality standards.
    """

    def __init__(
        self,
        frames: int = DEFAULT_FRAMES,
        frame_size: int = DEFAULT_FRAME_SIZE,
        quality_processing: bool = True,
    ):
        """Initialize the wavetable generator.

        Args:
            frames: Number of frames in the wavetable
            frame_size: Number of samples per frame
            quality_processing: Apply professional audio processing
        """
        self.frames = frames
        self.frame_size = frame_size
        self.quality_processing = quality_processing

    def generate(self, generator: Any) -> NDArray[np.float32]:
        """Generate a wavetable using the provided generator.

        Args:
            generator: Generator function or class instance with signature (theta, u)

        Returns:
            Generated wavetable as 1D numpy array with professional audio quality
        """
        # Get processing configuration from generator if available
        processing_config = {
            "wt_normalise": True,
            "wt_dc_remove": True,
            "wf_normalise": True,
            "wf_dc_remove": True,
        }
        if hasattr(generator, "get_processing"):
            processing_config.update(generator.get_processing())

        # Create phase array (0 to 2π)
        theta = TAU * np.arange(self.frame_size, dtype=np.float64) / self.frame_size

        table = np.zeros((self.frames, self.frame_size), dtype=np.float64)

        # Generate frames with morphing parameter
        for frame_idx in range(self.frames):
            # Morph parameter: 0 at first frame, 1 at last frame
            u = frame_idx / (self.frames - 1) if self.frames > 1 else 0.0

            # Generate waveform
            if hasattr(generator, "generate"):
                waveform = generator.generate(theta, u)
            else:
                waveform = generator(theta, u)

            # Convert to float64 array
            waveform = np.asarray(waveform, dtype=np.float64)

            # Apply per-waveform processing pipeline (order matters for quality)
            if self.quality_processing:
                if processing_config.get("wf_dc_remove", True):
                    waveform = remove_dc_offset(waveform)
                if processing_config.get("wf_normalise", True):
                    waveform = normalize_waveform(waveform)
                waveform = align_to_zero_crossing(waveform)

            # Final safety clamp
            waveform = clamp_amplitude(waveform)

            table[frame_idx, :] = waveform

        # Apply wavetable-level processing
        if self.quality_processing:
            # Wavetable-level DC removal
            if processing_config.get("wt_dc_remove", True):
                table = remove_wavetable_dc_offset(table)

            # Global normalization across all frames
            if processing_config.get("wt_normalise", True):
                if table.size > 0:
                    global_peak = np.max(np.abs(table))
                    if global_peak > EPSILON:
                        table = table / global_peak

        # Convert to float32 and flatten for output
        return table.flatten().astype(np.float32)

    @classmethod
    def create_simple(
        cls,
        frames: int = DEFAULT_FRAMES,
        frame_size: int = DEFAULT_FRAME_SIZE,
    ) -> "WavetableGenerator":
        """Create a generator with optimal professional settings.

        Args:
            frames: Number of frames
            frame_size: Samples per frame

        Returns:
            Configured WavetableGenerator with professional defaults
        """
        return cls(frames=frames, frame_size=frame_size, quality_processing=True)
