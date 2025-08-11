"""
Pytest configuration and shared fixtures for wavetable synthesis tests.
"""

from typing import Any, Dict

import numpy as np
import pytest

from wavetable_synthesis.core.generator import generate_wavetable
from wavetable_synthesis.core.registry import get_registry


@pytest.fixture
def sample_theta() -> np.ndarray:
    """Sample theta array for testing."""
    frame_size = 1024
    return 2.0 * np.pi * np.arange(frame_size, dtype=np.float64) / frame_size


@pytest.fixture
def sample_t() -> np.ndarray:
    """Sample t array for testing (normalized 0-1 position)."""
    frame_size = 1024
    return np.arange(frame_size, dtype=np.float64) / frame_size


@pytest.fixture
def registry() -> Dict[str, Any]:
    """Generator registry fixture."""
    return get_registry(verbose=False)


@pytest.fixture
def any_generator(registry: Dict[str, Any]) -> Any:
    """Fixture that returns the first available generator for basic testing."""
    if not registry:
        pytest.skip("No generators available")
    return next(iter(registry.values()))


@pytest.fixture
def first_generator_name(registry: Dict[str, Any]) -> str:
    """Fixture that returns the name of the first available generator."""
    if not registry:
        pytest.skip("No generators available")
    return next(iter(registry.keys()))


@pytest.fixture
def test_wavetable(any_generator: Any) -> np.ndarray:
    """Basic test wavetable fixture."""
    return generate_wavetable(any_generator, frames=64, frame_size=512)
