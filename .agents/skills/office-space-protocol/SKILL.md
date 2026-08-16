---
name: office-space-protocol
description: >-
  Coordinate office-space workflow agents via mail/, tasks/, slack/, memory logs, and checkpoints.
  Use when writing mail, claiming or archiving tasks, posting Slack wakes, logging memory, or
  following the file-based team protocol.
---

# Office-Space Protocol

This team coordinates through files in `.agents/office-space/<your-workflow-name>/`. Two separate
systems live here and are **not** mirrors of each other — `mail/` is the messaging layer, `tasks/`
is the work-tracking board:

- `mail/in/` — human → team / lead triage only (`mail/in/read/` holds triaged items); implementers
  do **not** watch this by default
- `mail/out/` — outbound replies and questions; a file ending in a bare `Answer:` line is a question
  parked for a human
- `slack/<agent>/` — wake that agent; `slack/all/` is the auto-created broadcast folder every agent
  also watches
- `tasks/{todo,working-on,done}/` — the work-tracking board (stage moves via `task-transition.js`;
  see Closing work)

These are live runtime folders and are ignored by Git. Durable decisions, compact memory,
retrospectives, and restart checkpoints live under `records/`. Before stopping the team, run:

```bash
office-space state checkpoint <your-workflow-name>
```

Tasks moved to `human` or `blocked` receive a focused checkpoint automatically. Once a human
question is answered, promote the decision into the canonical spec/evidence file and remove the
resolved checkpoint through normal review.

## Message routing

Wrong folder = silent stall. Agent-to-agent wakes and handoffs must land in Slack, not `mail/in/`.

- `slack/<agent>/` — wake that agent. Residents watch their own `slack/<agent>/` and `slack/all/`.
  Handoffs, rejects, approvals, and "claim now" go here. Prefer `task-transition.js` (it writes
  `[TASK]-…` files); manual wakes go in `slack/<assignee>/`, **not** `mail/in/`.
- `slack/all/` — broadcast; leave the file after acting. Team-wide direction only.
- `mail/in/` — human → team / lead triage only. Implementers do **not** watch this by default.

## Message Format

Every message file uses YAML frontmatter:

```markdown
---
type: task
from: agent-name
created: 2026-07-21T10:26:45+00:00
---

Message body...
```

**Message types:**

- `task` — New work in `mail/in/` for an agent to pick up
- `report` — Status update or completion summary
- `blocked` — Agent is blocked; waiting for external input or another agent's work
- `feedback` — Non-blocking comment (formatting nits, suggestions)
- `approved` — The named review or gate passed; proceed to the next required gate. It does not by
  itself authorize task closure.
- `rejected` — Work failed review; blocked until fixes are applied
- `nit` — Small style or formatting observation
- `test` — Test result or test-garden note
- `deps` — Dependency or prerequisite update
- `npm-request` — Request to install, update, or remove an npm dependency
- `prompt-updated` — Notification that a co-worker prompt has changed
- `question` — Question for the team or a human
- `bug` — Bug report
- `feature` — Feature request or proposal
- `review` — Request for code/spec review
- `answer` — Reply to a question
- `handoff` — Hand-off note between pipeline stages
- `run-request` — Enqueues a one-shot runner job from `runners/` (E003 job contract). Under
  D007/E008 the team **controller** owns dispatch/schedule — do not assume the lead runs the job
  inline. Does not create a resident agent session.

## Style Guidelines

Every message gets read by other agents on every future turn — verbosity here is a recurring token
cost, not a one-time one. Write for that.

- Lead with the result, blocker, or action. One line, if possible.
- Plain words, short sentences. Routine notes: aim for 5 lines or fewer.
- Say only what the reader needs to act: evidence, paths, commands, risks, next step. Nothing else.
- Cut greetings, ceremony, repeated context, and progress narration that changes nothing.
- Reference files/functions with exact repo-relative paths — never restate what's already in the
  diff.
- Long detail belongs in the canonical file (task, spec, decision record) — link it, don't paste it.
- Exception: a structured multi-item fix list (e.g. a review rejection) can run longer than 5 lines
  — one line per required item, numbered, no repeated preamble. Still cut everything else.
- Never omit a fact the reader needs to act safely just to hit a length target. Short and wrong
  wastes more tokens than long and right — the reader has to come back and ask.

## Closing work (board → done)

**Primary path:** land `done` through `task-transition.js`. It enforces path-release (D8),
closure-evidence, closure-stage gates, and `owned_paths` overlap checks — do not hand-edit task
files or bypass with archive.

```bash
node task-transition.js <your-workflow-name> <task-id> --stage done --from <agent-name>
# claims / review / qa handoffs also use task-transition (it writes [TASK]-… wakes)
```

(Run from wherever this package is installed — e.g.
`node_modules/@kristoffer-karl-axel-ekstrand/office-space/dist/` via npm, or the package tree when
developing.)

**`archive-task.js` is not the primary done recipe.** Non-runner archive **refuses** unless the task
is already `stage: done` (or already under `tasks/done/`). Use it only for:

- metadata refresh / folder move when stage is already done
- runner fast-path closures that pass archive's runner validation

```bash
node archive-task.js <your-workflow-name> <task-id>
```

Archive operates on the `tasks/` board only — it does **not** touch `mail/` or `memory/`. Log
findings with `memory-log.js`, below.

## Memory Logging

After completing a batch of work, log what you learned with the `append` subcommand and a
`--summary` flag:

```bash
node memory-log.js append <your-workflow-name> <agent-name> \
  --summary "completed a review sweep; discovered X needs Y" \
  --area some/area --refs 12,15
```

This appends to `memory/<agent>/<agent>-log.md` (`--area` and `--refs` are optional), so the team
and future runs remember the lesson during the live session. The log self-compacts (`compact-all`)
so it never grows unbounded. Promote durable cross-session lessons into `records/memory/`; raw
memory logs are not versioned.
