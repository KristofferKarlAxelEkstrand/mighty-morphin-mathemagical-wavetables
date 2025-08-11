"""
Property-based and advanced tests for wavetable synthesis.
"""

import time

import numpy as np
import pytest

from wavetable_synthesis.core.generator import generate_wavetable


@pytest.mark.parametrize("u", np.linspace(0.0, 1.0, 11))
def test_property_based_u_values(any_generator, sample_theta, sample_t, u):
    """Test generator behavior with various u values using property-based approach."""
    result = any_generator.generate(sample_theta, u)

    # Basic properties that should always hold
    assert isinstance(result, np.ndarray)
    assert len(result) == len(sample_theta)
    assert np.isfinite(result).all()  # No NaN or inf values
    assert np.max(np.abs(result)) > 0  # Not all zeros

    # Check normalization (should be close to 1.0)
    peak = np.max(np.abs(result))
    assert 0.8 <= peak <= 1.2  # Allow some tolerance


def test_aliasing_detection(any_generator):
    """Test for potential aliasing issues."""
    frame_size = 256  # Small frame size to test high frequencies
    theta = 2.0 * np.pi * np.arange(frame_size, dtype=np.float64) / frame_size

    waveform = any_generator.generate(theta, 0.5)

    # Check for high-frequency content that might indicate aliasing
    diff = np.diff(waveform)
    max_diff = np.max(np.abs(diff))

    # Waveform shouldn't have extreme discontinuities
    assert max_diff < 2.0


@pytest.mark.parametrize(
    "frames,frame_size",
    [
        (32, 512),  # Small
        (128, 1024),  # Medium
        (256, 2048),  # Large
    ],
)
def test_performance_benchmark(any_generator, frames, frame_size):
    """Benchmark wavetable generation performance."""
    start_time = time.time()
    wavetable = generate_wavetable(any_generator, frames, frame_size)
    end_time = time.time()

    generation_time = end_time - start_time
    if generation_time == 0:
        generation_time = 1e-6  # Avoid division by zero for very fast operations
    samples_per_second = (frames * frame_size) / generation_time

    print(
        f"Generated {frames} frames of {frame_size} samples in {generation_time:.3f}s "
        f"({samples_per_second:.1f} samples/sec)"
    )

    # Performance should be reasonable
    assert generation_time < 10.0  # Less than 10 seconds for any test case
    assert len(wavetable) == frames * frame_size


def test_memory_usage(any_generator):
    """Test memory usage patterns."""
    frames = 512
    frame_size = 4096

    # This should not cause memory issues
    wavetable = generate_wavetable(any_generator, frames, frame_size)

    # Verify we got the expected data
    assert len(wavetable) == frames * frame_size
    assert wavetable.dtype == np.float32

    # Memory usage should be reasonable
    memory_mb = wavetable.nbytes / (1024 * 1024)
    expected_mb = (frames * frame_size * 4) / (1024 * 1024)  # 4 bytes per float32
    assert abs(memory_mb - expected_mb) < 0.1  # Should match expected size


@pytest.mark.parametrize("u", [-10.0, -1.0, 0.0, 1.0, 10.0])
def test_edge_cases(any_generator, sample_theta, sample_t, u):
    """Test edge cases and boundary conditions."""
    result = any_generator.generate(sample_theta, u)

    assert isinstance(result, np.ndarray)
    assert len(result) == len(sample_theta)
    assert np.isfinite(result).all()


@pytest.mark.parametrize("u", [0.0, 0.25, 0.5, 0.75, 1.0])
def test_waveform_quality_metrics(any_generator, sample_theta, sample_t, u):
    """Test various waveform quality metrics."""
    waveform = any_generator.generate(sample_theta, u)

    assert isinstance(waveform, np.ndarray)  # Ensure it's an ndarray

    # RMS level should be reasonable (relaxed for different generators)
    rms = np.sqrt(np.mean(waveform**2))
    assert 0.3 <= rms <= 1.0

    # Crest factor should be reasonable (peak/RMS)
    if rms > 0:
        crest_factor = np.max(np.abs(waveform)) / rms
        assert crest_factor <= 10.0  # Shouldn't be too peaky

    # Check for reasonable DC offset (relaxed for different generators)
    dc_offset = np.mean(waveform)
    assert abs(dc_offset) < 0.8  # Some generators may have intentional DC offset
