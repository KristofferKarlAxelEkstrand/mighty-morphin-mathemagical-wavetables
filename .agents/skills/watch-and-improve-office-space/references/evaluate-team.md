# Evaluate setup and collaboration

Score each item **pass / weak / fail** with **one evidence path**. Then apply fixes via
[improvement-playbook.md](improvement-playbook.md).

Paths under `.agents/office-space/<workflow>/`.

---

## A. Setup

Inspect: `WORKFLOW.md`, `space.json`, `co-workers/*`, `runners/*`, `team roles`, `doctor`.

| #   | Check         | Pass                                       | Weak / fail                          |
| --- | ------------- | ------------------------------------------ | ------------------------------------ |
| A1  | Mission       | Mission, non-goals, human gates clear      | Vague; agents invent goals           |
| A2  | Role coverage | lead + reviewer + qa present               | Missing gate roles                   |
| A3  | Narrow roles  | Own/Never; scout ≠ implement; lead ≠ code  | God-agent; lead coding               |
| A4  | CLI / model   | Valid + authed; cost matches role          | Auth flaps; all max cost             |
| A5  | Stages        | space.json matches real handoffs           | Skip review/qa                       |
| A6  | Runners       | Controller path understood; queue durable  | Queue wiped on start; lead runs jobs |
| A7  | Partials      | Shared messaging/locks/sleep/git as needed | Doctrine duplicated or missing       |

## B. Communication

Inspect: `mail/in|out/`, `slack/<agent>/`, handoff notes.

| #   | Check         | Pass                                             | Weak / fail                               |
| --- | ------------- | ------------------------------------------------ | ----------------------------------------- |
| B1  | Routing       | Slack wakes + task-transition; lead owns mail/in | Wrong folder; implementers triage mail/in |
| B2  | Brevity       | Action-first, short (protocol style)             | Ceremony; repeated context                |
| B3  | Handoffs      | Concrete reject list / approve evidence          | Empty LGTM; vague reject                  |
| B4  | Broadcast     | `slack/all/` rare, team-wide                     | Personal work as broadcast                |
| B5  | Human surface | Real questions only; Answer: when parked         | Fake gates; unanswered pile               |
| B6  | Noise         | Stall wakes false when `blocked_by`              | Infinite false stalls                     |

## C. Collaboration

Inspect: `tasks/*`, owned_paths, concurrent claims.

| #   | Check              | Pass                                          | Weak / fail                         |
| --- | ------------------ | --------------------------------------------- | ----------------------------------- |
| C1  | One implement task | One implementing claim per implementer        | Two tasks; thrash                   |
| C2  | owned_paths        | Set on claim; no overlap                      | Dual claim same paths               |
| C3  | Gate chain         | implement → review → qa → done                | Self-approve; wrong qa assignee     |
| C4  | Lead as router     | Mail → tasks with AC + paths; no product code | Lead coding; mail rotting           |
| C5  | Scout loop         | Actionable mail; lead makes tasks             | Silent scout or scout edits product |
| C6  | Reject loop        | Fix listed items only; clean re-hand          | Argue; scope creep                  |
| C7  | Risk routing       | High risk → senior sparingly                  | Everything expensive / never senior |

## D. Flow (throughput + quality)

Inspect: board ages, stalled list, panes, session survival, gate batching.

| #   | Check             | Pass                                                                                                  | Weak / fail                                                                             |
| --- | ----------------- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| D1  | Board motion      | Review/qa clear in reasonable turns                                                                   | Permanent review pile                                                                   |
| D2  | Honest blocked_by | Deps updated when done; blocked ≠ stall                                                               | Stale `blocked_by` on done ids; false stalls                                            |
| D3  | Gate batching     | One non-trivial review/QA per oneshot turn                                                            | Mega-turns: 3 tasks + full verify in one call                                           |
| D4  | Test ladder       | Fast unit default; integration when surfaces need it                                                  | Always-verify or never-integration                                                      |
| D5  | Suite cost        | Default garden finishes in minutes; heavy path optional                                               | Default suite stalls QA/implementers for long turns                                     |
| D6  | Session survival  | Stays up through unit/qualify                                                                         | Dies when tests run (name collision)                                                    |
| D7  | Human gates       | Publish/release/product only                                                                          | Blocked on trivia lead could decide                                                     |
| D8  | Staffing          | Free implementer gets unblocked high-priority work                                                    | Idle implementer + unblocked queue                                                      |
| D9  | Post-epic idle    | Empty board after epic close is OK when lead woke scout (or scout mid-hunt) and mail/todo will refill | Idle implementers + empty todo **and** silent scout for >~1h with no keep-scouting wake |

**D8 vs D9:** `empty-todo-with-idle-implementer` collaboration alerts after a burn-down are **not**
automatic D8 fails. Pass D8 when the queue is honestly empty; score **D9** for whether the scout
refill loop is live (wake, mid-oneshot, or fresh mail). Class C false-dead (`await=dead` + pane
`timeout` + “starting CLI turn”) still means scout is working — see
[diagnose-downtime.md](diagnose-downtime.md).

If **D4 or D5 fails**, reworking tests is in scope for this skill — see
[improvement-playbook.md](improvement-playbook.md) “When tests stall the team”.

---

## Scorecard (handoff)

```text
Workflow: <name>   Session: UP|DOWN   When: <ISO>
Setup:          pass|weak|fail  — …
Communication:  pass|weak|fail  — …
Collaboration:  pass|weak|fail  — …
Flow:           pass|weak|fail  — …   # throughput: D1–D5, D8
Top 3 adjustments (throughput vs quality):
1. …   # may include “split/rework tests” if D4/D5 fail
Init template impact: none | …
Skill self-improve: none | …
```

Roll row scores into the four headers by judgment (one fail row → area at most weak; several fails →
fail).

**Throughput vs quality trade:** prefer more finished tasks with real gates over fewer tasks with
always-full `verify`. Failing quality is worse than slower throughput — never skip review/qa.
**Reworking the test garden** (fast vs heavy suites) is a valid throughput fix when the suite itself
is the stall.

## Cadence

| Mode     | Depth                                                   |
| -------- | ------------------------------------------------------- |
| Pulse    | Skip full scorecard; flag only glaring B/C/D issues     |
| Check-in | Full A–D                                                |
| Deep     | Full A–D + [init-templates.md](init-templates.md) audit |
