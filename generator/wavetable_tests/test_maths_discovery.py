"""Discovery of formula files in maths/."""

from pathlib import Path

from wavetable_synthesis.core.discover import maths_dir, maths_module_paths
from wavetable_synthesis.core.registry import get_registry

EXPECTED_GENERATORS = {
    "example",
    "linear_interpolation",
    "sine_to_triangle",
    "square_pwm_tz",
}


def test_maths_is_not_a_package() -> None:
    """maths/ must stay a folder of files, not a Python package."""
    assert not (maths_dir() / "__init__.py").exists()


def test_maths_dir_is_repo_maths() -> None:
    folder = maths_dir()
    repo = Path(__file__).resolve().parents[2]
    assert folder == repo / "maths"
    assert folder.is_dir()


def test_maths_module_paths_are_formula_files() -> None:
    names = {path.stem for path in maths_module_paths()}
    assert names >= EXPECTED_GENERATORS
    assert all(not path.name.startswith("_") for path in maths_module_paths())


def test_registry_loads_every_maths_generator() -> None:
    registry = get_registry(verbose=False)
    assert set(registry) >= EXPECTED_GENERATORS


def test_repo_has_no_wavetable_generators_package() -> None:
    repo = Path(__file__).resolve().parents[2]
    assert not (repo / "wavetable_generators").exists()
