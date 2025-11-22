"""
Integration tests for CLI and end-to-end functionality.
"""

import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from wavetable_synthesis.core.registry import get_registry

# Get project root for subprocess calls
project_root = Path(__file__).parent.parent


def test_cli_list_generators():
    """Test CLI list functionality."""
    # Run the new CLI
    result = subprocess.run(
        [sys.executable, "-m", "wavetable_synthesis.cli.cli", "--list"],
        check=False,
        capture_output=True,
        text=True,
        cwd=str(project_root),
        encoding="utf-8",
        errors="replace",  # Handle encoding issues gracefully
    )

    assert result.returncode == 0
    # Just check that we get some generator output, don't hardcode names
    assert "Generator" in result.stdout or len(result.stdout) > 0


def test_cli_generate_single_wavetable(tmp_path):
    """Test CLI single wavetable generation."""
    # Get first available generator dynamically
    registry = get_registry(verbose=False)
    if not registry:
        pytest.skip("No generators available")

    generator_name = next(iter(registry.keys()))

    # Run generation with new positional argument format
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "wavetable_synthesis.cli.cli",
            generator_name,
            "--output",
            str(tmp_path),
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=str(project_root),
        encoding="utf-8",
        errors="replace",
    )

    assert result.returncode == 0
    assert "Success" in result.stdout

    # Check that files were created in the specified directory
    wav_file = tmp_path / f"{generator_name}_256frames_44100Hz_16bit.wav"
    assert wav_file.exists()
    assert wav_file.stat().st_size > 0  # File has content


@pytest.mark.skipif(not hasattr(np, "array"), reason="NumPy not available")
def test_file_format_correctness(tmp_path):
    """Test that generated WAV files have correct format."""
    try:
        import soundfile as sf
    except ImportError:
        pytest.skip("soundfile not available, skipping file format test")

    # Get first available generator dynamically
    registry = get_registry(verbose=False)
    if not registry:
        pytest.skip("No generators available")

    generator_name = next(iter(registry.keys()))

    # Generate a wavetable
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "wavetable_synthesis.cli.cli",
            generator_name,
            "--output",
            str(tmp_path),
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=str(project_root),
        encoding="utf-8",
        errors="replace",
    )

    assert result.returncode == 0

    # Check file properties
    wav_file = tmp_path / f"{generator_name}_256frames_44100Hz_16bit.wav"
    assert wav_file.exists()

    # Read the file and check properties
    data, samplerate = sf.read(str(wav_file), dtype="float32")

    assert samplerate == 44100
    assert data.dtype == np.float32  # Internal representation
    assert len(data) == 256 * 2048  # frames * frame_size
    assert data.ndim == 1  # Mono

    # Check that data is not all zeros
    assert not np.allclose(data, 0)
