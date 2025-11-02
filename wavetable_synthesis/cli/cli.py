#!/usr/bin/env python3
"""Wavetable Generator CLI

Generate wavetables for modern synthesizers.
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Optional

import numpy as np

from ..core import generate_wavetable as core_generate_wavetable
from ..core.registry import get_registry
from ..export.wav import save_wavetable

# Configuration
DEFAULT_FRAMES = 256
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_BIT_DEPTH = 16
DEFAULT_OUTPUT_DIR = "./wavetable_dist"
FRAME_SIZE = 2048
VALIDATION_SAMPLE_SIZE = 128  # Sample size for generator validation testing

VALID_SAMPLE_RATES = [44100, 48000, 96000]
VALID_BIT_DEPTHS = [16, 24, 32]


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate wavetables for synthesizers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  wavetable sine_to_triangle          # Generate sine-to-triangle morph
  wavetable square_pwm_tz             # Generate square with PWM
  wavetable --list                    # Show available generators
  wavetable --validate                # Validate all registered generators
  wavetable --batch                   # Generate ALL wavetables with all configs
        """,
    )

    parser.add_argument("waveform", nargs="?", help="Generator name")
    parser.add_argument("--list", "-l", action="store_true", help="List available generators")
    parser.add_argument(
        "--validate",
        "-v",
        action="store_true",
        help="Validate all registered generators",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Generate all wavetables with all configurations",
    )
    parser.add_argument(
        "--frames",
        "-f",
        type=int,
        default=DEFAULT_FRAMES,
        help=f"Number of frames (default: {DEFAULT_FRAMES})",
    )
    parser.add_argument(
        "--rate",
        "-r",
        type=int,
        default=DEFAULT_SAMPLE_RATE,
        choices=VALID_SAMPLE_RATES,
        help=f"Sample rate (default: {DEFAULT_SAMPLE_RATE})",
    )
    parser.add_argument(
        "--bits",
        "-b",
        type=int,
        default=DEFAULT_BIT_DEPTH,
        choices=VALID_BIT_DEPTHS,
        help=f"Bit depth (default: {DEFAULT_BIT_DEPTH})",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )

    return parser


def show_available_generators() -> None:
    """Display available generators."""
    registry = get_registry(verbose=False)

    print("Available Wavetable Generators:")
    print("=" * 40)

    for name in sorted(registry.keys()):
        generator = registry[name]
        doc = generator.__doc__.strip().split("\n")[0] if generator.__doc__ else "No description"
        print(f"  {name:<20} - {doc}")

    print(f"\nTotal: {len(registry)} generators")


def validate_generators() -> bool:
    """Validate all registered generators.
    
    Checks that each generator:
    - Has valid metadata (get_info)
    - Has required methods (generate, get_processing, get_info)
    - Can be called with test parameters
    
    Returns:
        True if all generators are valid, False otherwise
    """
    from ..core.base_generator import BaseGenerator
    from ..core.constants import TAU
    
    registry = get_registry(verbose=False)
    generators = sorted(registry.keys())
    
    print("Validating Registered Generators")
    print("=" * 50)
    print(f"Found {len(generators)} generators to validate\n")
    
    all_valid = True
    theta = TAU * np.arange(VALIDATION_SAMPLE_SIZE, dtype=np.float64) / VALIDATION_SAMPLE_SIZE  # Test phase array
    
    for name in generators:
        print(f"Validating: {name}")
        generator = registry[name]
        has_errors = False
        
        # Check required methods
        required_methods = ["generate", "get_processing", "get_info"]
        for method in required_methods:
            if not hasattr(generator, method):
                print(f"  ✗ Missing method: {method}")
                has_errors = True
                all_valid = False
        
        # Validate metadata
        if hasattr(generator, "get_info"):
            try:
                info = generator.get_info()
                BaseGenerator.validate_info(info)
                print(f"  ✓ Metadata valid")
            except ValueError as e:
                print(f"  ✗ Invalid metadata: {e}")
                has_errors = True
                all_valid = False
        
        # Test generation with sample parameters
        if hasattr(generator, "generate"):
            try:
                # Test with u=0.0
                result = generator.generate(theta, 0.0)
                if not isinstance(result, np.ndarray):
                    print(f"  ✗ generate() must return numpy array, got {type(result)}")
                    has_errors = True
                    all_valid = False
                elif len(result) != len(theta):
                    print(f"  ✗ generate() returned wrong length: {len(result)} vs {len(theta)}")
                    has_errors = True
                    all_valid = False
                else:
                    # Test with u=0.5
                    generator.generate(theta, 0.5)
                    # Test with u=1.0
                    generator.generate(theta, 1.0)
                    print(f"  ✓ Generate function works")
            # Broad except is intentional here - we want to catch all generator errors
            # for validation purposes and report them in a user-friendly way
            except Exception as e:  # pylint: disable=broad-except
                print(f"  ✗ Generation failed ({type(e).__name__}): {e}")
                has_errors = True
                all_valid = False
        
        if not has_errors:
            print(f"  ✓ {name} is valid\n")
        else:
            print()
    
    print("=" * 50)
    if all_valid:
        print("✓ All generators are valid!")
    else:
        print("✗ Some generators have errors")
    print("=" * 50)
    
    return all_valid


def get_generator_function(waveform_name: str) -> Optional[Any]:
    """Get generator function from registry."""
    registry = get_registry(verbose=False)

    if waveform_name not in registry:
        available = sorted(registry.keys())
        print(f"Error: Unknown generator '{waveform_name}'")
        print("Available generators:")
        for name in available:
            print(f"  - {name}")
        return None

    return registry[waveform_name]


def generate_wavetable(waveform_name: str, frames: int, sample_rate: int, bit_depth: int, output_dir: str) -> None:
    """Generate and save a wavetable."""
    # Validation
    if frames <= 0:
        print(f"Error: Invalid frame count '{frames}'")
        return

    if sample_rate not in VALID_SAMPLE_RATES:
        print(f"Error: Invalid sample rate '{sample_rate}'")
        return

    if bit_depth not in VALID_BIT_DEPTHS:
        print(f"Error: Invalid bit depth '{bit_depth}'")
        return

    generator = get_generator_function(waveform_name)
    if generator is None:
        return

    # Setup output and validate directory
    output_path = Path(output_dir)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
        # Test if directory is writable by attempting to create a test file
        test_file = output_path / ".write_test"
        test_file.touch()
        test_file.unlink()
    except (OSError, PermissionError) as e:
        print(f"Error: Cannot create/access output directory '{output_dir}': {e}")
        return

    print(f"Generating {waveform_name} wavetable...")
    print(f"   Frames: {frames}, Rate: {sample_rate}Hz, Bits: {bit_depth}")

    try:
        # Generate wavetable
        data = core_generate_wavetable(generator, frames=frames, frame_size=FRAME_SIZE)

        # Validate data
        if len(data) == 0 or not np.all(np.isfinite(data)):
            print("Error: Invalid wavetable data generated")
            return

        # Save file (returns Path object)
        filepath = save_wavetable(
            waveform_name,
            data,
            output_dir=output_path,
            sample_rate=sample_rate,
            bit_depth=bit_depth,
        )

        print(f"Success! File: {filepath}")

    except (ValueError, OSError, IOError, RuntimeError) as e:
        print(f"Error: {e}")


def generate_all_wavetables(output_dir: str) -> None:
    """Generate all wavetables with multiple configurations.
    
    Generates wavetables for all registered generators with various
    configurations including different frame counts, sample rates, and bit depths.
    
    Args:
        output_dir: Directory to save generated wavetables
    """
    registry = get_registry(verbose=False)
    generators = sorted(registry.keys())
    print(f"Found {len(generators)} generators: {', '.join(generators)}")

    # Configuration combinations for batch generation
    frame_counts = [64, 128, 256, 512]
    sample_rates = [44100, 48000]
    bit_depths = [16, 24]

    total_combinations = len(generators) * len(frame_counts) * len(sample_rates) * len(bit_depths)
    print(f"Generating {total_combinations} wavetable combinations...")

    generated_count = 0
    current_item = 0

    for generator in generators:
        print(f"\n{'='*50}")
        print(f"Generating wavetables for: {generator}")
        print(f"{'='*50}")

        for frames in frame_counts:
            for sample_rate in sample_rates:
                for bit_depth in bit_depths:
                    progress_pct = ((current_item + 1) / total_combinations) * 100
                    print(
                        f"  [{current_item + 1}/{total_combinations}] ({progress_pct:.1f}%) "
                        f"{generator} - {frames} frames, {sample_rate}Hz, {bit_depth}bit"
                    )
                    current_item += 1

                    try:
                        generate_wavetable(generator, frames, sample_rate, bit_depth, output_dir)
                        generated_count += 1
                    except (ValueError, OSError, RuntimeError) as e:
                        print(f"    Error: {e}")

    print(f"\n{'='*50}")
    print(f"Generation complete! Generated {generated_count}/{total_combinations} wavetables")
    print(f"Output directory: {output_dir}")
    print(f"{'='*50}")


def main() -> int:
    """Main CLI entry point with comprehensive error handling."""
    try:
        parser = create_parser()
        args = parser.parse_args()

        exit_code = 0

        if args.list:
            show_available_generators()
        elif args.validate:
            if not validate_generators():
                exit_code = 1
        elif args.batch:
            # Create output directory
            try:
                Path(args.output).mkdir(parents=True, exist_ok=True)
            except (OSError, PermissionError) as e:
                print(f"Error: Cannot create output directory '{args.output}': {e}")
                return 1
            generate_all_wavetables(args.output)
        elif args.waveform:
            generate_wavetable(args.waveform, args.frames, args.rate, args.bits, args.output)
        else:
            parser.print_help()

        return exit_code

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 130  # Standard Unix exit code for SIGINT
    except Exception as e:  # pylint: disable=broad-except
        # Broad except is intentional for top-level CLI error handling
        # to provide user-friendly error messages for any unexpected errors
        print(f"\nUnexpected error ({type(e).__name__}): {e}")
        print("Please report this issue with the full error message.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
