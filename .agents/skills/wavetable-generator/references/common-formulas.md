# Common formulas

`theta` is radians, one cycle. Mix with `u` in `[0, 1]`.

## Building `theta`

```python
theta = 2.0 * np.pi * np.arange(n, dtype=np.float64) / n
```

Do not use degrees. Do not include the duplicate endpoint (`endpoint=False` if you use
`np.linspace`).

## Waves already in this repo

| Shape | Formula | Notes |
| --- | --- | --- |
| Sine | `np.sin(theta)` | Wrap is continuous |
| Saw | `theta / np.pi - 1.0` | One jump at the wrap. See `example.py` |
| Triangle | `(2.0 / np.pi) * np.arcsin(np.sin(theta))` | See `sine_to_triangle.py` |
| Square | `np.sign(np.sin(theta))` | See `linear_interpolation.py` |
| Through-zero PWM | `sign(sin(theta) - (2u - 1))` | See `square_pwm_tz.py` |

## Morph

Linear mix is enough:

```python
y = (1.0 - u) * wave_a + u * wave_b
```

Name `wave_a` and `wave_b`. Do not hide the mix in one dense line if the formula is the lesson.

## Precision

Use `float64` through the formula. The export path may cast to `float32` for the WAV. That is
not the generator's job.
