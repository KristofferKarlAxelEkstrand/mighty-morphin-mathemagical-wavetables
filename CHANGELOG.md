# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive code quality improvements (flake8, pylint, mypy)
- Complete Dependabot configuration for Python, npm, and GitHub Actions
- CHANGELOG.md file for tracking project changes
- Fixed repository URLs in pyproject.toml

### Fixed
- Code formatting issues (trailing whitespace)
- Unnecessary f-strings without placeholders
- Dependabot configuration was incomplete

## [0.1.0] - Initial Release

### Added
- Core wavetable synthesis engine
- Command-line interface for wavetable generation
- Four example generators:
  - `example` - Sine to sawtooth morphing
  - `linear_interpolation` - Linear interpolation morphing
  - `sine_to_triangle` - Sine to triangle wave morphing
  - `square_pwm_tz` - Through-zero PWM square wave
- Comprehensive test suite (99 tests, 78% coverage)
- Full type hint support with strict mypy checking
- Professional audio processing (normalization, DC removal)
- WAV file export with configurable bit depth (16/24/32-bit)
- Configurable sample rates (44100, 48000, 96000 Hz)
- Decorator-based generator registration system
- Extensive documentation:
  - README.md with quick start guide
  - QUICKSTART.md for new users
  - CONTRIBUTING.md for contributors
  - Technical documentation in docs/ directory
  - Mathematical concepts guide (radians, pi, phase, frequency)
- Pre-commit hooks with Husky
- Development tooling:
  - Black code formatting
  - isort import sorting
  - MyPy type checking
  - Pylint code quality
  - Flake8 PEP 8 compliance
  - pytest with coverage reporting
- Virtual environment setup script
- Educational and collaborative focus

### Project Goals
- Provide simple way to create expressive wavetables using mathematics
- Help learners understand math concepts (radians, π, sine, cosine)
- Offer approachable Python project for first-time open-source contributors
- Generate professional-quality wavetables for modern synthesizers

[Unreleased]: https://github.com/KristofferKarlAxelEkstrand/mighty-morphin-mathemagical-wavetables/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/KristofferKarlAxelEkstrand/mighty-morphin-mathemagical-wavetables/releases/tag/v0.1.0
