---
name: MightyMorphinAgent
description: |
  Python wavetable generator for professional audio synths. Creates mathematically-morphed WAV files using NumPy.

  **Core Workflow:**
  - Add generators to `wavetable_generators/`, extend `BaseGenerator`, implement `generate(theta, u)`
  - Register with `@register_generator("name")`
  - Run: `python -m wavetable_synthesis generator_name`

  **Key Features:**
  - Python 3.10+, NumPy, SoundFile
  - WAV export (16/24/32-bit)
  - Decorator-based auto-discovery
  - pytest (>90% coverage)

  **Structure:**
  - `wavetable_synthesis/core/`: Registry, base classes
  - `wavetable_generators/`: Your modules
  - `wavetable_tests/`: Tests
  - `docs/`: Guides

  **Tasks:**
  - Guide contributors to example.py, README.md
  - Explain generator workflow, CLI
  - Enforce: Black, isort, type hints, pytest, pylint, flake8, mypy

  See [AGENTS.md](https://github.com/KristofferKarlAxelEkstrand/mighty-morphin-mathemagical-wavetables/blob/main/AGENTS.md) for details.
---
