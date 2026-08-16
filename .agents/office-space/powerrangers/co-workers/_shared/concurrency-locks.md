## Shared Environment & Concurrency

You share one working tree with the other agents. Do not step on their toes.

- **Path reservations.** Active tasks declare `owned_paths`. Use the host task-transition tool for
  claims and handoffs; overlapping paths are rejected atomically — the loser re-picks. Only a task's
  current assignee may edit its reserved paths, and only while its config carries the capability
  that permits those edits. Agents with `implementer: true` may own implementation work; review/QA
  inspect without releasing the lock. Stage `implementing` requires an agent with
  `implementer: true` (`--assignee auto-implementer`), stage `review` requires an agent with
  `reviewer: true` (`--assignee auto-reviewer`), and stage `qa` requires an agent with `qa: true`
  (`--assignee auto-qa`). Auto-assignment chooses the least-loaded enabled agent with that
  capability. Wakes go only to the new assignee.
- **Path release (two triggers).** Runtime clears live `owned_paths` so another task can claim those
  paths. Task identity, assignee, and evidence stay. Follow the host mission WORKFLOW path-release
  policy when present.
  - **Enter `qa`.** On transition to `qa`, when no further product edits are expected (v1 default).
  - **Verified →`done`.** On transition to `done` with live locks still held, when the close is not
    a runner fast-path (for example thin review→done that never entered `qa`).
  - **Runner fast-path →`done`.** Unverified. Does not use this path-release contract.
  - **Re-reserve** before editing product paths after release; overlap rejection still applies while
    reserved.
  - **No content fingerprint at done.** Peer re-touch of released paths does **not** bounce the task
    back through implement/review. Tests still run the task's evidence ladder. Release or publish
    uses the host's configured release gate, not per-task fingerprints.
  - **Intentional deletions.** Keep the deleted path in `owned_paths` / `released_owned_paths`
    history and list its exact repository-relative path in `deleted_paths`. Closure accepts only a
    path that is absent and inside that declared scope. Unmarked missing paths and existing, broken,
    or escaping symlinks still fail closed.
- **Long or shared checks.** Before starting a long integration, runtime, packaging, or release
  check, consult the host's `WORKFLOW.md`, `space.json`, and any configured locks for concurrency,
  queueing, and result-reuse rules. Follow them exactly; if the host has no rule, ask the lead
  rather than assume a default.
- **Package installs.** Never install a new dependency yourself. Send a message describing what you
  need to the lead's `slack/` folder (`slack/{{lead}}/`). Only the agent with `lead: true` is
  authorized to install.
- **Build-directory locks.** If your project provides locked wrappers (per-directory build locks or
  caps on concurrent heavy builds), prefer them over bare build commands — they dedup unchanged
  builds, serialize callers, and return structured reports.
- **Result reuse.** Before reusing a previous test, build, or verification result, confirm the host
  allows reuse and that the freshness and source rules are met. Do not reuse a result when the host
  forbids reuse or has no policy.
- **Broken environment.** If you find a broken global dependency or environment problem, do not
  quietly fix it. Send a `blocked` message to the lead so the fix is assigned explicitly.
