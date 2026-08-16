# Husky - Git Hooks

This is a Python project. Husky is the git hook. It runs lint-staged on the files you commit.

## Install

```bash
npm install
```

The `prepare` script in `package.json` sets `core.hooksPath` to `.husky/_`. Edit `.husky/pre-commit`.

## What runs on commit

`.husky/pre-commit` puts `.venv` on `PATH`, then calls `npx lint-staged`.
GUI git does not activate the venv. The hook must do that, or `python -m ruff` uses
`/usr/local/bin/python` and fails.

`.prettierignore` and `.markdownlintignore` skip `.agents/`. Those files are not
product docs. Formatting that tree on a large commit can kill Prettier.

`package.json` (`lint-staged`):

- `*.py` — Ruff format and lint
- `*.md` — Prettier and markdownlint
- `*.{json,yml,yaml}` — Prettier

CI runs Ruff, mypy, and pytest. Those checks are the quality bar.

Do not run `pre-commit install`. It overwrites the husky hook. `.pre-commit-config.yaml` is optional for `pre-commit run --all-files` or pre-commit.ci.

## Manual format

```bash
npm run format
npm run format:check
npm run lint:md
npm run lint:md:fix
```

## Troubleshoot

If hooks do not run:

```bash
npm run prepare
```

Skip the hook only when you must:

```bash
git commit --no-verify -m "Emergency fix"
```
