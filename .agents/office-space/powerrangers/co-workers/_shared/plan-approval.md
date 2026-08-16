## Plan-Approval Gate

If a task's own text explicitly asks you to share a plan and wait for approval before building, do
**not** implement. Write the plan to
`.agents/office-space/{{workflow}}/mail/out/question-<task-id>-<slug>.md` in `Question:` / `Answer:`
format, send an `[AWAITING-APPROVAL]-<task-id>.md` message to
`.agents/office-space/{{workflow}}/slack/{{lead}}/`, and sleep. Only start once you receive a
genuinely fresh `task` for it — that is what approval looks like. Never proceed on a timeout or a
guess.

### Up-front plan-approval (risk: high, novel boundaries)

Also treat plan-approval as **required before coding** when the task is `risk: high` **and** the
work is novel concurrency, a trust-boundary change, or multi-model / multi-agent security design
(more than one defensible model of who can forge a channel or hold a lock). Even if the task text
omits an explicit “share a plan first” line:

1. Write the plan to `mail/out/question-<task-id>-<slug>.md` (`Question:` / `Answer:`).
2. Wake the lead with `[AWAITING-APPROVAL]-<task-id>.md` under `slack/{{lead}}/`.
3. Do **not** implement until a fresh `task` / design ACK arrives.

Team-lead should mark such tasks for plan-approval at triage when those signals are obvious. See
also **reject-budget** (design ACK after thrash) and host WORKFLOW reject-budget policy when
present.
