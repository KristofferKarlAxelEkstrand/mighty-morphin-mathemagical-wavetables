---
name: office-space-team-design
description: >-
  Design and redesign an office-space host team: mission one-liner, thin vs full lineup, capability
  flags, pipeline and human gates, path locks, evidence bar, and first real backlog. Use when
  choosing roles, rewriting WORKFLOW.md, adding or removing a co-worker, changing harness or CLI,
  splitting lead from implementer, introducing runners, widening or narrowing human gates, or fixing
  setup drift that needs a team-shape change.
---

# Office-space team design

Force concrete choices for **this** host. Init scaffolds folders; this skill authors mission, roles,
pipeline, and backlog. Pair with `office-space-onboard` for first-run sequence and keep/refresh —
this skill owns **what the team is**, not how to install the package.

## Do this (greenfield)

Work under `.agents/office-space/<workflow>/` only. Rewrite the mission template; do not paste
dogfood mission text.

### 1. Mission one-liner

Write one sentence: **what the team builds** and **why more than one agent**. If a single specialist
agent would do, stop — you do not need a full team yet.

Put it in `WORKFLOW.md` § Mission.

### 2. Lineup — start thin

| Shape        | Who (capabilities)                                              | When                                               |
| ------------ | --------------------------------------------------------------- | -------------------------------------------------- |
| **Minimal**  | `lead` + `implementer` + one agent with `reviewer` **and** `qa` | Greenfield, small product, one human owner         |
| **Standard** | `lead` + `implementer` + separate `reviewer` + separate `qa`    | Parallel review/QA, clearer gates                  |
| **Extended** | Standard + second `implementer` and/or scout/runner             | Sustained multi-path work or scheduled maintenance |

Default: **Minimal**. Add roles only when a real bottleneck appears (backlog pile-up, review queue,
blind spots). Prefer `office-space init --agents … --agent-roles "…"` for a fresh workflow; edit
co-worker `.prompt.json` / `.prompt.md` for an existing one. Confirm with
`office-space team roles <workflow>`.

**Optional role templates** (not in thin/full presets): package `templates/co-worker-roles/` —
`architect`, `researcher`, `product`, `tech-writer`, `security`, `release`. Specialty prompts with
Own/Never; most are prompt-only (`=none`). Copy onto an existing host or include the id in custom
`--agents` with matching flags (see that folder’s README).

### 3. Capability flags (source of pipeline authority)

In each co-worker’s `.prompt.json`:

| Flag                | Meaning                                                                                       |
| ------------------- | --------------------------------------------------------------------------------------------- |
| `lead: true`        | Exactly **one** enabled agent — triage, spawn tasks, installs                                 |
| `implementer: true` | Stage `implementing` via `--assignee auto-implementer`; may claim work and hold `owned_paths` |
| `reviewer: true`    | Stage `review` via `--assignee auto-reviewer`                                                 |
| `qa: true`          | Stage `qa` via `--assignee auto-qa`                                                           |

Ids (`team-lead`, `dev-1`, …) are names only. Route by capability, not folklore agent names. Prompt
bodies: Own / Never / Incomplete Exit — never paste the full protocol into every role.

### 4. Pipeline and human gates

Default stages (edit `space.json` → `tasks.stages` if needed):

`queued → implementing → review → qa → done`, plus `human` / `blocked` as needed.

In `WORKFLOW.md` § Human gate protocol, name **only** stages that require a human (design ACK,
release, secrets). Everything else must proceed once stage checks pass. Skipping Quality to “go
faster” is not a valid gate design — see [anti-patterns](references/anti-patterns.md).

### 5. Locks

- Tasks declare `owned_paths`; overlaps fail closed via `task-transition.js`.
- Default: **one** active implementation task per implementer.
- Every implementer loads `co-workers/_shared/concurrency-locks.md` (package doctrine — prefer
  prompt overlays over forking `_shared` in place).

### 6. Evidence bar

In `WORKFLOW.md` § Quality bars, define checkable criteria per stage:

1. **While editing** — narrowest focused test / lint on touched paths.
2. **Before review** — project’s fast default suite (if any) + focused coverage of the change.
3. **Integration / full verify** — only when the task’s paths or risk demand it (runtime, locks,
   multi-agent start/stop, packaging). Optional deeper tier policy: epic E006 / host
   package-test-gates docs if present.

Never invent a second board or a parallel “just run verify always” policy that stalls the team.

### 7. First backlog

Replace seed `T001` / welcome mail with a **real** epic + tasks:

- Concrete acceptance criteria and `owned_paths`.
- `verification_tier` (or host equivalent) set intentionally — not left blank if the host uses
  tiers.
- Small enough to finish in one implementer turn series; no eternal “explore the repo” stubs.

### 8. Wire discovery (after design)

Skills stay under `.agents/skills/`. After authoring: `office-space sync --write`, `doctor`,
`check --tier fast` (or host equivalent). First-run order and drift checklist live in
`office-space-onboard` — open that skill for the sequence.

## Redesign (existing host)

Do **not** re-run full greenfield. Open the matching playbook, change the fewest files, then
re-prove roles and discovery:

→ [references/redesign-playbooks.md](references/redesign-playbooks.md)

## Anti-patterns

→ [references/anti-patterns.md](references/anti-patterns.md)

## Load when

| File                                                                 | Open when                                                                                                         |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| [references/redesign-playbooks.md](references/redesign-playbooks.md) | Add/remove agent, harness/CLI change, split lead/implementer, runners, human-gate width, model audit after shifts |
| [references/anti-patterns.md](references/anti-patterns.md)           | Reviewing a draft setup, fixing drift, Quality pushback on team shape                                             |

## Sibling skills

| Skill                                              | Use for                                              |
| -------------------------------------------------- | ---------------------------------------------------- |
| `office-space-onboard`                             | First-run order, keep/refresh, drift “is it set up?” |
| `office-space-protocol`                            | mail / tasks / slack / memory runtime                |
| `office-space`                                     | Short co-worker design tips (not a decision guide)   |
| `model-chooser`                                    | cli / model / effort per role                        |
| `agent-agnostic` / `share-skills` / `create-skill` | Layout, discovery bridges, new skills                |

## Gotchas

- **Never copy** this package’s dogfood `developer-team/WORKFLOW.md` into a host — structure yes,
  product mission no.
- Canonical skills only under `.agents/skills/`. Harness trees (`.claude/skills`, …) are adapters,
  not source of truth.
- `doctor` OK ≠ harness sees skills. After design changes that touch skills, still `sync --write`.
- Do not merge protocol text into every `.prompt.md`. Point at the protocol skill.
- Package-owned `_shared` partials: customize via role prompts or host-only partial names; forking
  package `_shared` without a refresh plan creates silent drift on later `init --force`.
- This skill does **not** run `init`, implement CLI `skills refresh` / `explain`, or author harness
  mirrors — those are other E007 spawns / package work.
