# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Git hook is husky (`npm install`). Setup and the devcontainer no longer run
  `pre-commit install`. That command overwrites the husky hook.
- Wave formulas live in `maths/` at the repo root. That folder is not a package. The engine
  loads each `.py` file automatically. The old `wavetable_generators/` package is gone.
- The library and tests live under `generator/`. Import names stay `wavetable_synthesis`.
  Run tests with `pytest generator/wavetable_tests/`.
- Technical notes live in `docs/tech/`. The old `docs_tech/` folder is gone.
- Generated WAV files go in `maths_generated/`. The old `wavetable_dist/` name is gone.

### Added - Modern Development Tooling

- **Ruff** - Ultra-fast Python linter and formatter
- 10-100x faster than traditional tools
- Auto-fixes most code quality issues
- Comprehensive configuration in pyproject.toml
- **Git hooks** (husky + lint-staged)
- Automated Ruff, Prettier, and markdownlint checks on commit
- **Make task runner** (Makefile)
- Simple commands for common development tasks
- `make help`, `make test`, `make lint`, `make format`, etc.
- **Development container** (.devcontainer/)
- Ready-to-use VS Code/GitHub Codespaces environment
- Zero setup required
- **.python-version file**
- Python 3.10 specification for version managers

### Changed

- Simplified development workflow - removed duplicate tools
- Removed legacy linting tools (Black, isort, Flake8, Pylint) - now using Ruff only
- Streamlined documentation - one clear development guide
- Updated package.json scripts to use Ruff
- Enhanced setup.sh for better cross-platform support
- Updated .gitignore to allow .python-version file

### Removed

- Unused extras: Flask (`web`) and Sphinx (`docs`)
- Stale files: `auto_activate.sh`, `PIP.MD`, `docs/uv-guide.md`,
  `CI_OPTIMIZATION.md`, `docs/tech/python.md`
- `pre-commit` Python extra (husky is the hook)
- Legacy linting dependencies (Black, isort, Flake8, Pylint)
- Duplicate task runner (justfile) - kept Makefile only
- Redundant documentation files

### Developer Experience

- **Streamlined**: One modern way to work, not multiple options
- **Fast**: 10-100x faster linting and formatting
- **Simple**: Clear, consistent workflow via Make
- **Automated**: Pre-commit hooks catch issues early

### Added - Code Quality

- Complete Dependabot configuration for Python, npm, and GitHub Actions
- CHANGELOG.md file for tracking project changes

### Fixed

- Fixed repository URLs in pyproject.toml
- Code formatting issues (trailing whitespace)
- Unnecessary f-strings without placeholders

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
