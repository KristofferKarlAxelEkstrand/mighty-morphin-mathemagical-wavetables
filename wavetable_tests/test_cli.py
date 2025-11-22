"""
Test CLI functionality for wavetable generation.

This module tests the command-line interface including argument parsing,
generator listing, validation, and wavetable generation.
"""

import sys
from unittest.mock import patch

import pytest

from wavetable_synthesis.cli.cli import (
    create_parser,
    main,
    show_available_generators,
    validate_generators,
)


class TestCLIParser:
    """Test command-line argument parser."""

    def test_create_parser_default_values(self):
        """Test parser creates with expected default values."""
        parser = create_parser()
        args = parser.parse_args([])

        assert args.waveform is None
        assert args.frames == 256
        assert args.rate == 44100
        assert args.bits == 16
        assert args.output == "./wavetable_dist"
        assert args.list is False
        assert args.validate is False
        assert args.batch is False

    def test_create_parser_with_waveform(self):
        """Test parser accepts waveform argument."""
        parser = create_parser()
        args = parser.parse_args(["example"])

        assert args.waveform == "example"

    def test_create_parser_with_custom_frames(self):
        """Test parser accepts custom frame count."""
        parser = create_parser()
        args = parser.parse_args(["--frames", "512"])

        assert args.frames == 512

    def test_create_parser_with_custom_rate(self):
        """Test parser accepts custom sample rate."""
        parser = create_parser()
        args = parser.parse_args(["--rate", "96000"])

        assert args.rate == 96000

    def test_create_parser_with_custom_bits(self):
        """Test parser accepts custom bit depth."""
        parser = create_parser()
        args = parser.parse_args(["--bits", "32"])

        assert args.bits == 32

    def test_create_parser_with_custom_output(self):
        """Test parser accepts custom output directory."""
        parser = create_parser()
        args = parser.parse_args(["--output", "/tmp/test"])

        assert args.output == "/tmp/test"

    def test_create_parser_list_flag(self):
        """Test parser accepts list flag."""
        parser = create_parser()
        args = parser.parse_args(["--list"])

        assert args.list is True

    def test_create_parser_validate_flag(self):
        """Test parser accepts validate flag."""
        parser = create_parser()
        args = parser.parse_args(["--validate"])

        assert args.validate is True

    def test_create_parser_batch_flag(self):
        """Test parser accepts batch flag."""
        parser = create_parser()
        args = parser.parse_args(["--batch"])

        assert args.batch is True


class TestShowAvailableGenerators:
    """Test show_available_generators function."""

    def test_show_available_generators_output(self, capsys):
        """Test that show_available_generators prints expected output."""
        show_available_generators()
        captured = capsys.readouterr()

        assert "Available Wavetable Generators:" in captured.out
        assert "example" in captured.out
        assert "Total:" in captured.out


class TestValidateGenerators:
    """Test validate_generators function."""

    def test_validate_generators_runs(self, capsys):
        """Test that validate_generators runs without errors."""
        result = validate_generators()
        captured = capsys.readouterr()

        assert isinstance(result, bool)
        assert "Validating" in captured.out or "✓" in captured.out


class TestCLIMain:
    """Test main CLI function."""

    def test_main_list_command(self, capsys):
        """Test main with --list flag."""
        with patch.object(sys, "argv", ["wavetable", "--list"]):
            main()

        captured = capsys.readouterr()
        assert "Available Wavetable Generators:" in captured.out

    def test_main_validate_command(self, capsys):
        """Test main with --validate flag."""
        with patch.object(sys, "argv", ["wavetable", "--validate"]):
            # Don't expect SystemExit for validate
            main()

        captured = capsys.readouterr()
        assert "Validating" in captured.out or "✓" in captured.out

    def test_main_no_args_shows_help(self, capsys):
        """Test main with no arguments shows help."""
        with patch.object(sys, "argv", ["wavetable"]):
            main()

        captured = capsys.readouterr()
        # Should show usage/help information
        assert "usage:" in captured.out or "help" in captured.out

    def test_main_unknown_generator(self, capsys):
        """Test main with unknown generator name."""
        with patch.object(sys, "argv", ["wavetable", "nonexistent_generator"]):
            main()

        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "unknown" in captured.out.lower()

    def test_main_generate_wavetable(self, tmp_path, capsys):
        """Test main generates a wavetable file."""
        output_dir = tmp_path / "output"

        with patch.object(sys, "argv", ["wavetable", "example", "--frames", "32", "--output", str(output_dir)]):
            main()

        captured = capsys.readouterr()
        assert "Success" in captured.out or "Saved" in captured.out

        # Check that output file was created
        wav_files = list(output_dir.glob("*.wav"))
        assert len(wav_files) == 1
        assert wav_files[0].name.startswith("example_")
        assert wav_files[0].stat().st_size > 0

    def test_main_generate_with_custom_params(self, tmp_path):
        """Test main with custom parameters."""
        output_dir = tmp_path / "custom"

        with patch.object(
            sys,
            "argv",
            [
                "wavetable",
                "example",
                "--frames",
                "64",
                "--rate",
                "48000",
                "--bits",
                "24",
                "--output",
                str(output_dir),
            ],
        ):
            main()

        wav_files = list(output_dir.glob("*.wav"))
        assert len(wav_files) == 1
        # Check filename contains custom parameters
        filename = wav_files[0].name
        assert "64frames" in filename
        assert "48000Hz" in filename
        assert "24bit" in filename


class TestCLIEdgeCases:
    """Test CLI edge cases and error handling."""

    def test_invalid_sample_rate(self):
        """Test that invalid sample rate is rejected by parser."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["--rate", "99999"])

    def test_invalid_bit_depth(self):
        """Test that invalid bit depth is rejected by parser."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["--bits", "99"])

    def test_negative_frames(self, capsys):
        """Test that negative frame count is handled."""
        # Negative frame count should be rejected
        with patch.object(sys, "argv", ["wavetable", "example", "--frames", "-1"]):
            main()

        captured = capsys.readouterr()
        # Should show an error message
        assert "error" in captured.out.lower() or "invalid" in captured.out.lower()


class TestCLIIntegration:
    """Integration tests for CLI functionality."""

    def test_list_contains_all_generators(self, capsys):
        """Test that list command shows all registered generators."""
        show_available_generators()
        captured = capsys.readouterr()

        # Check for known generators
        assert "example" in captured.out
        assert "sine_to_triangle" in captured.out
        assert "square_pwm_tz" in captured.out
        assert "linear_interpolation" in captured.out

    def test_validate_checks_all_generators(self, capsys):
        """Test that validate command checks all generators."""
        result = validate_generators()
        captured = capsys.readouterr()

        # Should validate all known generators
        assert "example" in captured.out
        assert "sine_to_triangle" in captured.out
        assert isinstance(result, bool)

    def test_generate_multiple_generators(self, tmp_path):
        """Test generating wavetables from multiple generators."""
        output_dir = tmp_path / "multi"

        generators = ["example", "sine_to_triangle"]

        for gen_name in generators:
            with patch.object(
                sys,
                "argv",
                ["wavetable", gen_name, "--frames", "32", "--output", str(output_dir)],
            ):
                main()

        wav_files = list(output_dir.glob("*.wav"))
        assert len(wav_files) == len(generators)
