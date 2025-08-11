"""
Core wavetable synthesis functionality.
"""

from .generator import generate_wavetable
from .registry import get_registry

__all__ = [
    "generate_wavetable",
    "get_registry",
]
