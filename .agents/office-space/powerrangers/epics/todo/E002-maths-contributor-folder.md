---
id: e002
title: One maths/ folder for wave formulas
status: done
created: 2026-08-15
---

# E002 — One `maths/` folder for wave formulas

Make contributing a wave as simple as: open `maths/`, copy `example.py`, edit the formula. Hide
package plumbing so a new person never has to touch `__init__.py`.

This epic is already implemented in the tree. Keep it as the product record until the lead
promotes the decision file and removes this epic.

## Why

Discovery used to live in `wavetable_generators/__init__.py`. That file made auto-load work and
also cluttered the only folder beginners open. `maths/` is a folder of formula files, not a
Python package.

## What shipped

- `maths/` at the repo root: `example.py`, `linear_interpolation.py`, `sine_to_triangle.py`,
  `square_pwm_tz.py`, and a short `README.md`
- `generator/wavetable_synthesis/core/discover.py` loads each `maths/*.py` file
- `get_registry()` calls that loader
- `wavetable_generators/` is gone
- VS Code hides `**/__init__.py` in the explorer
- Docs, AGENTS.md, office-space paths, and spec `S001` say `maths/`
- Tests in `generator/wavetable_tests/test_maths_discovery.py`

## How a beginner adds a wave

1. `cp maths/example.py maths/my_wave.py`
2. Change `@register_generator("example")` and write `generate(theta, u)`
3. `python -m wavetable_synthesis my_wave`

## Evidence already run

- `python -m wavetable_synthesis --list` shows the same four names
- `python -m wavetable_synthesis example` writes a WAV
- `pytest --no-cov generator/wavetable_tests` (127 passed, including discovery tests)
- `ruff check` on `discover.py`, decorator registry, discovery tests, and `maths/`

## Tasks

None open. Implementation landed outside the board, then this epic was filed to record it.

## Durable record

`records/decisions/2026-08-15-maths-folder.md`
