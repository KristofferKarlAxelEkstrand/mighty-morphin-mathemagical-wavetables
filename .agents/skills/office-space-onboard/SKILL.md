---
name: office-space-onboard
description: >-
  First-run and keep-healthy sequence for an office-space host: classify, init, design the team,
  author WORKFLOW/prompts, sync/discover skills, prove with check-system/doctor/check, replace seed
  T001, refresh package skills after upgrades, and run a drift checklist. Use when onboarding a
  repo, after office-space init, after bumping the package, when skills are missing, doctor is green
  but agents are blind, setup smells, or "is this host set up?".
---

# Office-Space Onboard

Stand up a host once, then keep it healthy. **Init scaffolds; this skill sequences judgment.**
Redesign (roles, gates, lineup) → sibling `office-space-team-design`. Coordination protocol →
`office-space-protocol`.

## Load table

| When                             | Open                         |
| -------------------------------- | ---------------------------- |
| **First** (this skill)           | Onboard sequence below       |
| **Then** design/redesign         | `office-space-team-design`   |
| **Then** day-to-day mail/tasks   | `office-space-protocol`      |
| Discover / fix bridges           | `share-skills` (on demand)   |
| Author a skill                   | `create-skill` (on demand)   |
| Portable repo layout / AGENTS.md | `agent-agnostic` (on demand) |
| Pick CLI/model per role          | `model-chooser` (on demand)  |

Do **not** paste redesign playbooks here — if drift needs a new lineup or gate shape, hand off to
`office-space-team-design`.

## Do this

### A. First run (greenfield or empty host)

1. **Classify** the repo — harnesses in play, existing `AGENTS.md` / `CLAUDE.md` / `.agents/`.
   Detail → `agent-agnostic`.
2. **Scaffold** if needed:
   ```bash
   npx @kristoffer-karl-axel-ekstrand/office-space init
   # thin|full presets: --preset thin   (or --preset full)
   # custom: --agents lead,dev-1,quality --agent-roles "lead=lead,dev-1=implementer,quality=reviewer+qa"
   # Claude holdout: --harness claude
   # Do not combine --preset with --agents / --agent-roles
   ```
   Prefer thin lineups; do not copy dogfood `developer-team` wholesale.
3. **Design the team** — mission, roles, pipeline, human gates, first backlog. Open
   `office-space-team-design` and make concrete choices. Do not skip this for "default is fine."
4. **Author product policy** only under `.agents/office-space/<workflow>/`:
   - `WORKFLOW.md` — rewrite every section (mission is product-owned).
   - `co-workers/*.prompt.md` + `.prompt.json` — role bodies; prefer host overlays over forking
     package `_shared` partials.
5. **Discover skills** — canonical tree is `.agents/skills/` only:
   ```bash
   office-space sync --write
   ```
   Claude needs `.claude/skills` bridges; `doctor` OK ≠ Claude sees skills. → `share-skills`.
6. **Prove**:
   ```bash
   office-space check-system   # bash, jq, tmux, realpath, timeout, flock, sha256sum (coreutils + util-linux flock)
   office-space doctor
   office-space check --tier fast
   # optional live smoke:
   office-space team start && office-space team status && office-space team stop
   ```
7. **Replace seed work** — archive or rewrite eternal `T001` / welcome mail; file a **real** first
   epic + tasks with `owned_paths`. A host that still only has seed explore stubs is not onboarded.
8. **Pointers** — root `AGENTS.md` should name onboard, team-design, and protocol (and
   keep/refresh). Claude: root `CLAUDE.md` with `@AGENTS.md` first.

Longer step notes → [references/first-run.md](references/first-run.md).

### B. Keep path (after package bump / upgrade)

Do **not** use `init --force` to upgrade skills or partials (too broad; clobbers workflow content).

```bash
office-space whats-new                # host notes since host stamp (semver); --all / --from VER
office-space skills refresh --check   # package-owned skills that differ from bundled templates
office-space skills refresh --write   # update package-owned only; optional --notify → mail/in digest
# Multi-workflow: prefer --workflow <product>; bare partials scan all workflows (incl. fixtures)
office-space partials refresh --check [--workflow NAME]
office-space partials refresh --write [--workflow NAME]  # when package partials changed
office-space sync --write
office-space doctor
```

- **Package-owned** (safe to refresh; full set = `skills refresh --help`): `office-space-protocol`,
  `office-space`, `model-chooser`, `office-space-onboard`, `office-space-team-design`,
  `agent-agnostic`, `share-skills`, `create-skill`, `agent-cli-integration`, `tmux-automation`,
  `watch-and-improve-office-space`, `technical-writing`.
- **Host-owned** (never auto-overwrite): any other skill under `.agents/skills/` (domain skills).
- **Partials:** package basenames under `templates/partials/*.md` only → each workflow’s
  `co-workers/_shared/`; extra host files never overwritten or deleted. Does **not** stamp host-meta
  (only init + `skills refresh --write` absorb the package for notes floor).
- **Notify:** `--notify` with `skills refresh --write` only — writes/refreshes
  `mail/in/UPGRADE-<version>.md` for lead triage; default path writes no mail.
- v1 backup model: **git**. `--write` prints the changed-file summary first (no silent clobber).
- `init` is seed-if-missing for package skill files; intentional updates → `skills refresh` only.
- Host-facing log (runtime SoT in package): `templates/host-upgrades.md` (repo:
  `src/templates/host-upgrades.md`). Every release must add its current `## X.Y.Z` section before
  publish; the qualification driver rejects a newest section that differs from the package version.
  This is a release-qualification check, not an `npm pack` check.

Detail → [references/keep-refresh.md](references/keep-refresh.md).

### C. Drift checklist ("is this host set up?")

Run [references/drift-checklist.md](references/drift-checklist.md) on revisit. If anything fails and
the fix is redesign (roles, gates, mission rewrite), **diagnose here → fix via team-design**. Do not
duplicate redesign playbooks in this skill.

## Load when

| File                                                           | Open when                                   |
| -------------------------------------------------------------- | ------------------------------------------- |
| [references/first-run.md](references/first-run.md)             | Walking greenfield steps in detail          |
| [references/keep-refresh.md](references/keep-refresh.md)       | After package bump; refresh ownership rules |
| [references/drift-checklist.md](references/drift-checklist.md) | Audit / revisit / "something feels wrong"   |

## Gotchas

- **`doctor` green ≠ skills visible** — especially Claude. Bridge via `share-skills` /
  `sync --write`.
- **Never author under harness mirrors** (`.claude/skills`, `.cursor/skills`, …). Canonical =
  `.agents/skills/` only; adapters are bridges.
- **Do not paste protocol into every prompt** — load `office-space-protocol`; keep prompts
  role-thin.
- **Do not copy dogfood `developer-team/WORKFLOW.md`** — structure yes; product mission no.
- **`init --force` is not the skill upgrade path** — workflow re-scaffold only; skills → refresh.
- **Package `_shared` partials** are package doctrine: prefer customizing role prompts / host-only
  partial names over silent forks. Upgrade partials with `partials refresh`, not `init --force`.
- **Init presets:** `office-space init --preset thin|full` (default lineup unchanged without
  `--preset`; explicit `--agents` / `--agent-roles` must not combine with `--preset` — error).
