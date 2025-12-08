# CI Workflow Optimization Guide

## Overview

This document explains the CI workflow optimizations implemented to reduce GitHub Actions minutes usage
while maintaining code quality and test coverage.
These changes are designed for FOSS projects operating on the free tier with limited CI budget.

## Problem Statement

The original CI workflow was consuming more GitHub Actions minutes than necessary for a FOSS project:

- **6 parallel jobs** per run (4 test jobs + 1 lint + 1 CLI test)
- **4 Python versions tested** (3.10, 3.11, 3.12, 3.13)
- **Redundant dependency installations** across separate jobs
- **No concurrency controls** - old runs continued when new code was pushed
- **CI ran even for documentation changes** that don't affect code

## Optimizations Implemented

### 1. Reduced Python Version Matrix

**Before:**

```yaml
python-version: ["3.10", "3.11", "3.12", "3.13"]
```

**After:**

```yaml
python-version: ["3.10", "3.13"]
```

**Impact:** 50% reduction in test matrix jobs

**Rationale:**

- Tests the oldest (3.10) and newest (3.13) supported versions
- Covers the full compatibility range
- Python minor versions typically have high backward compatibility
- If code works on 3.10 and 3.13, it almost certainly works on 3.11 and 3.12

### 2. Job Consolidation

**Before:**

- `test`: Run tests on 4 Python versions (4 jobs)
- `lint`: Run code quality checks (1 job)
- `cli-test`: Run CLI tests (1 job)
- Total: 6 jobs, each installing dependencies independently

**After:**

- `test`: Run tests on 2 Python versions (2 jobs)
- `quality-and-cli`: Combined code quality and CLI tests (1 job)
- Total: 3 jobs

**Impact:** 50% reduction in total jobs

**Rationale:**

- Linting and type checking only need to run once on the latest Python version
- CLI tests don't need to run on multiple Python versions separately
- Combining these eliminates redundant dependency installations

### 3. Concurrency Controls

**Added:**

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
```

**Impact:** Automatic cancellation of outdated workflow runs

**Rationale:**

- When you push a new commit while CI is running, the old run is cancelled
- Saves minutes on testing code that's already been superseded
- Particularly valuable during active development with frequent commits

### 4. Path Filters

**Added:**

```yaml
paths-ignore:
  - "**.md"
  - "docs/**"
  - "docs_tech/**"
  - "LICENSE"
  - ".gitignore"
  - ".editorconfig"
  # ... other config files
```

**Impact:** CI skipped for documentation-only changes

**Rationale:**

- Documentation changes don't affect code functionality
- No need to run tests, linting, or builds for README updates
- Significant savings for docs-heavy projects

### 5. Improved Dependency Caching

**Added:**

```yaml
cache: "pip"
cache-dependency-path: "pyproject.toml"
```

**Impact:** Faster dependency installation through better cache hits

**Rationale:**

- Explicitly specifying the dependency file improves cache key generation
- Reduces time spent downloading and installing dependencies
- Particularly helpful for projects with stable dependency lists

## Expected Cost Savings

### Time Savings Per Run

- **Before:** ~48 seconds total (6 jobs running in parallel)
- **After:** ~25-30 seconds estimated (3 jobs running in parallel)
- **Reduction:** ~40-50% faster

### Action Minutes Savings

Based on typical usage patterns:

| Scenario               | Before     | After      | Savings            |
| ---------------------- | ---------- | ---------- | ------------------ |
| Code change PR         | 6 jobs     | 3 jobs     | 50%                |
| Documentation change   | 6 jobs     | 0 jobs     | 100%               |
| Multiple commits to PR | 6 jobs × N | 3 jobs × 1 | 50% + cancellation |

**Monthly savings example:**

- 50 code commits/month: ~150 job-runs saved
- 20 doc commits/month: ~120 job-runs saved
- 10 multi-commit PRs: ~30 job-runs saved
- **Total: ~300 job-runs saved per month**

## Quality Assurance

### What's Maintained

✅ Test coverage on oldest and newest Python versions
✅ All code quality checks (Ruff linting/formatting, mypy type checking, Bandit security)
✅ All CLI functionality tests
✅ Coverage reporting to Codecov
✅ Fail-fast disabled (all tests run even if one fails)

### What Changed

- ℹ️ Python 3.11 and 3.12 no longer explicitly tested (covered by 3.10 and 3.13)
- ℹ️ Code quality checks run once instead of in parallel with each test job
- ℹ️ Documentation changes don't trigger CI

## Best Practices for FOSS CI

1. **Test Version Boundaries**: Test oldest and newest supported versions, skip middle versions unless there are known compatibility issues
2. **Consolidate Similar Jobs**: Combine jobs that can share dependency installations
3. **Use Path Filters**: Skip CI for changes that don't affect code (docs, configs)
4. **Enable Concurrency Cancellation**: Don't waste minutes on outdated code
5. **Cache Aggressively**: Specify dependency files explicitly for better caching
6. **Monitor Usage**: Regularly review GitHub Actions usage in repository settings

## Additional Optimization Opportunities

Future enhancements to consider:

1. **Dependabot Optimization**: Reduce PR limits or use grouped updates
2. **Conditional Jobs**: Run expensive jobs only on main branch, not every PR
3. **Reusable Workflows**: Share workflow definitions across repositories
4. **Self-Hosted Runners**: For high-volume projects (not recommended for public repos due to security)
5. **Scheduled Runs**: Move non-critical checks to nightly runs instead of every commit

## Monitoring

Check your CI performance:

1. Go to `Settings` → `Actions` → `General` in your repository
2. View usage under the "Actions usage" section
3. Compare month-over-month trends

## References

- [GitHub Actions Best Practices](https://docs.github.com/en/actions/learn-github-actions/best-practices-for-github-actions)
- [GitHub Actions Usage Limits](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
- [Optimizing GitHub Actions Workflows](https://docs.github.com/en/actions/using-workflows/about-workflows#optimizing-workflows)

## Questions or Concerns?

If you have questions about these optimizations or want to suggest improvements, please open an issue or discussion in the repository.
