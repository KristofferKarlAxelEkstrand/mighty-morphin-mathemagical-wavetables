# Keep / refresh (package-owned skills + partials)

After bumping the office-space package (or switching `npx` version), bring package doctrine current
**without** clobbering host work.

## Commands

```bash
office-space whats-new
office-space skills refresh --check
office-space skills refresh --write          # optional: --notify
# Multi-workflow: prefer --workflow <product>; bare scan includes fixtures
office-space partials refresh --check [--workflow NAME]
office-space partials refresh --write [--workflow NAME]  # when package partials changed
office-space sync --write
office-space doctor
```

| Mode                                                  | Behavior                                                                                                                                                                                                                                                       |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `whats-new`                                           | Print host-facing sections from package `templates/host-upgrades.md` with version **>** host stamp (semver). `--all` full file; `--from VER` exclusive floor. Does not stamp.                                                                                  |
| `skills refresh --check`                              | List package-owned skills that differ from bundled templates. Nonzero when stale.                                                                                                                                                                              |
| `skills refresh --write`                              | Update package-owned skills; **print the same summary before writing**; leave host-owned alone; stamps `.agents/office-space/host-meta.json`.                                                                                                                  |
| `skills refresh --write --notify`                     | Same as `--write`, then write/refresh `mail/in/UPGRADE-<version>.md` for lead triage (opt-in; default path writes no mail).                                                                                                                                    |
| `partials refresh --check\|--write [--workflow NAME]` | Package `templates/partials/*.md` → each workflow `co-workers/_shared/<name>.md`. Host-owned extra basenames never touched. Prefer `--workflow` for product-only on multi-workflow hosts; bare scans all (incl. fixtures). Does **not** write host-meta stamp. |
| `sync --write` / `doctor`                             | Re-bridge discovery adapters; prove no broken symlinks.                                                                                                                                                                                                        |

v1 backup: **git**. No silent overwrite even without a `--backup` flag.

## Ownership

| Class                      | Examples                                                                                                                                                                                                                                                                                                      | Refresh?                           |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| **Package-owned skills**   | Full set (matches `skills refresh --help`): `office-space-protocol`, `office-space`, `model-chooser`, `office-space-onboard`, `office-space-team-design`, `agent-agnostic`, `share-skills`, `create-skill`, `agent-cli-integration`, `tmux-automation`, `watch-and-improve-office-space`, `technical-writing` | Yes (`skills refresh`)             |
| **Host-owned skills**      | Domain / product skills under `.agents/skills/`                                                                                                                                                                                                                                                               | **Never** auto-overwrite           |
| **Package-owned partials** | Basenames under package `templates/partials/*.md`                                                                                                                                                                                                                                                             | Yes (`partials refresh`)           |
| **Host-owned partials**    | Extra files under a workflow’s `co-workers/_shared/`                                                                                                                                                                                                                                                          | **Never** auto-overwrite or delete |

Dogfood note: this package’s own dogfood copies of some skills/partials may be fuller than trimmed
host templates. Refresh comparisons use the template each item shipped from — not “differs from
dogfood ⇒ stale.”

## Host notes + release hygiene

- Runtime source of truth: **`templates/host-upgrades.md`** inside the published package
  (`src/templates/host-upgrades.md` in this repo).
- Run `office-space whats-new` after a bump to see host impact since the stamp.
- **Release hygiene (D9):** every release must add its current `## X.Y.Z` section to
  `src/templates/host-upgrades.md` in the same change or the release bump PR. Pure internals: use
  one line “No host impact.” The qualification driver rejects a newest notes section that differs
  from `package.json`; `npm pack` itself does not run this gate.

## What not to use as upgrade

| Action                                      | Why not                                                                                                                   |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `init --force`                              | Re-scaffolds the **workflow** (prompts, mission, that workflow’s `_shared`); too broad; not the skill/partial update path |
| Re-run bare `init` expecting skill upgrades | Skills are seed-if-missing; init must not silently overwrite existing package skill files                                 |
| Hand-editing only under `.claude/skills`    | Adapter tree is not source of truth; next sync/refresh fights you                                                         |

Even with `init --force`, repo-global package skills under `.agents/skills/` stay seed-if-missing;
intentional skill updates → `skills refresh --write` only. Prefer `partials refresh` over `--force`
when only package `_shared` partials need updating.

## Init seed-if-missing

Package-owned skill files are seed-if-missing on init; **only** `skills refresh --write`
intentionally updates them. If you still see silent skill clobber on multi-workflow init, treat it
as a package defect — file it; do not “fix” by forking into harness mirrors.

## Package `_shared` partials

`co-workers/_shared/*.md` shipped by init are package doctrine:

- Prefer role prompts / host-only partial **names** over forking package partial files in place.
- Non-force init: existing `_shared` is seed-if-missing (not silently rewritten).
- `init --force`: may overwrite package-named `_shared` for that workflow after printing which files
  it replaces (“clean re-scaffold”).
- Day-to-day package partial upgrades: **`partials refresh --check|--write [--workflow NAME]`** (not
  `init --force`). On multi-workflow hosts prefer product `--workflow`; bare check scans fixtures
  too.

## After refresh

1. `sync --write` so holdout adapters match canonical skills.
2. `doctor` — no `broken-symlink`; `missing` adapters may be OK until you bridge Claude/etc.
3. Spot-check one holdout harness still lists onboard / protocol.
4. Optional: `office-space whats-new` again if you want the full bulletin after absorbing.
