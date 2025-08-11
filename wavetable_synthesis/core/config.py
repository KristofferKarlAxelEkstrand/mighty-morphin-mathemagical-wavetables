"""
Configuration classes for wavetable synthesis.

Type-safe configuration using dataclasses.
"""

from dataclasses import dataclass
from typing import Optional

from .constants import (
    DEFAULT_BIT_DEPTH,
    DEFAULT_FRAME_SIZE,
    DEFAULT_FRAMES,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SAMPLE_RATE,
    SUPPORTED_BIT_DEPTHS,
)


@dataclass
class WavetableConfig:
    """Configuration for wavetable generation."""

    frames: int = DEFAULT_FRAMES
    frame_size: int = DEFAULT_FRAME_SIZE
    sample_rate: int = DEFAULT_SAMPLE_RATE
    bit_depth: int = DEFAULT_BIT_DEPTH
    output_dir: str = DEFAULT_OUTPUT_DIR
    waveform_name: str = ""

    def get_filename(self) -> str:
        """Generate filename based on configuration."""
        return f"{self.waveform_name}_{self.frames}frames_" f"{self.sample_rate}Hz_{self.bit_depth}bit.wav"

    def validate(self) -> None:
        """Validate configuration parameters."""
        if self.frames <= 0:
            raise ValueError(f"frames must be positive, got {self.frames}")
        if self.frame_size <= 0:
            raise ValueError(f"frame_size must be positive, got {self.frame_size}")
        if self.sample_rate <= 0:
            raise ValueError(f"sample_rate must be positive, got {self.sample_rate}")
        if self.bit_depth not in SUPPORTED_BIT_DEPTHS:
            raise ValueError(f"bit_depth must be one of {SUPPORTED_BIT_DEPTHS}")
        if not self.waveform_name:
            raise ValueError("waveform_name cannot be empty")


@dataclass
class CLIConfig:
    """Configuration for CLI operations."""

    list_generators: bool = False
    clear_output: bool = False
    wavetable_config: Optional[WavetableConfig] = None

    def should_generate(self) -> bool:
        """Check if generation should proceed."""
        return not (self.list_generators or self.clear_output)

    def validate(self) -> None:
        """Validate CLI configuration."""
        if self.should_generate() and self.wavetable_config is None:
            raise ValueError("wavetable_config is required for generation")
