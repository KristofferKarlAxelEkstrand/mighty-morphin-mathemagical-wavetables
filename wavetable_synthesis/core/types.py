"""
Type definitions for wavetable synthesis.

This module contains all type definitions, protocols, and generic types
used throughout the wavetable synthesis system.
"""

from typing import Callable, Dict, List, Protocol, TypeVar, Union

import numpy as np
from numpy.typing import NDArray

# Generic type for generator classes
TGenerator = TypeVar("TGenerator", bound="GeneratorProtocol")

# Generic type for registry values
TRegistryValue = TypeVar("TRegistryValue")

# Processing configuration type
ProcessingConfig = Dict[str, bool]

# Generator metadata type
GeneratorInfo = Dict[str, Union[str, List[str], bool]]

# Generator collections type
GeneratorCollections = List[str]

# Generator tags type
GeneratorTags = List[str]

# Generator keywords type
GeneratorKeywords = List[str]


class GeneratorProtocol(Protocol):
    """Protocol defining the interface for wavetable generators.

    This protocol ensures type safety for both class-based and function-based
    generators used throughout the wavetable synthesis system.
    """

    def generate(
        self,
        theta: NDArray[np.float64],
        u: float,
    ) -> NDArray[np.float64]:
        """Generate waveform samples.

        Args:
            theta: Phase array (0 to 2π) for one complete cycle
            u: Morph parameter [0, 1] - controls waveform transformation

        Returns:
            Generated waveform as float64 array
        """
        ...

    def get_processing(self) -> ProcessingConfig:
        """Get processing configuration flags.

        Returns:
            Dictionary with processing control flags
        """
        ...

    def get_info(self) -> GeneratorInfo:
        """Get generator metadata.

        Returns:
            Dictionary containing generator information
        """
        ...


# Union type for generator inputs (class instances or functions)
GeneratorInput = Union[
    GeneratorProtocol,
    Callable[[NDArray[np.float64], float], NDArray[np.float64]],
]


# Registry type using generics
Registry = Dict[str, TRegistryValue]


# Function signature for generator functions
GeneratorFunction = Callable[[NDArray[np.float64], float], NDArray[np.float64]]


# Export all types for external use
__all__ = [
    "TGenerator",
    "TRegistryValue",
    "ProcessingConfig",
    "GeneratorInfo",
    "GeneratorCollections",
    "GeneratorTags",
    "GeneratorKeywords",
    "GeneratorProtocol",
    "GeneratorInput",
    "Registry",
    "GeneratorFunction",
]
