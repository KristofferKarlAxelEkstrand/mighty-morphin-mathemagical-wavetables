# First-run sequence (detail)

Use when walking greenfield or an empty host. SKILL.md has the short ladder; this expands traps.

## 1. Classify

Before `init`:

| Check                                       | Why                                              |
| ------------------------------------------- | ------------------------------------------------ |
| Existing `.agents/office-space/`?           | Second workflow vs first scaffold                |
| `AGENTS.md` / `CLAUDE.md` / `.cursorrules`? | Merge vs replace; Claude needs `@AGENTS.md` shim |
| Which harnesses must work?                  | Bridges differ (Claude hard holdout)             |
| Package already a dep / only `npx`?         | Affects bump + refresh later                     |

Open sibling `agent-agnostic` for layout and AGENTS.md rules.

## 2. Scaffold

```bash
npx @kristoffer-karl-axel-ekstrand/office-space init
# or pin version: npx @kristoffer-karl-axel-ekstrand/office-space@<ver> init
```

Useful flags:

| Flag                                   | Use                                                         |
| -------------------------------------- | ----------------------------------------------------------- |
| `--workflow NAME`                      | Non-default workflow folder name                            |
| `--agents a,b,c` + `--agent-roles "…"` | Thin lineup (every agent needs a role entry)                |
| `--harness claude\|codex\|…`           | Default CLI for scaffolded agents                           |
| `--force`                              | Overwrite **workflow folder** content — not a skill upgrade |

Roles: `lead`, `implementer`, `reviewer`, `qa`, `none` (prompt-only). Exactly one enabled agent
should have `lead: true` in live config.

Init creates runtime dirs, mission skeleton, seed task, and package skills (set grows with E007). It
does **not** write your product mission for you.

## 3. Design the team

Open `office-space-team-design`. Force concrete choices: mission one-liner, thin vs full lineup,
capability flags, pipeline/human gates, locks, first real backlog.

Anti-pattern: leave default six roles and seed `WORKFLOW.md` "for later."

## 4. Author under the workflow tree only

| Path                                                 | Own                                    |
| ---------------------------------------------------- | -------------------------------------- |
| `.agents/office-space/<wf>/WORKFLOW.md`              | Product mission + pipeline rules       |
| `.agents/office-space/<wf>/co-workers/*.prompt.md`   | Role bodies                            |
| `.agents/office-space/<wf>/co-workers/*.prompt.json` | cli, model, capability flags, partials |
| `.agents/office-space/<wf>/space.json`               | Stages, defaults, machine checks       |
| `.agents/skills/<name>/`                             | Skills (package-owned or host domain)  |

Do not invent a parallel mail/task board outside office-space folders.

## 5. Discover

```bash
office-space sync --write          # Unix symlinks for holdouts
office-space sync --write --mirror # Windows / when mirrors required
office-space sync --check          # CI-friendly drift of adapters
```

`sync` bridges **skills** (and related discovery adapters) — it does **not** generate MCP vendor
files from `.agents/mcp/servers.json`.

Prove a holdout agent can list the skill (Claude: `/skills` or equivalent), not only that doctor is
green.

## 6. Prove

```bash
office-space check-system   # bash, jq, tmux, realpath, timeout, flock, sha256sum (coreutils + util-linux flock)
office-space doctor
office-space check --tier fast
```

Optional live smoke: `team start` → `team status` → `team stop`. If system deps missing, fix
`check-system` first; do not declare onboard complete without a plan to run the team.

## 7. Real backlog

Seed `T001` / welcome messages are bootstraps, not the product backlog.

1. Write an epic under `epics/todo/` (or your workflow's epic tree).
2. File tasks with clear acceptance, `owned_paths`, and a `verification_tier` when the host uses
   tiers.
3. Archive or close seed tasks so the board shows real work.

## 8. AGENTS.md pointers (lean)

Always-on context should **name** skills, not paste them:

- `office-space-onboard` — first-run + keep
- `office-space-team-design` — design / redesign
- `office-space-protocol` — mail / tasks / slack

Keep path one-liner: after package bump → `whats-new` → `skills refresh --check|--write` (optional
`--notify`) → `partials refresh --check|--write [--workflow NAME]` → `sync --write` → `doctor`. On
multi-workflow hosts prefer product `--workflow`; bare partials scan includes fixtures.

Claude: `CLAUDE.md` with `@AGENTS.md` first; Claude-only notes below the import.
