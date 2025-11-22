"""
Decorator-based generator registry for MAWT.

This allows generators to self-register using decorators.
"""

from collections.abc import Callable
from typing import Any

# Global registry for decorator-based registration
_DECORATOR_REGISTRY: dict[str, Any] = {}


def register_generator(name: str) -> Callable[[type[Any]], type[Any]]:
    """Decorator to register a generator class in the wavetable synthesis registry.

    This decorator automatically instantiates and registers generator classes,
    enabling automatic discovery for the wavetable synthesis system.

    Args:
        name: Unique identifier for the generator (used in CLI and API)

    Returns:
        Decorator function that registers the class and returns it unchanged

    Example:
        @register_generator("sine_wave")
        class SineGenerator(BaseGenerator):
            pass
    """

    def decorator(cls: type[Any]) -> type[Any]:
        """Internal decorator function that performs the actual registration.

        Args:
            cls: Generator class to register

        Returns:
            The original class unchanged (for normal class definition flow)
        """
        _DECORATOR_REGISTRY[name] = cls()
        return cls

    return decorator


def get_registry(verbose: bool = True) -> dict[str, Any]:
    """Get decorator-registered generators with optional status reporting.

    Retrieves all generators that have been registered via the @register_generator
    decorator. Useful for system discovery and debugging.

    Args:
        verbose: If True, prints status information about registered generators

    Returns:
        Copy of the registry dictionary mapping names to generator instances

    Note:
        Returns a copy to prevent external modification of the internal registry.
    """
    if verbose and _DECORATOR_REGISTRY:
        print(f"Registered {len(_DECORATOR_REGISTRY)} generators:")
        for name in sorted(_DECORATOR_REGISTRY.keys()):
            generator = _DECORATOR_REGISTRY[name]
            if hasattr(generator, "description"):
                print(f"  - {name}: {generator.description}")
            elif hasattr(generator, "get_info"):
                info = generator.get_info()
                print(f"  - {name}: {info.get('description', 'No description')}")

    return _DECORATOR_REGISTRY.copy()


def clear_registry() -> None:
    """Clear the registry (useful for testing and system reset).

    Removes all registered generators from the internal registry.
    Primarily used for testing isolation and system state management.

    Warning:
        This will affect all code that depends on registered generators.
        Use with caution in production environments.
    """
    _DECORATOR_REGISTRY.clear()
