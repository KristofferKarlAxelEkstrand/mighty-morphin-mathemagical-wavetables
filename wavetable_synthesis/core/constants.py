"""
Audio constants for wavetable synthesis.

Professional audio standards and configuration values.
"""

import math
from typing import List

# Mathematical constants
TAU: float = 2.0 * math.pi  # 2π for phase calculations
EPSILON: float = 1e-12  # Numerical stability threshold

# Default audio parameters
DEFAULT_SAMPLE_RATE: int = 44100
DEFAULT_BIT_DEPTH: int = 16
DEFAULT_FRAME_SIZE: int = 2048
DEFAULT_FRAMES: int = 256

# Supported formats
SUPPORTED_BIT_DEPTHS: List[int] = [16, 24, 32]

# Output configuration
DEFAULT_OUTPUT_DIR: str = "wavetable_dist"

# Processing settings
NORMALIZE_FRAME_BY_FRAME: bool = True
NORMALIZE_GLOBAL: bool = True
APPLY_DC_REMOVAL: bool = True
APPLY_ZERO_CROSSING_ALIGNMENT: bool = True
FADE_SAMPLES: int = 4  # Edge fade samples when enabled
