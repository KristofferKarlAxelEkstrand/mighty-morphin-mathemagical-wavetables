"""
Export functionality for wavetable formats.

This module handles saving wavetables to various audio formats
and managing output directories.
"""

from pathlib import Path
from typing import List, Optional, Union

import numpy as np
import soundfile as sf

from ..core.constants import (
    DEFAULT_FRAME_SIZE,
    DEFAULT_OUTPUT_DIR,
    SUPPORTED_BIT_DEPTHS,
)


def get_bit_depth_subtype(bit_depth: int) -> str:
    """Convert bit depth to soundfile subtype for professional audio export.

    Maps integer bit depths to the corresponding soundfile PCM subtype
    strings required for proper WAV file encoding. Ensures compatibility
    with professional audio software and synthesizers.

    Args:
        bit_depth: Bit depth (16, 24, or 32 bits per sample)

    Returns:
        Soundfile subtype string ("PCM_16", "PCM_24", or "PCM_32")

    Raises:
        ValueError: If bit_depth is not in SUPPORTED_BIT_DEPTHS

    Note:
        16-bit: Standard CD quality, most compatible
        24-bit: Professional studio standard, extended dynamic range
        32-bit: Maximum precision, preferred for synthesis applications
    """
    if bit_depth == 16:
        return "PCM_16"
    if bit_depth == 24:
        return "PCM_24"
    if bit_depth == 32:
        return "PCM_32"
    raise ValueError(f"Unsupported bit depth: {bit_depth}. Use 16, 24, or 32.")


def generate_filename(
    name: str,
    frames: int,
    sample_rate: int,
    bit_depth: int,
) -> str:
    """Generate a standardized filename for wavetable export with metadata encoding.

    Creates consistent filenames that embed essential wavetable metadata
    for easy identification and organization. Follows professional audio
    naming conventions for synthesizer compatibility.

    Args:
        name: Base name of the wavetable (descriptive identifier)
        frames: Number of frames in the wavetable
        sample_rate: Sample rate in Hz (metadata only, not audio content)
        bit_depth: Bit depth for export format

    Returns:
        Formatted filename: "{name}_{frames}frames_{sample_rate}Hz_{bit_depth}bit.wav"

    Example:
        generate_filename("sine_to_triangle", 256, 44100, 24)
        → "sine_to_triangle_256frames_44100Hz_24bit.wav"

    Note:
        Sample rate in filename is metadata only - wavetables are sample-rate
        independent for synthesis applications.
    """
    return f"{name}_{frames}frames_{sample_rate}Hz_{bit_depth}bit.wav"


def save_wavetable(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    name: str,
    data: np.ndarray,
    output_dir: Union[str, Path] = DEFAULT_OUTPUT_DIR,
    sample_rate: int = 44100,
    bit_depth: int = 16,
    frames: Optional[int] = None,
) -> Path:
    """Save wavetable to WAV file.

    Args:
        name: Name of the wavetable
        data: Audio data as numpy array
        output_dir: Output directory as string or Path (default: "wavetables")
        sample_rate: Sample rate in Hz (default: 44100)
        bit_depth: Bit depth (16, 24, or 32) (default: 16)
        frames: Number of frames (calculated from data if not provided)

    Returns:
        Path object to the saved file

    Example:
        >>> from pathlib import Path
        >>> filepath = save_wavetable("sine", data, output_dir="./waves")
        >>> print(filepath)  # Path object
        waves/sine_256frames_44100Hz_16bit.wav
        >>> str(filepath)    # Convert to string if needed
        'waves/sine_256frames_44100Hz_16bit.wav'
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Calculate frames if not provided
    if frames is None:
        frames = len(data) // DEFAULT_FRAME_SIZE

    # Get soundfile subtype
    subtype = get_bit_depth_subtype(bit_depth)

    # Generate filename
    filename = generate_filename(name, frames, sample_rate, bit_depth)
    filepath = output_path / filename

    # Write file
    sf.write(str(filepath), data, sample_rate, subtype=subtype)
    print(f"Saved: {filepath}")

    return filepath


# pylint: disable=too-many-arguments,too-many-positional-arguments
def export_wavetable(
    name: str,
    data: np.ndarray,
    output_dir: Union[str, Path] = DEFAULT_OUTPUT_DIR,
    sample_rate: Union[int, List[int]] = 44100,
    bit_depth: Union[int, List[int]] = 16,
    frames: Optional[int] = None,
) -> Union[Path, List[Path]]:
    """Unified export function for wavetable in single or multiple formats.

    This is the main export function that handles both single file export
    and batch export to multiple formats/configurations.

    Args:
        name: Name of the wavetable
        data: Audio data as numpy array
        output_dir: Output directory as string or Path (default: "wavetables")
        sample_rate: Sample rate(s) in Hz (int or list, default: 44100)
        bit_depth: Bit depth(s) (int or list, default: 16)
        frames: Number of frames (calculated from data if not provided)

    Returns:
        Path object to saved file or list of Path objects for batch export

    Examples:
        # Single export - returns Path object
        path = export_wavetable("my_wave", data)
        print(path)  # PosixPath('wavetables/my_wave_256frames_44100Hz_16bit.wav')

        # Batch export - returns list of Path objects
        paths = export_wavetable("my_wave", data, sample_rate=[44100, 48000])
        for path in paths:
            print(path.name)  # Access Path properties

        # Convert to string if needed
        path_str = str(path)

        # Batch export with multiple formats
        paths = export_wavetable("my_wave", data,
                                sample_rate=[44100, 48000],
                                bit_depth=[16, 24, 32])
    """
    # Convert single values to lists for unified processing
    sample_rates = [sample_rate] if isinstance(sample_rate, int) else sample_rate
    bit_depths = [bit_depth] if isinstance(bit_depth, int) else bit_depth

    # Validate parameters
    for rate in sample_rates:
        if rate <= 0:
            raise ValueError(f"Sample rate must be positive, got {rate}")

    for depth in bit_depths:
        if depth not in SUPPORTED_BIT_DEPTHS:
            raise ValueError(f"Unsupported bit depth {depth}. " f"Must be one of {SUPPORTED_BIT_DEPTHS}")

    # If only single configuration, use simple export
    if len(sample_rates) == 1 and len(bit_depths) == 1:
        return save_wavetable(
            name=name,
            data=data,
            output_dir=output_dir,
            sample_rate=sample_rates[0],
            bit_depth=bit_depths[0],
            frames=frames,
        )

    # Batch export
    saved_files = []
    for rate in sample_rates:
        for depth in bit_depths:
            path = save_wavetable(
                name=name,
                data=data,
                output_dir=output_dir,
                sample_rate=rate,
                bit_depth=depth,
                frames=frames,
            )
            saved_files.append(path)

    return saved_files


def save_wavetable_simple(name: str, data: np.ndarray, sample_rate: int = 44100, bit_depth: int = 16) -> Path:
    """Save wavetable to WAV file (simple version for basic usage).

    Args:
        name: Name of the wavetable
        data: Audio data as numpy array
        sample_rate: Sample rate in Hz (default: 44100)
        bit_depth: Bit depth (16, 24, or 32) (default: 16)

    Returns:
        Path object to the saved file

    Example:
        >>> filepath = save_wavetable_simple("my_wave", data)
        >>> print(filepath.exists())  # True
        >>> print(filepath.name)      # 'my_wave_256frames_44100Hz_16bit.wav'
    """
    result = export_wavetable(name, data, DEFAULT_OUTPUT_DIR, sample_rate, bit_depth)
    # Since we're passing single values, export_wavetable returns a Path object
    return result  # type: ignore[return-value]


__all__ = [
    "export_wavetable",
    "save_wavetable",
    "save_wavetable_simple",
]
