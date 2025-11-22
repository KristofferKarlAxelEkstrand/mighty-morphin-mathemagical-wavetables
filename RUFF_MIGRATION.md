# Ruff Migration Report

This document summarizes the Ruff linting results and provides recommendations for the modernization transition.

## Current Status

**Date:** 2025-11-22
**Ruff Version:** 0.14.6
**Total Issues Found:** 165
**Auto-fixable:** 46 (with `--fix`)
**Unsafe Auto-fixable:** 35 (with `--unsafe-fixes`)

## Issue Breakdown

### Top Issues by Category

| Issue Type | Count | Auto-fix | Description |
|------------|-------|----------|-------------|
| PLC0415 | 62 | ❌ | Import outside top-level (mostly in tests) |
| UP006 | 21 | ✅ | Non-PEP 585 annotations (use `list` not `List`) |
| EM102 | 11 | ❌ | F-string in exception (should assign to variable) |
| UP035 | 10 | ❌ | Deprecated imports from `typing` |
| EM101 | 8 | ❌ | Raw string in exception |
| TID252 | 8 | ❌ | Relative imports (prefer absolute) |
| UP007 | 7 | ❌ | Use `X \| Y` instead of `Union[X, Y]` |
| RUF100 | 5 | ✅ | Unused `noqa` directives |
| UP045 | 5 | ✅ | Use `X \| None` instead of `Optional[X]` |
| Others | 28 | Mixed | Various minor issues |

### Files with Most Issues

```bash
wavetable_tests/test_*.py - ~62 issues (mostly test-specific patterns)
wavetable_synthesis/cli/cli.py - ~20 issues
wavetable_synthesis/__init__.py - ~10 issues
wavetable_synthesis/core/* - ~15 issues
wavetable_generators/*.py - ~5 issues
```

## Recommendations

### Phase 1: Quick Wins (Auto-fixable) ✅ Recommended Now

Run auto-fix to resolve 46 issues immediately:

```bash
ruff check --fix .
```

This will fix:

-  Type annotation modernization (PEP 585, PEP 604)
-  Unused noqa directives
-  Some subprocess issues
-  Unsorted `__all__`

### Phase 2: Test File Imports ⏳ Later

**Issue:** 62 instances of `PLC0415` (imports outside top-level)

**Why it exists:** Tests use local imports for test isolation

**Options:**

1.  Keep as-is (add `# noqa: PLC0415` to test files)
2.  Update Ruff config to ignore in tests (already done in pyproject.toml)
3.  Refactor tests to use top-level imports

**Recommendation:** Already configured to ignore in tests via `pyproject.toml`:

```toml
[tool.ruff.lint.per-file-ignores]
"wavetable_tests/**" = ["PLC0415"]  # Allow imports in test functions
```

### Phase 3: Exception Message Patterns ⏳ Later

**Issues:** EM101, EM102 (exception message formatting)

**Current pattern:**

```python
raise ValueError(f"Invalid value: {x}")
```

**Recommended pattern:**

```python
msg = f"Invalid value: {x}"
raise ValueError(msg)
```

**Recommendation:** Low priority. Current pattern is readable and common. Can be addressed during regular code maintenance.

### Phase 4: Modern Type Hints ⏳ Later

**Issues:** UP006, UP007, UP035, UP045 (deprecated typing patterns)

**Examples:**

```python
# Old style
from typing import List, Optional, Union
def foo(x: List[str], y: Optional[int]) -> Union[str, None]:
    pass

# Modern style (Python 3.10+)
def foo(x: list[str], y: int | None) -> str | None:
    pass
```

**Recommendation:** Medium priority. The project targets Python 3.10+, so these modernizations are appropriate. Some can be auto-fixed with `--fix`.

### Phase 5: Import Organization ⏳ Later

**Issue:** TID252 (relative imports)

**Current:** Using relative imports like `from .core import ...`
**Alternative:** Absolute imports like `from wavetable_synthesis.core import ...`

**Recommendation:** Low priority. Relative imports are fine for internal package structure.

## Migration Strategy

### Conservative Approach (Recommended)

1.  **Now:** Enable Ruff for linting (already done ✅)
2.  **Now:** Run auto-fixes for safe changes

   ```bash
   ruff check --fix .
   ruff format .
   ```

1.  **Next PR:** Apply type hint modernizations manually or with unsafe fixes
2.  **Ongoing:** Fix issues as code is touched for other reasons
3.  **Future:** Fully replace Black/isort/Flake8 in CI

### Aggressive Approach (If Desired)

```bash
# Fix everything that's auto-fixable (including unsafe)
ruff check --fix --unsafe-fixes .
ruff format .

# Review changes carefully
git diff

# Run tests to ensure nothing broke
make test
```

## Configuration

Current Ruff configuration in `pyproject.toml` already handles many exceptions:

```toml
[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports
"wavetable_tests/**" = ["ARG", "PLR", "PLC0415"]  # Relax test rules
"wavetable_generators/**" = ["PLR0915"]  # Allow long functions in generators
```

## Impact on CI

Currently, CI uses legacy tools (Black, isort, Flake8, Pylint). Options:

### Option A: Keep Legacy Tools in CI (Current)

-  ✅ No changes needed
-  ✅ Code passes existing checks
-  ❌ CI runs slower

### Option B: Add Ruff to CI (Parallel)

-  ✅ Developers can use either
-  ✅ Gradual transition
-  ❌ Runs both old and new

### Option C: Switch CI to Ruff Only (Future)

-  ✅ Faster CI
-  ✅ Single source of truth
-  ⚠️ Requires fixing issues first

**Recommendation:** Stay with Option A for now. The CI workflow has comments showing how to enable Ruff when ready.

## Testing Impact

✅ All 122 tests still pass
✅ 88% code coverage maintained
✅ No breaking changes from Ruff configuration

## Developer Impact

**Positive:**

-  ⚡ 10-100x faster linting
-  🔧 Auto-fix capabilities
-  🎯 Single tool instead of 4+

**Minimal:**

-  Pre-commit hooks catch issues early
-  Clear error messages from Ruff
-  Legacy tools still work

## Summary

The modernization infrastructure is **complete and working**. Ruff is configured, documented, and ready to use. The 165 issues it found are:

1.  **Not bugs** - They're style/modernization opportunities
2.  **Not urgent** - Code works perfectly as-is
3.  **Gradually fixable** - Can address over time or all at once

**Immediate Action Recommended:**

```bash
# Fix safe auto-fixable issues
ruff check --fix .
ruff format .
git commit -m "Apply Ruff auto-fixes"
```

**Long-term Strategy:**
Fix remaining issues during normal code maintenance, or dedicate a future PR to complete the migration.

## Questions?

See `MODERNIZATION.md` for more details on the transition strategy and tool comparisons.
