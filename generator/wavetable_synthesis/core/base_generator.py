"""
Base generator class for wavetable synthesis.

This module provides a base class that contributors can extend to create
new wavetable generators. It provides a clean, consistent interface and
makes it easy to add new generators to the system.
"""

from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import NDArray

from .types import GeneratorInfo, ProcessingConfig


class BaseGenerator(ABC):
    """Base class for all wavetable generators.

    This abstract base class provides a consistent interface for all
    wavetable generators. Contributors should extend this class to
    create new generators.

    Example:
        class MyGenerator(BaseGenerator):
            def get_info(self) -> GeneratorInfo:
                return {
                    "name": "my_generator",
                    "id": "my_generator",
                    "description": "My custom waveform generator",
                    "author": "Your Name",
                    "tags": ["custom"],
                    "collections": ["examples"],
                    "keywords": ["custom", "example"],
                    "free": True,
                }

            def generate(self, theta, u):
                # Your waveform generation logic here
                return np.sin(theta)  # Example: simple sine wave
    """

    @staticmethod
    def _validate_u(u: float) -> None:
        """Validate that the u parameter is within valid bounds.

        Args:
            u: Morph parameter to validate

        Raises:
            ValueError: If u is outside the range [0, 1]
        """
        if not 0.0 <= u <= 1.0:
            raise ValueError(f"Morph parameter u must be in range [0, 1], got {u}")

    # Function to generate the wavetable one sample at a time
    @abstractmethod
    def generate(
        self,
        theta: NDArray[np.float64],
        u: float,
    ) -> NDArray[np.float64]:
        """Generate waveform with IEEE 754 double precision.

        Args:
            theta: Phase array (0 to 2π) for one complete cycle
            u: Primary morph parameter [0, 1] - controls waveform transformation

        Returns:
            Generated waveform as float64 array with professional audio quality

        Note:
            All generators must return normalized waveforms within ±1.0 range
            with zero DC offset for professional synthesizer compatibility.
        """
        raise NotImplementedError("Subclasses must implement generate method")

    def get_processing(self) -> ProcessingConfig:
        """Get generator metadata for the processing pipeline configuration.

        Returns processing flags that control how the wavetable generator
        applies post-processing to the generated waveforms. These settings
        ensure professional audio quality and synthesizer compatibility.

        Returns:
            Dictionary with processing control flags:
            - wt_normalise: Enable wavetable-level normalization
            - wt_dc_remove: Enable wavetable-level DC offset removal
            - wf_normalise: Enable per-waveform normalization
            - wf_dc_remove: Enable per-waveform DC offset removal

        Note:
            These flags are used by the WavetableGenerator to determine
            which processing steps to apply during wavetable creation.
        """
        return {
            "wt_normalise": True,  # Normalize wavetable
            "wt_dc_remove": True,  # Remove DC offset from entire wavetable
            "wf_normalise": True,  # Normalize waveform
            "wf_dc_remove": True,  # Remove DC offset from each waveform
        }

    def get_info(self) -> GeneratorInfo:
        """Get comprehensive generator information for documentation and UI display.

        Provides metadata about the generator including identification,
        description, authorship, and parameter specifications. Used by
        documentation systems and user interfaces.

        Subclasses should override this method to provide their specific metadata.

        Returns:
            Dictionary containing:
            - name: Generator identifier string
            - id: Unique identifier (typically lowercase name)
            - description: Human-readable description
            - author: Creator/maintainer information
            - tags: List of category tags for the generator
            - collections: List of collections this generator belongs to
            - keywords: List of search keywords
            - free: Boolean indicating if the generator is freely available

        Note:
            This information is used by CLI tools, documentation generation,
            and user interfaces to provide consistent generator discovery.
        """
        return {
            "name": "base",
            "id": "base",
            "description": "Wavetable",
            "author": "Anonymous",
            "tags": [],
            "collections": [],
            "keywords": [],
            "free": True,
        }

    @staticmethod
    def _validate_required_string_field(info: GeneratorInfo, field_name: str) -> None:
        """Validate that a field is a non-empty string.

        Args:
            info: Generator information dictionary
            field_name: Name of the field to validate

        Raises:
            ValueError: If field is not a non-empty string
        """
        if not isinstance(info[field_name], str) or not info[field_name]:
            raise ValueError(f"Field '{field_name}' must be a non-empty string")

    @classmethod
    def validate_info(cls, info: GeneratorInfo) -> None:
        """Validate generator metadata for required fields and correct types.

        Args:
            info: Generator information dictionary to validate

        Raises:
            ValueError: If required fields are missing or have incorrect types
        """
        required_fields = ["name", "id", "description", "author", "tags", "collections", "keywords", "free"]

        # Check for required fields
        missing_fields = [field for field in required_fields if field not in info]
        if missing_fields:
            raise ValueError(f"Missing required fields in generator info: {missing_fields}")

        # Validate required non-empty string fields
        cls._validate_required_string_field(info, "name")
        cls._validate_required_string_field(info, "id")
        cls._validate_required_string_field(info, "description")

        # Author can be empty but must be a string
        if not isinstance(info["author"], str):
            raise ValueError("Field 'author' must be a string")

        if not isinstance(info["tags"], list):
            raise ValueError("Field 'tags' must be a list")

        if not isinstance(info["collections"], list):
            raise ValueError("Field 'collections' must be a list")

        if not isinstance(info["keywords"], list):
            raise ValueError("Field 'keywords' must be a list")

        if not isinstance(info["free"], bool):
            raise ValueError("Field 'free' must be a boolean")
