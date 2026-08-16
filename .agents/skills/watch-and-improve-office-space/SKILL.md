---
name: watch-and-improve-office-space
description: >-
  Check in on a live office-space team: watch health, evaluate setup and collaboration, diagnose why
  sessions die, adjust prompts/board habits, rework tests when the suite stalls throughput, keep
  init templates current, and improve this skill from lessons. Use when watching developer-team,
  reviewing how the team works, fixing restarts/flaps, speeding up QA/test gardens, or evolving the
  watch-and-improve loop.
---

# Watch and improve office-space

Observe a running workflow, score how it is set up and how agents work together, then make durable
fixes to the live team, package defaults (`src/templates/`), and **this skill**. Evidence over
guesses.

Default workflow name: `developer-team` (override with the user’s workflow).

## Modes (pick one)

| Mode         | When                                                     | Do                                                          |
| ------------ | -------------------------------------------------------- | ----------------------------------------------------------- |
| **Pulse**    | Continuous “keep an eye on it”                           | Snapshot → material deltas only → diagnose if down          |
| **Check-in** | “How is the team working?” / ~30–60m                     | Pulse + full scorecard + ≤3 adjustments + skill self-review |
| **Deep**     | After flap cluster, epic done, or user asks for thorough | Check-in + init template audit + file tasks for leftovers   |

## Do this

### 1. Baseline

```bash
bash .agents/skills/watch-and-improve-office-space/scripts/team-snapshot.sh [workflow]
node src/cli.js team roles [workflow]
node src/cli.js doctor
```

Then open (paths under `.agents/office-space/<workflow>/`):

- `WORKFLOW.md`, `space.json`, `co-workers/*`
- Latest `health/reports/`, `mail/in/`, unread `slack/<agent>/` (not `read/`)
- `health/session-binding.log` if the session vanished recently

### 2. By mode

**Pulse** — every tick (default 30s if continuous):

1. Session up? (`<workflow>-agents` only — ignore `qualify-*` / `wf*` fixtures).
2. Down → classify before restart ([diagnose-downtime.md](references/diagnose-downtime.md)).
3. Up but `await=dead` **or `await=never`** + assigned work → capture-pane: oneshot mid-turn (incl.
   post-respawn missing heartbeat) vs truly dead.
4. Note new mail, handoffs, rejects, dual claims, false stalls.
5. Report **material** changes only.

**Check-in / Deep** — also:

1. Score **setup / communication / collaboration / flow**
   ([evaluate-team.md](references/evaluate-team.md)).
2. Apply ≤3 adjustments ([improvement-playbook.md](references/improvement-playbook.md)).  
   If **tests/QA stall the team** (long default suites, always-verify, dogfood killed by tests),
   **reworking the test garden** (fast vs integration split, isolation, agent gate docs) is in scope
   — not only co-worker prompts.
3. Universal lessons → `src/templates/` ([init-templates.md](references/init-templates.md)).
4. Skill self-review ([self-improve.md](references/self-improve.md)); `npm run validate:skills` if
   you edited the skill.

### 3. Hand off

```text
Status: UP|DOWN — one line
Scorecard: setup / communication / collaboration / flow   # omit on pure Pulse
Findings: 1–5 bullets + evidence paths
Changes: live | src/ | templates/ | this skill
Skill self-improve: none | …
Open: next for team / human
```

## Load when

| File                                                                     | Open when                          |
| ------------------------------------------------------------------------ | ---------------------------------- |
| [references/diagnose-downtime.md](references/diagnose-downtime.md)       | Down, flap, restart, false “dead”  |
| [references/evaluate-team.md](references/evaluate-team.md)               | Scorecard / collaboration check-in |
| [references/improvement-playbook.md](references/improvement-playbook.md) | Choosing and applying fixes        |
| [references/init-templates.md](references/init-templates.md)             | Promoting lessons into `init`      |
| [references/self-improve.md](references/self-improve.md)                 | Editing this skill                 |
| `scripts/team-snapshot.sh`                                               | One-shot status dump               |

## Sibling skills

| Skill                           | Use for                     |
| ------------------------------- | --------------------------- |
| `office-space-protocol`         | mail / tasks / slack format |
| `office-space`                  | co-worker design doctrine   |
| `agent-cli-integration`         | CLI launch, auth, probes    |
| `tmux-automation`               | panes, private sockets      |
| `model-chooser`                 | cli / model / effort        |
| `create-skill` / `share-skills` | skill shape / discovery     |

## Gotchas

- **Session names are host-global** (`${workflow}-agents`). `OFFICE_SPACE_ROOT` does not isolate
  tmux. Never `stop_team` / `team stop` a live dogfood name from tests — use unique workflow names
  or private tmux (`tmux-automation`).
- **`team start` always `stop_team`s first.** Prefer `team start` / `run-team --ensure` only when
  down.
- **`cli=unsupported`** (stub activity probe) blocks **weak-evidence** stagnant restart only.
  Confirmed-dead await poller + work still queues `stagnant` (T196). Mid-turn hold: `paneBusy` or
  cli active → no restart.
- **Oneshot mid-turn** shows pane `timeout` + dead await — normal until `CLI turn finished`.
- **`await=never` after relaunch** with `timeout` pane + work assigned is usually false dead
  (heartbeat cleared, lock stale) — capture-pane before any `--restart`.
- **Empty board after epic close** + idle implementers is expected, not a staffing fail, when lead
  woke scout / scout is mid-hunt (scorecard **D9**). Silent scout for ~1h+ with no wake is the real
  flow fail.
- **Other sessions** (`qualify-host*`, `wf*`) on the same server are not dogfood death.
- **Ctrl `q`** stops the only running team with no confirmation.
- Prefer `node src/cli.js …` while developing this package (not stale `dist/`/npx).
- **Slow default tests stall throughput** — split/rework is allowed; do not only preach “run fewer
  checks.”
- **Deep `qa` pile + concurrent full gardens** — if many tasks sit at `stage: qa` while multiple
  agents each run full `test:unit`, host thrashes and drain slows. Fix: one garden at a time; Tests
  reuse own prior full-unit (≤60m + path-clean); archive duplicate `[TASK]` wakes after picking one
  primary. See dogfood package-test-gates rules 8/10 and WORKFLOW §3.3 / §6.4.
- One skill self-improve pass per check-in; human owns commits unless asked.
