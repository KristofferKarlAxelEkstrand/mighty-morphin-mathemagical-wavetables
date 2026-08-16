## Reject budget and design ACK (E006 D9)

Stop Quality↔implement (and Tests↔implement) thrash after a hard design disagreement. This does
**not** lower the quality bar and does **not** authorize rubber-stamp approves after N rejects.

### Budget = 3 hard rejects

A **hard reject** is a Quality or Tests gate rejection that sends the task back to `implementing`
(or `blocked`) with a concrete fix list — not a nit, feedback, or self-fail before handoff.

Count hard rejects on the **same task id** that land **without** an intervening Lead **design
decision** (Lead answer in `mail/out/`, task note, or `approved` design ACK that changes the
approach family).

| Hard-reject count (no Lead design decision yet) | Next action                                                                                                                                                      |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1–2                                             | Implementer fixes the listed items; mid-reject checks stay **focused-only** (see **package-test-gates**).                                                        |
| **3**                                           | Stop blind re-implement. Move toward `blocked` and/or file a Lead `question` (design ACK). Do **not** start a fourth implement pass on the same approach family. |

Who acts at budget:

- **Implementer** — after the third hard reject lands, do not re-code the same design; `blocked` or
  Lead `question` with the open design fork; leave a self-wake only if still waiting on Lead.
- **Quality / Tests** — on the third hard reject (or when about to issue it), state that the budget
  is hit and that the next step is Lead design ACK, not another implement cycle on the same
  approach.
- **Team Lead** — answer the design question (pick approach, relax acceptance, or re-scope); record
  the decision on the task; only then re-open `implementing`. A design ACK **resets** the budget
  counter for that task.

### Threat model in security-relevant rejects

When the defect is security- or trust-boundary-relevant, every hard reject note **must** state:

1. **Attacker** — who can act (untrusted mail body, co-worker, host process, …).
2. **Required property** — what must hold (unforgeable channel, path containment, no secret in
   prompts, …).

If that property is **unsatisfiable** with the current approach family (e.g. “try another forgeable
channel”), reject into **Lead design** — do not ask the implementer for another pass on the same
family.

### Explicit anti-patterns

- **Rubber-stamp after N rejects** — forbidden. Budget exhaustion means design ACK, not “approve to
  clear the board.”
- **Full garden / full verify on every mid-reject fix** — forbidden. Use the package-test-gates
  ladder; mid-reject = focused suite (+ lint/format on touched paths) until the hand-back that
  claims the gate.

### Recording rejects (digest-friendly)

Prefer transition notes that start a body line with `Rejected:` so tooling (e.g.
collaboration-digest `reject-budget:*` alerts) can count them. One hard reject → one such marker (or
equivalent explicit count in the task note).

### Digest reset phrases (machine match)

`collaboration-digest` windows hard-reject counts after the latest design ACK in the **task body**.
It matches these substrings only (case-insensitive). Free-form ACKs that omit them do **not** reset
the window and can leave false `reject-budget:Txxx:N` alerts.

| Prefer             | Phrase (exact substring)            |
| ------------------ | ----------------------------------- |
| **Primary (Lead)** | `Lead design ACK`                   |
| Alternate          | `Design ACK (resets reject budget)` |
| Minimal            | `(resets reject budget)`            |

Write the primary form on the task when Lead records a design decision. Put the phrase in the task
body (transition note or decision line), not only in Slack. Rejects after that line count in a new
window. Rejects before it do not.
