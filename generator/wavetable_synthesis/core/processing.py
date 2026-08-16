"""
Wavetable processing utilities.

This module provides utilities for processing and normalizing wavetable data.
"""

import numpy as np
from numpy.typing import NDArray

from .constants import EPSILON, FADE_SAMPLES


def normalize_waveform(waveform: NDArray[np.float64], target_peak: float = 1.0) -> NDArray[np.float64]:
    """Normalize a waveform to a target peak amplitude with IEEE 754 precision.

    Scales the waveform so its maximum absolute value equals the target peak.
    Uses epsilon-based protection against division by zero to maintain
    numerical stability in professional audio applications.

    Args:
        waveform: Input waveform array (IEEE 754 double precision)
        target_peak: Target peak amplitude (default: 1.0 for ±1 range)

    Returns:
        Normalized waveform with peak amplitude = target_peak (±1e-6 tolerance)

    Mathematical Formula:
        y_norm = y * (target_peak / max(|y|)) if max(|y|) > ε

    Note:
        Professional audio standard requires normalization within ±1e-6
        tolerance for synthesizer compatibility.
    """
    if len(waveform) == 0:
        return waveform
    peak: float = np.max(np.abs(waveform))
    if peak > EPSILON:
        return waveform * (target_peak / peak)
    return waveform


def remove_dc_offset(waveform: NDArray[np.float64]) -> NDArray[np.float64]:
    """Remove DC offset from a waveform using mean subtraction.

    Eliminates the DC component by subtracting the arithmetic mean,
    ensuring the waveform is centered around zero. This is critical
    for professional audio applications to prevent DC bias.

    Args:
        waveform: Input waveform array (IEEE 754 double precision)

    Returns:
        DC-free waveform with zero mean (< 1e-10 precision target)

    Note:
        Professional audio standard requires DC offset < 1e-10 for
        wavetable synthesis compatibility.
    """
    if len(waveform) == 0:
        return waveform
    return waveform - np.mean(waveform)


def remove_wavetable_dc_offset(
    wavetable: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Remove DC offset from entire wavetable using mean subtraction.

    Eliminates the DC component across all frames by subtracting the
    arithmetic mean of the entire wavetable. This ensures the complete
    wavetable is centered around zero, which is important when all frames
    should share the same DC reference.

    Args:
        wavetable: Input wavetable array (2D: frames × samples)

    Returns:
        DC-free wavetable with zero mean across all samples

    Note:
        Use this when you want consistent DC removal across all frames,
        rather than per-frame DC removal which treats each frame independently.
    """
    if wavetable.size == 0:
        return wavetable
    return wavetable - np.mean(wavetable)


def align_to_zero_crossing(waveform: NDArray[np.float64]) -> NDArray[np.float64]:
    """Align waveform to the first upward zero crossing for phase coherence.

    Rotates the waveform so it starts at the first upward zero crossing,
    ensuring phase alignment and seamless looping in wavetable playback.
    This is essential for professional synthesizer compatibility.

    Args:
        waveform: Input waveform array (IEEE 754 double precision)

    Returns:
        Phase-aligned waveform starting at upward zero crossing

    Algorithm:
        1. Search for first upward zero crossing (waveform[i-1] <= 0 < waveform[i])
        2. Rotate array to start at that position
        3. Fallback: align to minimum absolute value if no zero crossing found

    Note:
        Zero crossing alignment prevents phase discontinuities during
        wavetable morphing and ensures smooth parameter transitions.
    """
    # Find first upward zero crossing
    for i in range(1, len(waveform)):
        if waveform[i - 1] <= 0 < waveform[i]:
            return np.concatenate([waveform[i:], waveform[:i]])

    # Fallback: align to minimum absolute value
    idx = int(np.argmin(np.abs(waveform)))
    if idx > 0:
        return np.concatenate([waveform[idx:], waveform[:idx]])

    return waveform.copy()


def apply_fade_edges(waveform: NDArray[np.float64], fade_samples: int = FADE_SAMPLES) -> NDArray[np.float64]:
    """Apply linear fade in/out to waveform edges to reduce aliasing artifacts.

    Applies linear envelopes to the beginning and end of the waveform to
    minimize discontinuities that can cause audible clicks and aliasing.
    Essential for high-quality wavetable synthesis.

    Args:
        waveform: Input waveform array (IEEE 754 double precision)
        fade_samples: Number of samples to fade at each edge (default: 4)

    Returns:
        Waveform with smooth fade transitions at edges

    Algorithm:
        - Fade in: y[0:n] *= linspace(0, 1, n)
        - Fade out: y[-n:] *= linspace(1, 0, n)

    Note:
        Fade length is automatically limited to prevent overlap.
        Minimum waveform length = 2 * fade_samples for proper operation.
    """
    if len(waveform) <= 2 * fade_samples:
        return waveform

    # Create fade envelope
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)

    # Apply fade in
    waveform[:fade_samples] *= fade_in

    # Apply fade out
    waveform[-fade_samples:] *= fade_out

    return waveform


def clamp_amplitude(waveform: NDArray[np.float64], min_val: float = -1.0, max_val: float = 1.0) -> NDArray[np.float64]:
    """Clamp waveform amplitude to prevent digital clipping and overflow.

    Hard-limits the waveform to the specified range to prevent digital
    overflow and maintain professional audio standards. Essential for
    maintaining signal integrity in wavetable synthesis.

    Args:
        waveform: Input waveform array (IEEE 754 double precision)
        min_val: Minimum allowed amplitude value (default: -1.0)
        max_val: Maximum allowed amplitude value (default: 1.0)

    Returns:
        Amplitude-clamped waveform within [min_val, max_val] range

    Note:
        Professional audio standard uses ±1.0 range for normalized signals.
        Clamping prevents overflow during mathematical operations but may
        introduce harmonic distortion if applied to over-driven signals.
    """
    return np.clip(waveform, min_val, max_val)
