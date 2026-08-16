# Decision: engine lives in `generator/` (2026-08-15)

`wavetable_synthesis/` and `wavetable_tests/` live under `<repo>/generator/`.

Import names stay `wavetable_synthesis`. Commands stay
`python -m wavetable_synthesis`. Tests run from `generator/wavetable_tests/`.

`discover.repo_root()` is the parent of `generator/` so `maths/` stays at the
repo root.
