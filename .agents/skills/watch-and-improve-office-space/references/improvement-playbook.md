# Improvement playbook

After watch + evaluate (+ downtime diagnosis if needed), apply the **smallest durable fix**. Cap
**≤3** adjustments per check-in unless the user asked for deep work.

## Priority

1. **Safety** — do not kill the dogfood session
2. **Diagnosability** — next death is explainable
3. **Scorecard fails** — setup / communication / collaboration / flow
4. **Test garden rework** — when the suite itself stalls the team (§ below)
5. **Init templates** — general lessons only ([init-templates.md](init-templates.md))
6. **This skill** — ([self-improve.md](self-improve.md))
7. Other docs

## Safety: test isolation

Session names are **host-global**. Never:

```text
stop_team "developer-team"
team stop developer-team
run-team --stop developer-team
```

from a test that shares the default tmux server.

**Do:**

```js
const workflow = `tr${randomUUID().replaceAll("-", "")}`;
// init --workflow … (lead + reviewer + qa)
// OFFICE_SPACE_ROOT = temp tree
// optional: private tmux (TMUX_TMPDIR + unset TMUX) — tmux-automation
```

Optional assert: `developer-team-agents` has-session status unchanged.

## Scorecard → surfaces

| Area          | Fix surfaces                                                                       |
| ------------- | ---------------------------------------------------------------------------------- |
| Setup         | `co-workers/*`, `WORKFLOW.md`, `space.json`, models, runners                       |
| Communication | messaging / mailbox partials; lead triage; false stall monitor                     |
| Collaboration | owned_paths, task-transition, Own/Never, lead routing                              |
| Flow          | blocked_by honesty, gate batching, **test ladder / suite shape**, session survival |

| Score | Action                                                           |
| ----- | ---------------------------------------------------------------- |
| pass  | Leave alone                                                      |
| weak  | One small live fix **or** file nit/mail                          |
| fail  | Stop bleeding; file bug/task with acceptance; fix `src/` if code |

## When tests stall the team — rework the garden

If check-in shows **QA or implementers blocked by suite cost** (not by product bugs), changing the
**test layout and scripts** is a first-class improvement — not “only product code.”

**Signals (evidence):**

- `tests` oneshot turns run 15–30m on full `verify` / full unit for routine tasks
- `qa` queue piles while one agent re-runs the same heavy suite
- Live dogfood dies mid-QA because tests call `stop_team` on the live workflow name
- Agents avoid running checks, or always-run everything “to be safe”
- Default `test:unit` includes multi-second tmux/poller/controller loops every time

**Valid reworks (pick the smallest that restores throughput without dropping quality):**

1. **Split fast vs heavy** — e.g. `*.integration.test.js` excluded from default unit;
   `test:unit:integration` / `test:unit:all` for heavy run-team/tmux/poller cases (this package’s
   pattern).
2. **Tighten env-sensitive waits** — configurable poll intervals for controllers in tests; shorter
   timeouts when behavior is still proven.
3. **Isolate side effects** — unique workflow names / private tmux so garden work never kills
   dogfood.
4. **Teach the team** — WORKFLOW + co-worker partials: when to use fast vs heavy vs `verify`
   (package-test-gates).
5. **File follow-ups** — if rework is large, ship the split first, then tasks for remaining suite
   debt.

**Do not:**

- Delete coverage that guards real regressions just to go green faster
- Leave only a slow path with no documented fast path for day-to-day
- Skip gates — rework _which_ command runs by default, not whether review/qa exist

After rework: update co-worker prompts / WORKFLOW if agents still invoke the old “always verify”
habit.

## Live vs templates vs package

| Kind               | Live `.agents/office-space/<wf>/` | `src/templates/` + init map | `src/` runtime  |
| ------------------ | --------------------------------- | --------------------------- | --------------- |
| Dogfood-only       | yes                               | no                          | if bug          |
| Universal doctrine | yes (now)                         | **yes** (next init)         | rare            |
| Package bug        | —                                 | only if scaffold wrong      | **yes** + tests |

## While the team is live

**Do:** file findings to `mail/in/`; fix dual-claim / false stall process; shorten noisy prompts;
`run-team --restart <wf> <agent>` after a prompt fix.

**Do not:** full `team start` “to refresh”; poorly isolated tmux unit tests; hand-edit `dist/` or
generated skill mirrors; rewrite every prompt.

## Verify (this package)

- Prefer focused: `npm run test:unit -- <file>`
- Day-to-day full garden: `npm run test:unit` (excludes integration **and** `test/release/**` E005
  soaks)
- run-team / tmux / poller / controller: also `npm run test:unit:integration`
- Full unit+integration: `npm run test:unit:all` (what `verify` uses; still no release soaks)
- E005 qualification only: `npm run test:unit:release`
- Prefer `node src/cli.js` over stale installed bins
- `npm run validate:skills` if this skill changed
- Dogfood co-workers: partial `package-test-gates` + WORKFLOW §6.1

## Done when

- Scorecard written on check-in/deep (even if all pass)
- Each fail/weak → fix, filed work, or explicit deferral
- Init impact stated
- Skill self-review done on check-in/deep
- User knows UP/DOWN, changes, open items
