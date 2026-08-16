# Decision: formulas live in `maths/` (2026-08-15)

Wave formulas live in `<repo>/maths/`. That folder is not a Python package. There is no
`__init__.py`. The engine loads each `*.py` file from `generator/wavetable_synthesis/core/discover.py`.

`wavetable_generators/` is removed. New work goes in `maths/<name>.py` with
`@register_generator` and `generate(theta, u)`.

Epic: E002.
