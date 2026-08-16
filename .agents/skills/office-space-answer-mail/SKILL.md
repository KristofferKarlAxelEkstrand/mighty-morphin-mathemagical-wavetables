---
name: office-space-answer-mail
description: >-
  Walk a workflow's mail/out/ queue and answer it: fill in bare Answer: lines on question items, and
  decide/reply on release-ready report items. Use when answering mail, clearing mail/out/, answering
  a parked question, responding to a release-ready report, or processing outbound office-space mail.
---

# Office-space answer mail

Clear a workflow's `mail/out/` queue conversationally: summarize each pending item, ask how to
respond, write the reply in the exact shape the protocol expects. `office-space-protocol` owns the
mail format and routing rules — this skill is a workflow on top of it, not a redefinition.

## Step 1 — pick the workflow

Scan `.agents/office-space/*/mail/out/*.md` (top-level files only — skip `read/`) for every workflow
under the host. Skip ephemeral leftovers (`selftest-*`, `probe-wf`) if present.

- Exactly one workflow has pending items → use it silently.
- More than one → list counts per workflow and ask which to work on.
- None → say so and stop.

## Step 2 — enumerate the queue

List pending files sorted oldest-first by `created:` frontmatter (fallback: filename/mtime). Read
each file's `type`, `from`, `created`, and enough of the body to summarize in one line.

## Step 3 — per item, branch on `type`

| Shape                                                             | How to spot it                                   | What to do                                                                                                                                                                                                            |
| ----------------------------------------------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Question**                                                      | Body ends in a bare `Answer:` line               | Summarize the question. Ask conversationally what the answer should be — open-ended; offer quick options only when a real shortlist exists (e.g. yes/no/custom). `Edit` the file in place to fill the `Answer:` line. |
| **Report** (or any other non-question type parked in `mail/out/`) | No `Answer:` field — e.g. a release-ready notice | Summarize it. Ask what to do: no action (skip), or reply to the team.                                                                                                                                                 |

**Question items** — do not move the file after answering. Archiving to `mail/out/read/` is the
responding agent's job on its next wake, per `office-space-protocol`; moving it yourself would
suppress that wake.

**Report items that want a reply** — draft a new `mail/in/` message, modeled on
`mail/in/read/human-answer-*.md`:

```markdown
---
type: answer
from: human
to: <original from, e.g. team-lead>
created: <now, ISO 8601>
---

<the human's reply>
```

Show the draft for confirmation before writing it. Never edit or move the original report file —
team-lead closes the loop on its own triage pass through `mail/in/`.

## Step 4 — loop

After each item, ask continue vs. stop. End when the queue is empty or the human stops.

## Gotchas

- Never invent frontmatter fields or `type` values beyond the enum documented in
  `office-space-protocol`.
- Never touch `mail/out/read/` or `mail/in/read/` — those are already closed.
- Never run `git add`/`commit`/`push` or `npm publish` on behalf of the human, even when a report
  says "release-ready" — commit and publish are human-owned regardless of what the report says.
- `mail/` is a gitignored live runtime dir; writing to it needs no special ceremony beyond the
  normal edit-confirmation flow.

## Sibling skills

| Skill                      | Use for                                      |
| -------------------------- | -------------------------------------------- |
| `office-space-protocol`    | Mail/task/slack format and routing authority |
| `office-space-onboard`     | First-run order, keep/refresh, drift checks  |
| `office-space-team-design` | Team shape, roles, pipeline, human gates     |
