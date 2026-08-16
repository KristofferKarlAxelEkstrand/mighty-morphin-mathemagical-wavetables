---
name: wavetable-generator
description: >-
  Create or change a mathematical wavetable generator: generate(theta, u),
  @register_generator, morph, DC, periodicity, and registry-wide tests. Use when
  adding a generator, editing maths/, or reviewing the audio contract.
---

# Wavetable generator

Write a formula that turns phase and a morph amount into one cycle of audio.

## Do this

1. Copy `maths/example.py` to `maths/<name>.py`.
2. Change `@register_generator("example")`, the class name, and `get_info()` (`name` and `id`
   must match the decorator string).
3. Implement `generate(theta, u)`:
   - Call `self._validate_u(u)` first.
   - `theta` is radians, one cycle, `0` to `2π`.
   - Use vectorized NumPy. Return `float64` the same length as `theta`.
4. Keep the formula readable. Offline generation may be slow.
5. Prove:
   - `python -m wavetable_synthesis --list` shows the name
   - `python -m wavetable_synthesis <name>`
   - `pytest --no-cov generator/wavetable_tests` (tests must cover **all** registered names)

## Load when

| File | Open when |
| --- | --- |
| [references/audio-contract.md](references/audio-contract.md) | Review, QA, or writing assertions for peak, DC, dtype, `u`, wrap |
| [references/test-pattern.md](references/test-pattern.md) | Adding or changing tests that should apply to every generator |
| [references/common-formulas.md](references/common-formulas.md) | Writing sine, saw, triangle, square, or PWM math |

## Gotchas

- `any_generator` in `generator/wavetable_tests/conftest.py` is the **first** registry entry only. A test
  that uses it does not prove the contract for every generator.
- `u` outside `[0, 1]` must raise `ValueError`. Do not clamp and continue.
- Degrees are wrong. `2 * np.pi * np.arange(n) / n` is the usual `theta`.
- Do not load a WAV or other sample as the waveform. Math only.
- Peak and DC are finished by `get_processing()` flags. Still return a sane, finite raw array.
- Linux venv: `source .venv/bin/activate`. `Scripts/activate` is Windows.
