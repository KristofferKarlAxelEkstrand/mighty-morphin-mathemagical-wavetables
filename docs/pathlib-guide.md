# Pathlib Usage Guide

This project uses Python's modern `pathlib.Path` for all file path operations. This guide explains how to work with Path objects throughout the codebase.

## Why Pathlib?

`pathlib.Path` is the modern, pythonic way to handle file paths since Python 3.4+:

- **Object-oriented**: Paths are objects with useful methods and properties
- **Cross-platform**: Automatically handles Windows vs Unix path differences
- **Readable**: Uses `/` operator instead of `os.path.join()`
- **Type-safe**: Better IDE autocomplete and type checking
- **Powerful**: Rich API for common path operations

## Quick Start

### Creating Paths

```python
from pathlib import Path

# From string
path = Path("wavetables/sine_wave.wav")

# From current file location
current_dir = Path(__file__).parent

# From home directory
home = Path.home()

# Using the / operator (most readable!)
output_dir = Path("wavetables")
filepath = output_dir / "sine_wave.wav"
```

### Common Path Operations

```python
from pathlib import Path

path = Path("wavetables/sine_to_triangle_256frames_44100Hz_16bit.wav")

# Get components
print(path.name)        # 'sine_to_triangle_256frames_44100Hz_16bit.wav'
print(path.stem)        # 'sine_to_triangle_256frames_44100Hz_16bit'
print(path.suffix)      # '.wav'
print(path.parent)      # PosixPath('wavetables')

# Check existence
if path.exists():
    print("File exists!")

if path.is_file():
    print("It's a file!")

if path.is_dir():
    print("It's a directory!")

# Create directories
path.parent.mkdir(parents=True, exist_ok=True)

# Iterate over directory
for file in path.parent.iterdir():
    if file.suffix == ".wav":
        print(f"Found WAV: {file.name}")

# Convert to string when needed
path_str = str(path)
```

## Using Path Objects in This Project

### Saving Wavetables

All export functions now return `Path` objects:

```python
from pathlib import Path
from wavetable_synthesis.export.wav import save_wavetable
import numpy as np

# Generate some test data
data = np.zeros(2048)

# Save wavetable - returns Path object
filepath = save_wavetable(
    name="my_wave",
    data=data,
    output_dir="./my_wavetables",  # Can pass string or Path
    sample_rate=44100,
    bit_depth=16
)

# filepath is a Path object!
print(type(filepath))  # <class 'pathlib.Path'>
print(filepath.name)   # 'my_wave_1frames_44100Hz_16bit.wav'
print(filepath.exists())  # True

# Convert to string if needed for legacy code
filepath_str = str(filepath)
```

### Working with Directories

```python
from pathlib import Path

# Create output directory
output_dir = Path("wavetables")
output_dir.mkdir(parents=True, exist_ok=True)

# Pass Path objects to functions
filepath = save_wavetable("sine", data, output_dir=output_dir)

# Check if directory is writable
try:
    test_file = output_dir / ".write_test"
    test_file.touch()
    test_file.unlink()
    print("Directory is writable")
except (OSError, PermissionError):
    print("Directory is not writable")
```

### Batch Export

When exporting multiple files, you get a list of Path objects:

```python
from wavetable_synthesis.export.wav import export_wavetable

# Export in multiple formats - returns List[Path]
paths = export_wavetable(
    name="my_wave",
    data=data,
    output_dir="./batch_output",
    sample_rate=[44100, 48000],
    bit_depth=[16, 24]
)

# Iterate over Path objects
for path in paths:
    print(f"Created: {path.name}")
    print(f"  Size: {path.stat().st_size} bytes")
    print(f"  Parent: {path.parent}")
```

### Generator Discovery

Our generator auto-discovery uses pathlib:

```python
from pathlib import Path
import importlib

# Get current directory
_current_dir = Path(__file__).parent

# Iterate over Python files
for filepath in _current_dir.iterdir():
    if filepath.suffix == ".py" and filepath.name != "__init__.py":
        # Get module name without extension
        module_name = filepath.stem
        importlib.import_module(f".{module_name}", package=__name__)
```

## Migration from os.path

If you have old code using `os.path`, here's how to migrate:

### Before (os.path)

```python
import os

# Path operations
path = os.path.join("wavetables", "sine.wav")
dirname = os.path.dirname(path)
basename = os.path.basename(path)
name, ext = os.path.splitext(basename)

# Directory operations
os.makedirs(dirname, exist_ok=True)
for filename in os.listdir(dirname):
    if filename.endswith(".wav"):
        full_path = os.path.join(dirname, filename)

# Check permissions
if os.access(path, os.W_OK):
    print("Writable")
```

### After (pathlib)

```python
from pathlib import Path

# Path operations
path = Path("wavetables") / "sine.wav"
dirname = path.parent
basename = path.name
name = path.stem
ext = path.suffix

# Directory operations
dirname.mkdir(parents=True, exist_ok=True)
for filepath in dirname.iterdir():
    if filepath.suffix == ".wav":
        # filepath is already the full path!
        pass

# Check permissions (more pythonic)
test_file = path.parent / ".write_test"
try:
    test_file.touch()
    test_file.unlink()
    print("Writable")
except (OSError, PermissionError):
    print("Not writable")
```

## Best Practices

### ✅ Do This

```python
from pathlib import Path

# Use Path objects internally
def process_wavetable(input_path: Path) -> Path:
    output_path = input_path.parent / f"{input_path.stem}_processed.wav"
    # ... processing ...
    return output_path

# Accept both strings and Path objects in public APIs
def save_file(output_dir: Union[str, Path]) -> Path:
    output_path = Path(output_dir)  # Normalize to Path
    # ... save logic ...
    return output_path

# Use the / operator
filepath = base_dir / subdir / filename

# Use Path properties
if filepath.suffix == ".wav":
    print(filepath.stem)
```

### ❌ Avoid This

```python
# Don't use string concatenation
filepath = directory + "/" + filename  # Bad!

# Don't use os.path with pathlib
import os
path = Path("dir")
bad = os.path.join(str(path), "file")  # Mixing APIs

# Don't convert to string unnecessarily
def process(path: Path) -> str:
    return str(path)  # Why convert?
```

## Common Patterns

### Pattern 1: Safe Directory Creation

```python
from pathlib import Path

def ensure_output_dir(output_dir: Union[str, Path]) -> Path:
    """Ensure output directory exists and is writable."""
    output_path = Path(output_dir)

    try:
        output_path.mkdir(parents=True, exist_ok=True)

        # Test writability
        test_file = output_path / ".write_test"
        test_file.touch()
        test_file.unlink()

        return output_path
    except (OSError, PermissionError) as e:
        raise RuntimeError(f"Cannot use directory {output_dir}: {e}")
```

### Pattern 2: Find Files by Extension

```python
from pathlib import Path
from typing import List

def find_wav_files(directory: Union[str, Path]) -> List[Path]:
    """Find all WAV files in directory."""
    dir_path = Path(directory)
    return [f for f in dir_path.iterdir() if f.suffix == ".wav"]

# Or use glob
def find_wav_files_recursive(directory: Union[str, Path]) -> List[Path]:
    """Find all WAV files recursively."""
    dir_path = Path(directory)
    return list(dir_path.rglob("*.wav"))
```

### Pattern 3: Generate Related Filenames

```python
from pathlib import Path

def generate_variants(base_path: Path) -> dict[str, Path]:
    """Generate related file paths."""
    return {
        "original": base_path,
        "backup": base_path.with_suffix(base_path.suffix + ".bak"),
        "metadata": base_path.with_suffix(".json"),
        "processed": base_path.parent / f"{base_path.stem}_processed{base_path.suffix}"
    }

# Usage
base = Path("wavetables/sine.wav")
variants = generate_variants(base)
print(variants["backup"])  # wavetables/sine.wav.bak
print(variants["metadata"])  # wavetables/sine.json
```

### Pattern 4: Cross-Platform Paths

```python
from pathlib import Path

# Paths work the same on Windows and Unix!
path = Path("wavetables") / "output" / "sine.wav"

# On Windows: wavetables\output\sine.wav
# On Unix:    wavetables/output/sine.wav

# Always use / operator, never string concatenation
good = base_path / "subdir" / "file.wav"
bad = str(base_path) + "/" + "subdir" + "/" + "file.wav"  # Don't!
```

## Path Object Quick Reference

| Operation         | Code                       | Returns        |
| ----------------- | -------------------------- | -------------- |
| Create path       | `Path("dir/file.txt")`     | Path object    |
| Join paths        | `Path("dir") / "file.txt"` | Path object    |
| Get filename      | `path.name`                | str            |
| Get stem (no ext) | `path.stem`                | str            |
| Get extension     | `path.suffix`              | str            |
| Get directory     | `path.parent`              | Path           |
| Check exists      | `path.exists()`            | bool           |
| Check is file     | `path.is_file()`           | bool           |
| Check is dir      | `path.is_dir()`            | bool           |
| Create directory  | `path.mkdir(parents=True)` | None           |
| List directory    | `path.iterdir()`           | Iterator[Path] |
| Find files (glob) | `path.glob("*.wav")`       | Iterator[Path] |
| Find recursive    | `path.rglob("*.wav")`      | Iterator[Path] |
| Get absolute      | `path.resolve()`           | Path           |
| Convert to string | `str(path)`                | str            |
| Get file stats    | `path.stat()`              | os.stat_result |
| Read file         | `path.read_text()`         | str            |
| Write file        | `path.write_text(content)` | int            |

## Integration with This Project

### In Generators

```python
from pathlib import Path
from wavetable_synthesis.export.wav import save_wavetable

def my_generator_workflow():
    """Example generator workflow using Path objects."""
    # Generate data
    data = generate_wavetable_data()

    # Save and get Path back
    filepath = save_wavetable(
        name="my_generator",
        data=data,
        output_dir=Path("output") / "custom",
    )

    # Use Path methods
    print(f"Saved {filepath.stat().st_size} bytes")
    print(f"To: {filepath.resolve()}")

    return filepath
```

### In Tests

```python
from pathlib import Path
import pytest

def test_wavetable_generation(tmp_path: Path):
    """pytest provides tmp_path as a Path object."""
    # tmp_path is already a Path!
    output_dir = tmp_path / "wavetables"

    filepath = save_wavetable("test", data, output_dir=output_dir)

    # Use Path methods in assertions
    assert filepath.exists()
    assert filepath.suffix == ".wav"
    assert filepath.parent == output_dir
```

## Additional Resources

- [pathlib documentation](https://docs.python.org/3/library/pathlib.html)
- [PEP 428 - The pathlib module](https://www.python.org/dev/peps/pep-0428/)
- [Real Python: Python pathlib tutorial](https://realpython.com/python-pathlib/)

## Summary

- **Always use `pathlib.Path`** for file operations
- **Accept `Union[str, Path]`** in public APIs for flexibility
- **Return `Path` objects** from functions
- **Use the `/` operator** for path joining
- **Use Path properties** (`.name`, `.stem`, `.suffix`, etc.)
- **Convert to string only when necessary** (e.g., for external libraries)

The pathlib approach makes code more readable, maintainable, and cross-platform!
