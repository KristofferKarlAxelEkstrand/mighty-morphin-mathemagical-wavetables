# Audio contract

Binding product text is spec `S001` (`.agents/office-space/powerrangers/spec/S001.md`). This
file is the check list agents use while editing.

## Raw `generate(theta, u)`

| Check | Pass |
| --- | --- |
| `u` | `_validate_u(u)` runs. Outside `[0, 1]` raises `ValueError`. |
| dtype | `float64` |
| length | `len(out) == len(theta)` |
| finite | `np.isfinite(out).all()` |
| energy | not all zeros |
| source | formula, not a sample file |

## After `generate_wavetable` / processing

Use the generator `get_processing()` flags. Default flags normalize and remove DC.

| Check | Pass |
| --- | --- |
| peak | `0.95 <= max(abs(frame)) <= 1.05` |
| DC | `abs(mean(frame)) < 0.01` |
| wrap | first-to-last step matches the formula (sine continuous; saw may jump once) |

Processing target numbers in `generator/wavetable_synthesis/core/processing.py` are tighter (peak `1e-6`,
DC `1e-10`). Tests may use the looser table above until E001 T003 lands. Do not loosen further.

## Review rejects

- Tests that only exercise `any_generator`
- `generate(..., u=-1)` that does not expect `ValueError`
- Degrees, Python loops over samples, or sampled audio
- Changing `BaseGenerator.generate` without a human gate
