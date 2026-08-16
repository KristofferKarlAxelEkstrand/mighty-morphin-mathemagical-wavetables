# generator/

This folder is the wavetable engine: the Python library and its tests.

Write new wave formulas in [`maths/`](../maths/), not here.

```text
generator/
├── wavetable_synthesis/   # Library (import name is still wavetable_synthesis)
└── wavetable_tests/       # Test suite
```

You still run:

```bash
python -m wavetable_synthesis --list
pytest generator/wavetable_tests/
```
