"""
Command-line interface for wavetable synthesis.
"""

from typing import Any


def __getattr__(name: str) -> Any:
    """Lazy import for CLI modules."""
    if name == "cli_main":
        from .cli import main  # pylint: disable=import-outside-toplevel

        return main
    if name == "test_main":
        from .test_cli import main  # pylint: disable=import-outside-toplevel

        return main
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = ["cli_main", "test_main"]  # pylint: disable=undefined-all-variable
