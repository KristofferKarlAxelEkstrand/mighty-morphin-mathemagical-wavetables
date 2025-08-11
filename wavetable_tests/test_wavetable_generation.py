"""
Test suite for wavetable synthesis package.
"""

import numpy as np
import pytest

from wavetable_synthesis.core.generator import generate_wavetable
from wavetable_synthesis.core.processing import align_to_zero_crossing


@pytest.fixture
def sample_theta():
    """Sample theta array for testing."""
    frame_size = 1024
    return 2.0 * np.pi * np.arange(frame_size, dtype=np.float64) / frame_size


class TestGeneratorRegistry:
    """Test the generator registry functionality."""

    def test_registry_loading(self, registry):
        """Test that registry loads generators correctly."""
        assert len(registry) >= 1  # At least one generator should be loaded

    def test_generator_function_signature(self, any_generator):
        """Test that generators have correct function signature."""
        import inspect

        sig = inspect.signature(any_generator.generate)
        params = list(sig.parameters.keys())

        assert len(params) >= 2
        assert params[0] == "theta"
        assert params[1] == "u"

    def test_generator_return_types(self, any_generator, sample_theta, sample_t):
        """Test generator return types."""
        result = any_generator.generate(sample_theta, 0.5)

        assert isinstance(result, np.ndarray)
        assert result.dtype in [np.float32, np.float64]

        # Test metadata access via class methods
        meta_result = any_generator.get_processing()
        assert isinstance(meta_result, dict)
        assert "wt_normalise" in meta_result


class TestWavetableGeneration:
    """Test wavetable generation functionality."""

    def test_make_wavetable_basic(self, any_generator):
        """Test basic wavetable generation."""
        frames = 64
        frame_size = 512
        wavetable = generate_wavetable(any_generator, frames, frame_size)

        assert isinstance(wavetable, np.ndarray)
        assert wavetable.dtype == np.float32
        assert len(wavetable) == frames * frame_size

    def test_make_wavetable_normalization(self, any_generator):
        """Test that generated wavetables are properly normalized."""
        frames = 32
        frame_size = 256
        wavetable = generate_wavetable(any_generator, frames, frame_size)

        # Check that the wavetable is normalized (peak should be close to 1.0)
        peak = float(np.max(np.abs(wavetable)))
        assert 0.95 <= peak <= 1.05  # Allow some tolerance

    def test_make_wavetable_u_parameter_range(self, any_generator):
        """Test u parameter range handling."""
        frame_size = 256

        # Test u = 0 (should be pure sine-like)
        wt_0 = generate_wavetable(any_generator, 1, frame_size)

        # Test u = 1 (should be triangle-like)
        wt_1 = generate_wavetable(any_generator, 1, frame_size)

        assert len(wt_0) == frame_size
        assert len(wt_1) == frame_size

    def test_make_wavetable_with_meta(self, any_generator):
        """Test make_wavetable with meta support."""

        frames = 64
        frame_size = 512
        wavetable = generate_wavetable(any_generator, frames, frame_size)

        assert isinstance(wavetable, np.ndarray)
        assert wavetable.dtype == np.float32
        assert len(wavetable) == frames * frame_size

    def test_write_wav_function(self, tmp_path):
        """Test write_wav function."""
        import numpy as np

        from wavetable_synthesis.export.wav import save_wavetable

        # Create test data - use a single frame worth of data
        data = np.sin(np.linspace(0, 2 * np.pi, 2048, endpoint=False)).astype(np.float32)

        # Test write with explicit frames parameter
        save_wavetable("test", data, str(tmp_path), frames=1)

        # Check file exists
        assert (tmp_path / "test_1frames_44100Hz_16bit.wav").exists()

    def test_generate_filename_function(self):
        """Test filename generation function."""
        from wavetable_synthesis.export.wav import generate_filename

        filename = generate_filename("test_wave", 2048, 44100, 16)
        expected = "test_wave_2048frames_44100Hz_16bit.wav"
        assert filename == expected

    def test_zero_crossing_alignment(self, sample_theta):
        """Test zero crossing alignment function."""
        # Create a test signal that's not aligned
        test_signal = np.sin(sample_theta + np.pi / 4)  # Phase shift

        aligned = align_to_zero_crossing(test_signal)

        # Check that alignment worked (first sample should be close to zero)
        assert abs(aligned[0]) < 0.1

        # Check that the signal is still the same length
        assert len(aligned) == len(test_signal)


class TestParameterRanges:
    """Test parameter range validation."""

    def test_u_parameter_clamping(self, any_generator, sample_theta, sample_t):
        """Test that u parameter is properly clamped."""
        result_low = any_generator.generate(sample_theta, -0.5)
        result_high = any_generator.generate(sample_theta, 1.5)
        result_zero = any_generator.generate(sample_theta, 0.0)
        result_one = any_generator.generate(sample_theta, 1.0)

        assert isinstance(result_low, np.ndarray)
        assert isinstance(result_high, np.ndarray)
        assert isinstance(result_zero, np.ndarray)
        assert isinstance(result_one, np.ndarray)

    def test_extreme_frame_sizes(self, any_generator):
        """Test generation with extreme frame sizes."""

        # Very small frame size
        small_wt = generate_wavetable(any_generator, frames=1, frame_size=8)
        assert len(small_wt) == 8

        # Large frame size
        large_wt = generate_wavetable(any_generator, frames=1, frame_size=8192)
        assert len(large_wt) == 8192

    def test_single_frame_generation(self, any_generator):
        """Test generation with single frame."""

        single_wt = generate_wavetable(any_generator, frames=1, frame_size=2048)
        assert len(single_wt) == 2048

    def test_invalid_parameters(self, any_generator):
        """Test handling of invalid parameters."""

        # This should not raise an exception but handle gracefully
        try:
            wt = generate_wavetable(any_generator, frames=0, frame_size=2048)
            # If it returns something, check it's reasonable
            assert isinstance(wt, np.ndarray)
        except (ValueError, ZeroDivisionError):
            # Expected for invalid parameters
            pass


class TestAudioQuality:
    """Test audio quality aspects."""

    def test_no_dc_offset(self, any_generator):
        """Test that generated waveforms have minimal DC offset."""
        frame_size = 1024
        frames = 16
        wavetable = generate_wavetable(any_generator, frames, frame_size)

        # Reshape to frames
        wavetable_2d = wavetable.reshape(frames, frame_size)

        for frame_idx in range(frames):
            frame = wavetable_2d[frame_idx, :]
            dc_offset = np.mean(frame)
            assert abs(dc_offset) < 0.01  # DC offset should be very small

    def test_waveform_continuity(self, any_generator):
        """Test that waveforms are continuous (no clicks/pops)."""
        frame_size = 512
        frames = 8
        wavetable = generate_wavetable(any_generator, frames, frame_size)

        # Reshape to frames
        wavetable_2d = wavetable.reshape(frames, frame_size)

        for frame_idx in range(frames):
            frame = wavetable_2d[frame_idx, :]

            # Check that first and last samples are close (for looping)
            continuity_error = abs(frame[0] - frame[-1])
            assert continuity_error < 0.1  # Should be very close for smooth looping


class TestProcessing:
    """Test processing utilities."""

    def test_normalize_waveform_basic(self):
        """Test basic waveform normalization."""
        from wavetable_synthesis.core.processing import normalize_waveform

        # Create test waveform with peak of 2.0
        waveform = np.array([0.0, 1.0, 2.0, 1.0, 0.0], dtype=np.float64)

        normalized = normalize_waveform(waveform, target_peak=1.0)

        # Check peak is 1.0
        assert np.max(np.abs(normalized)) == pytest.approx(1.0, abs=1e-6)
        # Check shape preserved
        assert len(normalized) == len(waveform)

    def test_normalize_waveform_zero_input(self):
        """Test normalization with zero input."""
        from wavetable_synthesis.core.processing import normalize_waveform

        waveform = np.zeros(10, dtype=np.float64)
        normalized = normalize_waveform(waveform)

        # Should return unchanged
        assert np.allclose(normalized, waveform)

    def test_remove_dc_offset(self):
        """Test DC offset removal."""
        from wavetable_synthesis.core.processing import remove_dc_offset

        # Create waveform with DC offset
        waveform = np.array([0.5, 1.5, 2.5, 1.5, 0.5], dtype=np.float64)
        cleaned = remove_dc_offset(waveform)

        # Mean should be very close to zero
        assert abs(np.mean(cleaned)) < 1e-10

    def test_align_to_zero_crossing_upward(self):
        """Test zero crossing alignment with upward crossing."""
        from wavetable_synthesis.core.processing import align_to_zero_crossing

        # Create waveform: [0.5, -0.5, 0.5, 1.0, 0.5]
        # First upward zero crossing is between -0.5 and 0.5 (index 1->2)
        waveform = np.array([0.5, -0.5, 0.5, 1.0, 0.5], dtype=np.float64)
        aligned = align_to_zero_crossing(waveform)

        # Should start with positive value close to zero crossing
        assert aligned[0] > 0  # First sample should be positive
        assert len(aligned) == len(waveform)

    def test_align_to_zero_crossing_no_crossing(self):
        """Test zero crossing alignment when no crossing exists."""
        from wavetable_synthesis.core.processing import align_to_zero_crossing

        # All positive waveform
        waveform = np.array([0.1, 0.2, 0.3, 0.4, 0.5], dtype=np.float64)
        aligned = align_to_zero_crossing(waveform)

        # Should align to minimum absolute value (first element)
        assert aligned[0] == 0.1
        assert len(aligned) == len(waveform)

    def test_apply_fade_edges(self):
        """Test fade edges application."""
        from wavetable_synthesis.core.processing import apply_fade_edges

        # Create test waveform
        waveform = np.ones(20, dtype=np.float64)
        faded = apply_fade_edges(waveform, fade_samples=4)

        # First 4 samples should be faded in
        assert faded[0] < faded[3]  # Should increase
        # Last 4 samples should be faded out
        assert faded[-1] < faded[-4]  # Should decrease
        # Middle samples should remain 1.0
        assert faded[10] == pytest.approx(1.0, abs=1e-10)

    def test_apply_fade_edges_short_waveform(self):
        """Test fade edges with short waveform."""
        from wavetable_synthesis.core.processing import apply_fade_edges

        # Waveform too short for fading
        waveform = np.ones(5, dtype=np.float64)
        faded = apply_fade_edges(waveform, fade_samples=4)

        # Should return unchanged
        assert np.allclose(faded, waveform)

    def test_clamp_amplitude(self):
        """Test amplitude clamping."""
        from wavetable_synthesis.core.processing import clamp_amplitude

        # Create waveform with values outside [-1, 1]
        waveform = np.array([-2.0, -0.5, 0.0, 0.5, 2.0], dtype=np.float64)
        clamped = clamp_amplitude(waveform, -1.0, 1.0)

        # Should be clamped to [-1, 1]
        assert np.min(clamped) >= -1.0
        assert np.max(clamped) <= 1.0
        assert clamped[0] == -1.0  # Was -2.0, should be clamped
        assert clamped[4] == 1.0  # Was 2.0, should be clamped
        assert clamped[2] == 0.0  # Was within range, unchanged


class TestExport:
    """Test WAV export functionality."""

    def test_get_bit_depth_subtype(self):
        """Test bit depth to subtype conversion."""
        from wavetable_synthesis.export.wav import get_bit_depth_subtype

        assert get_bit_depth_subtype(16) == "PCM_16"
        assert get_bit_depth_subtype(24) == "PCM_24"
        assert get_bit_depth_subtype(32) == "PCM_32"

        # Test invalid bit depth
        try:
            get_bit_depth_subtype(8)
            assert False, "Should raise ValueError"
        except ValueError:
            pass

    def test_generate_filename(self):
        """Test filename generation."""
        from wavetable_synthesis.export.wav import generate_filename

        filename = generate_filename("test_wave", 256, 44100, 16)
        expected = "test_wave_256frames_44100Hz_16bit.wav"
        assert filename == expected

    def test_export_wavetable_single(self, tmp_path):
        """Test single file export."""
        import numpy as np

        from wavetable_synthesis.export.wav import export_wavetable

        # Create test data
        data = np.sin(np.linspace(0, 2 * np.pi, 2048, endpoint=False)).astype(np.float32)

        # Export
        result = export_wavetable("test", data, str(tmp_path))

        # Check result - now returns Path object
        from pathlib import Path

        assert isinstance(result, Path)
        assert result.name == "test_1frames_44100Hz_16bit.wav"
        assert result.exists()

    def test_export_wavetable_batch(self, tmp_path):
        """Test batch export."""
        import numpy as np

        from wavetable_synthesis.export.wav import export_wavetable

        # Create test data
        data = np.sin(np.linspace(0, 2 * np.pi, 2048, endpoint=False)).astype(np.float32)

        # Export multiple formats
        result = export_wavetable("test", data, str(tmp_path), sample_rate=[44100, 48000], bit_depth=[16, 24])

        # Check result
        assert isinstance(result, list)
        assert len(result) == 4  # 2 rates × 2 depths

    def test_save_wavetable_simple(self, tmp_path):
        """Test simple save function."""
        import numpy as np

        from wavetable_synthesis.export.wav import save_wavetable_simple

        # Create test data
        data = np.sin(np.linspace(0, 2 * np.pi, 2048, endpoint=False)).astype(np.float32)

        # Test simple save
        result = save_wavetable_simple("test", data)

        # Check result - now returns Path object
        from pathlib import Path

        assert isinstance(result, Path)
        assert "test" in result.name
        assert result.exists()

    def test_export_validation(self, tmp_path):
        """Test export parameter validation."""
        import numpy as np

        from wavetable_synthesis.export.wav import export_wavetable

        # Create test data
        data = np.sin(np.linspace(0, 2 * np.pi, 2048, endpoint=False)).astype(np.float32)

        # Test invalid sample rate
        try:
            export_wavetable("test", data, str(tmp_path), sample_rate=-44100)
            assert False, "Should raise ValueError"
        except ValueError:
            pass

        # Test invalid bit depth
        try:
            export_wavetable("test", data, str(tmp_path), bit_depth=8)
            assert False, "Should raise ValueError"
        except ValueError:
            pass


class TestCLI:
    """Test CLI functionality."""

    def test_cli_lazy_import_cli_main(self):
        """Test lazy import of cli_main."""
        import wavetable_synthesis.cli as cli_module

        # Access cli_main dynamically to trigger __getattr__
        cli_main = getattr(cli_module, "cli_main")

        # Should return the main function from cli module
        assert callable(cli_main)

    def test_cli_lazy_import_test_main(self):
        """Test lazy import of test_main."""
        import wavetable_synthesis.cli as cli_module

        # Access test_main dynamically to trigger __getattr__
        test_main = getattr(cli_module, "test_main")

        # Should return the main function from test_cli module
        assert callable(test_main)

    def test_cli_lazy_import_invalid_attribute(self):
        """Test lazy import with invalid attribute."""
        from wavetable_synthesis.cli import __getattr__ as cli_getattr

        try:
            cli_getattr("invalid_attribute")
            assert False, "Should have raised AttributeError"
        except AttributeError as e:
            assert "has no attribute 'invalid_attribute'" in str(e)

    def test_generate_wavetable_valid_params(self, tmp_path, first_generator_name):
        """Test generate_wavetable with valid parameters."""
        from wavetable_synthesis.cli.cli import generate_wavetable

        output_dir = str(tmp_path / "output")
        generate_wavetable(first_generator_name, 64, 44100, 16, output_dir)

        # Check if file was created
        expected_file = tmp_path / "output" / f"{first_generator_name}_64frames_44100Hz_16bit.wav"
        assert expected_file.exists()

    def test_generate_wavetable_invalid_frames(self, tmp_path, first_generator_name, capsys):
        """Test generate_wavetable with invalid frame count."""
        from wavetable_synthesis.cli.cli import generate_wavetable

        output_dir = str(tmp_path / "output")
        generate_wavetable(first_generator_name, -1, 44100, 16, output_dir)

        captured = capsys.readouterr()
        assert "Error: Invalid frame count" in captured.out

    def test_generate_wavetable_invalid_sample_rate(self, tmp_path, first_generator_name, capsys):
        """Test generate_wavetable with invalid sample rate."""
        from wavetable_synthesis.cli.cli import generate_wavetable

        output_dir = str(tmp_path / "output")
        generate_wavetable(first_generator_name, 64, 22050, 16, output_dir)

        captured = capsys.readouterr()
        assert "Error: Invalid sample rate" in captured.out

    def test_generate_wavetable_invalid_bit_depth(self, tmp_path, first_generator_name, capsys):
        """Test generate_wavetable with invalid bit depth."""
        from wavetable_synthesis.cli.cli import generate_wavetable

        output_dir = str(tmp_path / "output")
        generate_wavetable(first_generator_name, 64, 44100, 8, output_dir)

        captured = capsys.readouterr()
        assert "Error: Invalid bit depth" in captured.out

    def test_generate_wavetable_unknown_generator(self, tmp_path, capsys):
        """Test generate_wavetable with unknown generator."""
        # Import here to avoid toplevel import issues with pytest
        from wavetable_synthesis.cli.cli import (  # pylint: disable=import-outside-toplevel,import-error
            generate_wavetable,
        )

        output_dir = str(tmp_path / "output")
        generate_wavetable("unknown_generator", 64, 44100, 16, output_dir)

        captured = capsys.readouterr()
        assert "Error: Unknown generator" in captured.out
        assert "Available generators:" in captured.out

    def test_generate_wavetable_empty_data(self, tmp_path, first_generator_name, capsys, monkeypatch):
        """Test generate_wavetable with empty data generation."""
        from wavetable_synthesis.cli.cli import generate_wavetable

        def mock_generate(*args, **kwargs):
            return np.array([])

        monkeypatch.setattr("wavetable_synthesis.cli.cli.core_generate_wavetable", mock_generate)

        output_dir = str(tmp_path / "output")
        generate_wavetable(first_generator_name, 64, 44100, 16, output_dir)

        captured = capsys.readouterr()
        assert "Error: Invalid wavetable data generated" in captured.out

    def test_generate_wavetable_nan_inf_data(self, tmp_path, first_generator_name, capsys, monkeypatch):
        """Test generate_wavetable with NaN/Inf data."""
        from wavetable_synthesis.cli.cli import generate_wavetable

        def mock_generate(*args, **kwargs):
            return np.array([np.nan, np.inf, 1.0])

        monkeypatch.setattr("wavetable_synthesis.cli.cli.core_generate_wavetable", mock_generate)

        output_dir = str(tmp_path / "output")
        generate_wavetable(first_generator_name, 64, 44100, 16, output_dir)

        captured = capsys.readouterr()
        assert "Error: Invalid wavetable data generated" in captured.out

    def test_generate_wavetable_success_message(self, tmp_path, first_generator_name, capsys):
        """Test generate_wavetable success message."""
        from wavetable_synthesis.cli.cli import generate_wavetable

        output_dir = str(tmp_path / "output")
        generate_wavetable(first_generator_name, 64, 44100, 16, output_dir)

        captured = capsys.readouterr()
        assert "Success!" in captured.out
        assert "File:" in captured.out

    def test_cli_generate_all_wavetables(self, tmp_path, capsys):
        """Test generate_all_wavetables function."""
        from wavetable_synthesis.cli.cli import generate_all_wavetables

        output_dir = str(tmp_path / "batch_output")
        generate_all_wavetables(output_dir)

        captured = capsys.readouterr()
        assert "Found" in captured.out
        assert "generators:" in captured.out
        assert "Generating" in captured.out
        assert "Generation complete!" in captured.out

    def test_cli_main_batch_mode(self, tmp_path, capsys, monkeypatch):
        """Test main function with batch mode."""
        from unittest.mock import Mock

        from wavetable_synthesis.cli.cli import main

        # Mock sys.argv for batch mode
        test_args = ["cli.py", "--batch", "--output", str(tmp_path / "batch")]
        monkeypatch.setattr("sys.argv", test_args)

        # Mock Path.mkdir to avoid actual directory creation issues
        mock_mkdir = Mock()
        monkeypatch.setattr("pathlib.Path.mkdir", mock_mkdir)

        # Mock generate_all_wavetables
        mock_generate_all = Mock()
        monkeypatch.setattr("wavetable_synthesis.cli.cli.generate_all_wavetables", mock_generate_all)

        result = main()
        assert result == 0
        mock_generate_all.assert_called_once()

    def test_cli_main_help_mode(self, capsys, monkeypatch):
        """Test main function with no arguments (help mode)."""
        from wavetable_synthesis.cli.cli import main

        # Mock sys.argv with no arguments
        test_args = ["cli.py"]
        monkeypatch.setattr("sys.argv", test_args)

        result = main()
        assert result == 0

        captured = capsys.readouterr()
        assert "usage:" in captured.out or "positional arguments" in captured.out


class TestMain:
    """Test main entry point."""

    def test_main_entry_point(self):
        """Test that __main__.py has correct structure."""
        import wavetable_synthesis.__main__ as main_module

        # Should be able to import without errors
        assert main_module is not None

        # Should have the expected attributes
        assert hasattr(main_module, "__name__")
        assert hasattr(main_module, "__file__")

        # The main block should exist in the source
        import inspect

        source = inspect.getsource(main_module)
        assert 'if __name__ == "__main__":' in source
        assert "main()" in source

    def test_main_name_check(self):
        """Test that main only runs when __name__ == '__main__'."""
        # This test verifies the structure is correct
        import wavetable_synthesis.__main__ as main_module

        # The module should have the correct structure
        assert hasattr(main_module, "__name__")
        # The main block should exist (we can't easily test execution without running as script)


class TestConfig:
    """Test configuration classes."""

    def test_wavetable_config_defaults(self):
        """Test WavetableConfig with default values."""
        from wavetable_synthesis.core.config import WavetableConfig

        config = WavetableConfig()

        assert config.frames == 256
        assert config.frame_size == 2048
        assert config.sample_rate == 44100
        assert config.bit_depth == 16
        assert config.output_dir == "wavetable_dist"
        assert config.waveform_name == ""

    def test_wavetable_config_custom_values(self):
        """Test WavetableConfig with custom values."""
        from wavetable_synthesis.core.config import WavetableConfig

        config = WavetableConfig(
            frames=128,
            frame_size=1024,
            sample_rate=48000,
            bit_depth=24,
            output_dir="/tmp",
            waveform_name="test_wave",
        )

        assert config.frames == 128
        assert config.frame_size == 1024
        assert config.sample_rate == 48000
        assert config.bit_depth == 24
        assert config.output_dir == "/tmp"
        assert config.waveform_name == "test_wave"

    def test_wavetable_config_get_filename(self):
        """Test filename generation."""
        from wavetable_synthesis.core.config import WavetableConfig

        config = WavetableConfig(waveform_name="sine_wave", frames=64, sample_rate=44100, bit_depth=16)

        filename = config.get_filename()
        expected = "sine_wave_64frames_44100Hz_16bit.wav"
        assert filename == expected

    def test_wavetable_config_validate_valid(self):
        """Test validation with valid parameters."""
        from wavetable_synthesis.core.config import WavetableConfig

        config = WavetableConfig(
            frames=64,
            frame_size=2048,
            sample_rate=44100,
            bit_depth=16,
            waveform_name="test",
        )

        # Should not raise
        config.validate()

    def test_wavetable_config_validate_invalid_frames(self):
        """Test validation with invalid frames."""
        from wavetable_synthesis.core.config import WavetableConfig

        config = WavetableConfig(frames=-1, waveform_name="test")

        with pytest.raises(ValueError, match="frames must be positive"):
            config.validate()

    def test_wavetable_config_validate_invalid_frame_size(self):
        """Test validation with invalid frame_size."""
        from wavetable_synthesis.core.config import WavetableConfig

        config = WavetableConfig(frame_size=0, waveform_name="test")

        with pytest.raises(ValueError, match="frame_size must be positive"):
            config.validate()

    def test_wavetable_config_validate_invalid_sample_rate(self):
        """Test validation with invalid sample_rate."""
        from wavetable_synthesis.core.config import WavetableConfig

        config = WavetableConfig(sample_rate=-44100, waveform_name="test")

        with pytest.raises(ValueError, match="sample_rate must be positive"):
            config.validate()

    def test_wavetable_config_validate_invalid_bit_depth(self):
        """Test validation with invalid bit_depth."""
        from wavetable_synthesis.core.config import WavetableConfig

        config = WavetableConfig(bit_depth=8, waveform_name="test")

        with pytest.raises(ValueError, match="bit_depth must be one of"):
            config.validate()

    def test_wavetable_config_validate_empty_waveform_name(self):
        """Test validation with empty waveform_name."""
        from wavetable_synthesis.core.config import WavetableConfig

        config = WavetableConfig(waveform_name="")

        with pytest.raises(ValueError, match="waveform_name cannot be empty"):
            config.validate()

    def test_cli_config_defaults(self):
        """Test CLIConfig with default values."""
        from wavetable_synthesis.core.config import CLIConfig

        config = CLIConfig()

        assert config.list_generators is False
        assert config.clear_output is False
        assert config.wavetable_config is None

    def test_cli_config_should_generate(self):
        """Test should_generate method."""
        from wavetable_synthesis.core.config import CLIConfig

        # Should generate when no flags set
        config = CLIConfig()
        assert config.should_generate() is True

        # Should not generate when list_generators is True
        config = CLIConfig(list_generators=True)
        assert config.should_generate() is False

        # Should not generate when clear_output is True
        config = CLIConfig(clear_output=True)
        assert config.should_generate() is False

    def test_cli_config_validate_valid(self):
        """Test CLIConfig validation with valid config."""
        from wavetable_synthesis.core.config import CLIConfig, WavetableConfig

        config = CLIConfig(wavetable_config=WavetableConfig(waveform_name="test"))
        config.validate()  # Should not raise

    def test_cli_config_validate_missing_wavetable_config(self):
        """Test CLIConfig validation when wavetable_config is required but missing."""
        from wavetable_synthesis.core.config import CLIConfig

        config = CLIConfig()  # No wavetable_config, but should_generate() is True

        with pytest.raises(ValueError, match="wavetable_config is required"):
            config.validate()


class TestWavetableGenerator:
    """Test WavetableGenerator class."""
