#!/usr/bin/env python3
"""
Test Runner CLI

Run the wavetable synthesis test suite.
"""

import subprocess
import sys
from typing import Any

pytest: Any = None

try:
    import pytest
except ImportError:
    pass


def run_tests() -> int:
    """Run the test suite with pytest."""
    print("Running wavetable synthesis tests...")
    print("=" * 45)

    if pytest is None:
        print("❌ pytest not found. Install with: pip install pytest")
        return 1

    # Run pytest with coverage
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "wavetable_tests/",
        "-v",
        "--tb=short",
        "--cov=wavetable_synthesis",
        "--cov-report=term-missing",
    ]

    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        return 130
    except (subprocess.SubprocessError, OSError) as e:
        print(f"Error running tests: {e}")
        return 1


def main() -> int:
    """Main entry point."""
    return run_tests()


if __name__ == "__main__":
    sys.exit(main())
