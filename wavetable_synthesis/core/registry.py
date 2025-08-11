"""
MAWT Generator Registry - Decorator-Based System.

Import this module to access the decorator-based generator registry.
"""

# Import the decorator-based registry system
from .decorator_registry import get_registry, register_generator

# Re-export for compatibility
__all__ = ["get_registry", "register_generator"]
