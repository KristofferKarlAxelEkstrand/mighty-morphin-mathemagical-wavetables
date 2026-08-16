## Messaging Protocol

All communication happens through files in `mail/` (tasks) or `slack/` (async coordination). Every
message file uses YAML frontmatter:

```markdown
---
type: task
from: agent-name
created: 2026-07-21T10:26:45+00:00
---
```

**Where messages go** (wrong folder = silent stall):

- `slack/<agent>/` — wake that agent. Residents watch their own `slack/<agent>/` and `slack/all/`.
  Handoffs, rejects, approvals, and "claim now" go here. Prefer `task-transition.js` (it writes
  `[TASK]-…` files); manual wakes go in `slack/<assignee>/`, **not** `mail/in/`.
- `slack/all/` — broadcast; leave the file after acting. Team-wide direction only.
- `mail/in/` — human → team / lead triage only. Implementers do **not** watch this by default.

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

**Style:**

- Every message is re-read by other agents on future turns — verbosity is a recurring token cost.
  Write for that.
- Lead with the result, blocker, or action; plain words, short sentences
- Routine notes: 5 lines or fewer. Structured fix lists (e.g. rejections) may run longer — one line
  per item, no repeated preamble
- Cut greetings, ceremony, repetition, and status narration that changes nothing
- Use exact repo-relative paths when citing files; link to canonical files instead of pasting long
  detail
- Never omit a fact the reader needs to act safely just to hit a length target

**Closing work:**

- Put the closure note in the task, report completion to the configured lead at `slack/{{lead}}/`,
  and land `done` with
  `node {{taskTransitionScript}} {{workflow}} <task-id> --stage done --from <agent>` (D8 / closure
  gates). Use `node {{archiveTaskScript}} {{workflow}} <task-id>` only for runner fast-path or
  already-`stage: done` metadata refresh. Reserve `mail/out/` for human questions, decisions, and
  gate packets.

Use capabilities, not conventional agent names, when routing pipeline work. The single enabled agent
with `lead: true` handles lead-directed reports. `--assignee auto-implementer` selects an enabled
`implementer: true` agent (stage `implementing` only). `--assignee auto-reviewer` selects an enabled
`reviewer: true` agent. `--assignee auto-qa` selects an enabled `qa: true` agent.
