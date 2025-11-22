"""
Wavetable Synthesis Package

A modern Python package for generating high-quality wavetables
using mathematical functions and real-time audio synthesis.
"""

from typing import List

__version__ = "0.1.0"
__author__ = "Kristoffer Ekstrand"
__description__ = "Wavetable generators, functions make sounds and math do the rest"

# Import main functions for easy access
from .core import generate_wavetable
from .core.registry import get_registry
from .export import save_wavetable_simple

# Lazy import CLI to avoid import cycles
try:
    from .cli import cli_main
except ImportError:
    cli_main = None  # pylint: disable=invalid-name


def _get_all_exports() -> list[str]:
    """Get all exports including dynamically registered generators.

    Note: This imports the generators module to ensure decorators are executed.
    """
    # Import generators to trigger @register_generator decorators
    # pylint: disable=import-outside-toplevel,unused-import
    import wavetable_generators

    exports = [
        "generate_wavetable",
        "save_wavetable_simple",
        "cli_main",
        "get_registry",
    ]

    # Add all registered generators
    registry = get_registry(verbose=False)
    exports.extend(registry.keys())

    return exports


__all__ = _get_all_exports()
