# Drift checklist

Lightweight setup-health. Diagnose here; **fix redesign via `office-space-team-design`**. `doctor`
surfaces objective setup warnings for the smells below; this checklist is the durable bar.

## Run through

Mark each item. Any **fail** means the host is not fully set up or has drifted.

| #   | Smell                               | How to check                                                                                                                                                      | Fix owner                                                                               |
| --- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| 1   | **Placeholder WORKFLOW**            | `WORKFLOW.md` still contains scaffold "rewrite / starting point" voice or literal template markers (e.g. unreplaced `{{…}}`, "Describe in one or two sentences…") | team-design + host authors mission                                                      |
| 2   | **Eternal T001**                    | Board still only seed welcome / explore stub; no real epic+tasks                                                                                                  | onboard step 7 — real backlog                                                           |
| 3   | **Protocol pasted into prompts**    | Role `.prompt.md` duplicates mail/task protocol instead of loading the skill                                                                                      | strip paste; keep `office-space-protocol`                                               |
| 4   | **Skills only under harness trees** | Content authored under `.claude/skills` / `.cursor/skills` as SoT                                                                                                 | move to `.agents/skills/`; bridge with `share-skills`                                   |
| 5   | **AGENTS.md missing pointers**      | No lean pointers to onboard, team-design, protocol (and keep/refresh)                                                                                             | edit AGENTS.md; Claude `@AGENTS.md` shim                                                |
| 6   | **Never ran sync**                  | Claude/holdouts have no adapters; skills invisible despite files on disk                                                                                          | `office-space sync --write` (+ prove in harness)                                        |
| 7   | **Package skills / partials stale** | After package bump, doctrine or `_shared` partials outdated                                                                                                       | Full keep path (below): `whats-new` → skills refresh → partials refresh → sync → doctor |

## Quick commands

Full **B. Keep path** after a package bump (epic D7):

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

Day-to-day probes:

```bash
office-space doctor
office-space sync --check
office-space skills refresh --check
office-space partials refresh --check [--workflow NAME]
office-space check --tier fast
```

## Handoff rule

| Finding                                                          | Next                                          |
| ---------------------------------------------------------------- | --------------------------------------------- |
| Missing bridge / never synced / stale package skills or partials | Stay on onboard + share-skills + keep path    |
| Wrong lineup, weak gates, god-agent, bad mission                 | `office-space-team-design` redesign playbooks |
| Mail/task protocol misuse on a live team                         | `office-space-protocol`                       |

## Automated signals (`office-space doctor`)

Prefer objective checks over "your mission is bad" AI judgment. `doctor` (and therefore
`check --tier fast`, which runs doctor first) prints **setup warnings** for:

| Smell                            | When                                                                                                                                                                                                 |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Missing package-owned skill dirs | Any of the D2 set is absent under `.agents/skills/` (dirs only — not body equality)                                                                                                                  |
| AGENTS.md pointers               | File missing, or lacks lean names `office-space-onboard` / `office-space-team-design` / `office-space-protocol`                                                                                      |
| WORKFLOW template residue        | **Default workflow only:** its `WORKFLOW.md` still contains mission-template marker text (e.g. "starting point, not a contract." / "Describe in one or two sentences…") or unreplaced `{{…}}` tokens |
| Stale host stamp                 | `host-meta.json` `packageVersion` is semver-older than the running package (keep-path hint: skills → partials → sync → doctor)                                                                       |
| Stale host-upgrade notes         | Package `templates/host-upgrades.md` latest `## X.Y.Z` is semver-older than the running package (release notes duty / qualify; **not** fixed by skills refresh alone)                                |
| Missing package-owned partials   | **Default workflow only:** lacks a package `templates/partials/*.md` basename under `co-workers/_shared/` (file presence only — not body equality)                                                   |

Warnings are **non-fatal** (doctor still exits 0). They point here and at team-design for fix
ownership — the CLI does not auto-rewrite host content.

**Fixture / secondary workflows** (adapter-sync fixtures, thin test hosts) are out of scope for
WORKFLOW-residue and missing-partials: doctor does not require every instance to be a full product
mission. Skills, AGENTS pointers, and host stamp stay host-wide.

When doctor hints `partials refresh --write`, always pin **`--workflow NAME`** (the default product
workflow). Bare multi-instance `--write` can clobber intentional fixture drift — see keep-refresh /
T252.

Also: `skills refresh --check` and `partials refresh --check` exit nonzero when package-owned skill
or partial _files_ are stale or missing (content-level; doctor only smells **missing** partial
basenames, not content-stale).

Dogfood exemption: this package's developer-team skills and `_shared` partials may intentionally
differ from trimmed host templates — do not "refresh down" dogfood-only depth by treating every body
diff as host drift. Doctor checks skill **directory** and partial **basename** presence, not body
equality.
