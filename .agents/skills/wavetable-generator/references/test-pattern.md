# Test pattern

## Registry-wide fixture

Do not rely on `any_generator` for contract tests. Parametrize over the live registry:

```python
import pytest

from wavetable_synthesis.core.registry import get_registry


@pytest.fixture(params=sorted(get_registry(verbose=False)))
def generator_name(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture
def generator(generator_name: str):
    return get_registry(verbose=False)[generator_name]
```

If the registry is empty, skip. Importing generators must stay side-effect safe.

## Focused vs package

- While editing one test file: `pytest --no-cov generator/wavetable_tests/test_that_file.py`
- Before review (`package`): `pytest --no-cov wavetable_tests`
- `integration`: drop `--no-cov` (project addopts already enable coverage) plus
  `python -m mypy --strict generator/wavetable_synthesis/`

## `u` range

```python
def test_rejects_u_out_of_range(generator, sample_theta):
    with pytest.raises(ValueError):
        generator.generate(sample_theta, -0.1)
    with pytest.raises(ValueError):
        generator.generate(sample_theta, 1.1)
```

## Owned paths

`generator/wavetable_tests/` is one lock. Do not start a second implementer on tests while another test
task is `implementing`.
