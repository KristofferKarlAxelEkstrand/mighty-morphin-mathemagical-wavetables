"""Load generator modules from the repo `maths/` folder.

`maths/` is a folder of formula files, not a Python package. It has no `__init__.py`.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


class _LoadState:
    loaded: bool = False


def repo_root() -> Path:
    """Return the repository root (parent of `generator/`)."""
    return Path(__file__).resolve().parents[3]


def maths_dir() -> Path:
    """Return the folder that holds generator `.py` files.

    Prefers the checkout path `<repo>/maths`. Falls back to
    `wavetable_synthesis/maths` if the library was installed without the repo
    layout.
    """
    checkout = repo_root() / "maths"
    if checkout.is_dir():
        return checkout
    return Path(__file__).resolve().parents[1] / "maths"


def maths_module_paths() -> list[Path]:
    """Return generator files in `maths/`, skipping names that start with `_`."""
    folder = maths_dir()
    if not folder.is_dir():
        return []
    return sorted(path for path in folder.glob("*.py") if not path.name.startswith("_"))


def load_maths_generators() -> None:
    """Import each `maths/*.py` file so `@register_generator` runs.

    Safe to call more than once. The second call is a no-op until
    `reset_maths_load_state()` runs.
    """
    if _LoadState.loaded:
        return
    for path in maths_module_paths():
        _import_file(path)
    _LoadState.loaded = True


def reset_maths_load_state() -> None:
    """Forget loaded `maths.*` modules so the next load re-imports them."""
    _LoadState.loaded = False
    stale = [name for name in sys.modules if name == "maths" or name.startswith("maths.")]
    for name in stale:
        del sys.modules[name]


def _import_file(path: Path) -> None:
    module_name = f"maths.{path.stem}"
    if module_name in sys.modules:
        return
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        message = f"Could not load generator file: {path}"
        raise ImportError(message)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
