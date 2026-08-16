## Mailbox Hygiene (not optional)

**Where messages go** (wrong folder = silent stall):

- `slack/<agent>/` — wake that agent. Residents watch their own `slack/<agent>/` and `slack/all/`.
  Handoffs, rejects, approvals, and "claim now" go here. Prefer `task-transition.js` (it writes
  `[TASK]-…` files); manual wakes go in `slack/<assignee>/`, **not** `mail/in/`.
- `slack/all/` — broadcast; leave the file after acting. Team-wide direction only.
- `mail/in/` — human → team / lead triage only. Implementers do **not** watch this by default.

**Delete or move every message file the moment you have acted on it.** A file left in your personal
`slack/` folder looks like unread mail on your next wake.

This rule is load-bearing for more than tidiness. The poller marks a message as seen _before_ your
turn has read anything — it exits the instant it spots the file, and your turn happens afterwards.
If that turn dies, a write-once mark would bury the message forever. So an unchanged file still
sitting in a mailbox gets **one** extra wake on the next cycle, on the assumption that a file left
in place was never handled. Leaving an acted-on file behind spends the single retry that exists to
rescue genuinely dropped work.

(`mail/out/` is exempt from the delete-on-read rule: a question legitimately waits there for a
human, and their answer edit triggers its own wake. But an answered question is spent — the moment
you wake on the answer and act on it, move the file to `mail/out/read/` in that same turn. A decided
`[DECISION]` or `[GATE]` left loose in `mail/out/` reads as an open question on the next sweep, so
`mail/out/` must show only genuinely unanswered items.)

**`slack/all/` inverts this rule.** The broadcast folder is shared by the whole team, so act on what
you find there and **leave the file** — deleting it takes it from everyone who has not woken yet.
Its author prunes it. You are woken once per broadcast; a file sitting there is not a dropped
message.

**Stale-work guard.** Before acting on any message, check whether the work is already done — the
task moved to `.agents/office-space/{{workflow}}/tasks/done/`, the change already shipped, or your
memory digest already records the verdict. If so, delete the stale message and move on. Do not
re-implement, re-review, or re-archive. This is what stops a restart from replaying an entire
mailbox.

**Malformed messages.** If a file is unreadable or you hit an unrecoverable error processing it,
move that specific file to `.agents/office-space/{{workflow}}/slack/quarantine/` so you do not
crash-loop on it.
