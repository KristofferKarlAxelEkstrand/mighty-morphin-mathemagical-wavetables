## Peer consultation contract

Direct Architect or Security consultation follows this contract.

**Request envelope:**

- Send a `question` or `review` wake to `slack/architect/` or `slack/security/`
- Include the task id, one concrete question, relevant paths/context, and `blocking: yes|no`
- Do not use `mail/in/` or broadcast routine consultations

**Specialist handling:**

- Handle one bounded consultation per wake
- Reply to the requester's Slack folder
- Do not take task assignment or path locks
- Do not claim work or approve normal review/QA

**Original task unchanged:**

- Consultation never changes the original task's assignee, stage, or `owned_paths`
- Specialists advise only. They do not implement or approve pipeline gates

**Record rule:**

- Material scope/architecture/security-property changes go in the task or one short
  `records/decisions/` note; the original task owner creates this record, not the specialist or the
  consultation requester
- Routine advice creates no record noise

**Escalation:**

- Escalate to Team Lead only for priority or scope changes, conflicting specialist advice, a human
  decision, or the existing high-risk design ACK

**Idle behavior:**

- On idle wakes, specialists do not hunt, mint tasks, or self-wake to stay busy
