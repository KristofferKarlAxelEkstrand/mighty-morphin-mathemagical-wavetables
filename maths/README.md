# Maths

Put your wave formulas here. This folder is not a Python package. There is no `__init__.py`.
Drop a `.py` file in and the CLI finds it.

## Make a wave

1. Copy the template:

   ```bash
   cp maths/example.py maths/my_wave.py
   ```

2. In `my_wave.py`, change `@register_generator("example")` to `@register_generator("my_wave")`.
   Change the class name. Write your formula in `generate(theta, u)`.

3. Run it:

   ```bash
   python -m wavetable_synthesis my_wave
   ```

`theta` is one cycle in radians (`0` to `2π`). `u` is the morph amount (`0` to `1`).
