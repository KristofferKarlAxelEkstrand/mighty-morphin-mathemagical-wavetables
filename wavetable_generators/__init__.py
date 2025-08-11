"""
MAWT Generator modules with decorator-based registration.

Import this module to register all generators automatically.
"""

# Automatically import all generators to trigger @register_generator decorators
import importlib
from pathlib import Path

_current_dir = Path(__file__).parent
for filepath in _current_dir.iterdir():
    if filepath.suffix == ".py" and filepath.name != "__init__.py":
        module_name = filepath.stem  # Get filename without extension
        importlib.import_module(f".{module_name}", package=__name__)
