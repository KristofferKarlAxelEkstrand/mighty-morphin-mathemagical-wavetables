---
id: e003
title: Python-first tooling (Node only for office-space)
status: todo
created: 2026-08-16
---

# E003 — Python-first tooling

The product is a Python library. A contributor who writes a wave in `maths/` should need
Python, a venv, and `pip install -e ".[dev]"`. Node stays only because office-space has no
Python port.

Do not port office-space. Do not remove `.agents/office-space/`.

## Why

Today a clone looks like two projects. `package.json` owns git hooks (husky, lint-staged),
Markdown (Prettier, markdownlint-cli), and npm-check-updates. Python already has Ruff, mypy,
pytest, bandit, and `.pre-commit-config.yaml`. Two hook systems fought. Setup tells two
stories.

## Keep on Node

| Tool | Why it stays |
| --- | --- |
| `@kristoffer-karl-axel-ekstrand/office-space` | Agent team. No Python package. |
| `package.json` / `package-lock.json` | Install that one package. |
| `npm install` | Host / team only. Not required to generate a WAV. |

## Move to Python

| Now (Node) | Replace with |
| --- | --- |
| husky + lint-staged | Python `pre-commit` as the only git hook |
| Prettier (md / json / yaml) | `mdformat` for Markdown. pre-commit-hooks for JSON / YAML |
| markdownlint-cli | Drop. Do not keep the Node markdownlint pre-commit hook |
| npm-check-updates | Drop. Nothing left to bump except office-space |
| `npm run lint:py` / `type:check` | Makefile / `python -m ruff` / `python -m mypy` |

`[project.optional-dependencies] dev` gets `pre-commit` back. No new **runtime** Python or
npm dependency. That keeps this off the WORKFLOW.md human gate.

## Tasks (lead files these)

Split in this order. Do not start T007 until T005 and T006 are done.

- T005 — Hooks: `pre-commit install` is the git hook. Remove husky and lint-staged. Point
  `setup.sh` and `.devcontainer/postCreate.sh` at `pre-commit install`. Delete
  `docs/tech/husky.md` after the replacement note exists. `core.hooksPath` must not stay on
  `.husky/_`.
- T006 — Docs quality in Python: add `mdformat` (dev extra or pre-commit repo). Format
  Markdown with that. Use `pre-commit-hooks` for JSON / YAML / whitespace. Remove prettier
  and markdownlint-cli from `package.json` and from `.pre-commit-config.yaml`.
- T007 — Shrink Node to office-space: `package.json` lists only the office-space dependency.
  No `devDependencies`. README, DEVELOPMENT, CONTRIBUTING, AGENTS, Makefile, and setup say:
  Python is enough to develop generators. `npm install` is only for the office-space host.

## Done

- `python -m wavetable_synthesis --list` still works after a Python-only setup
- `pre-commit run --all-files` is the hook and the local quality sweep for mixed files
- `ruff` / `mypy` / `pytest --no-cov generator/wavetable_tests` still pass
- `package.json` has no husky, lint-staged, prettier, markdownlint, or npm-check-updates
- A new contributor can skip Node and still lint, test, and generate a WAV
- office-space still installs with `npm install` and `office-space` still runs

## Out of scope

- Porting office-space to Python
- Changing `generate(theta, u)` or spec `S001`
- Merging overlapping product docs (`DEVELOPMENT.md` vs `docs/development-setup.md`)
- Adding Flask, Sphinx, or other unused extras back
