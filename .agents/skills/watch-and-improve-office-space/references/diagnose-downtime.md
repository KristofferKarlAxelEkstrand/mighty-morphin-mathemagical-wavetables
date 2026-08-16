# Diagnose downtime

Use when the workflow session is down, an agent flaps, or status looks “all dead” while panes are
busy.

Paths below are relative to `.agents/office-space/<workflow>/` unless noted.

## Signals

| Signal               | Where                                                 | Meaning                                             |
| -------------------- | ----------------------------------------------------- | --------------------------------------------------- |
| Status grid          | `node src/cli.js team status <wf>`                    | await / cli / board / pane / stagnation             |
| Session              | `tmux has-session -t <wf>-agents`                     | whole team present or gone                          |
| Panes                | `tmux list-panes -t <wf>-agents -s -F '…'`            | `timeout` ≈ oneshot mid-turn; `node` often intercom |
| Pane text            | `tmux capture-pane -t <wf>-agents:agents.N -p -S -40` | progress, exit lines                                |
| Restarts             | `health/uptime.log`                                   | `restart`, `flap`, `recovered`, `suspected-hung`    |
| Alerts               | `health/alerts/*.json`                                | flap left down for human                            |
| Heartbeats           | `health/heartbeats/<agent>.json`                      | poller pid; `999999999` = launch stamp              |
| Await locks          | `.temp/.await-lock-*.json`                            | LIVE if `kill -0 $pid`                              |
| Binding / stop audit | `health/session-binding.log`                          | resolve failures; `stop_team` lines                 |
| Reports              | `health/reports/`                                     | monitor narrative                                   |
| Ctrl                 | `office-space ctrl` → **q** / **r**                   | intentional stop / restart                          |

Always key off **`<workflow>-agents`**, not “any tmux session changed.”

## Classes

### A — Whole session gone

**Symptoms:** no `<wf>-agents`; all panes gone; await locks DEAD; often **no** new `uptime.log`
restart lines.

**Almost always `stop_team`:**

1. Human / ctrl **q** / `team stop`
2. `team start` or ctrl **r** (starts with `stop_team`)
3. Test: `stop_team "<live-wf-name>"` (classic: `developer-team` inside unit tests)
4. Failed mid-start (“stopping incomplete session”)

**Prove (3):**

```bash
grep stop_team health/session-binding.log | tail
pgrep -af 'vitest|test:unit|run-team --stop|stop_team'
```

**Fix:** isolate tests ([improvement-playbook.md](improvement-playbook.md)); then `team start` if
the user wants the team back.

### B — Single-agent flap

**Symptoms:** session still up; `uptime.log` restart → `flap`; `health/alerts/<agent>.json`.

**Causes:** CLI auth / rate limit; bad model id; prompt exits immediately; launch stuck interactive.

```bash
tmux capture-pane -t <wf>-agents:agents.<i> -p -S -80
jq '{cli,model,permission_mode,reasoning_effort,enabled}' \
  co-workers/<agent>.prompt.json
```

**Fix:** auth/model/prompt; then `bash src/run-team --restart <wf> <agent>`.

#### Claude finishes a turn but stays in an idle REPL

**Signature:** pane text shows the agent's clean end-of-turn summary, then Claude's interactive
prompt with unsubmitted suggested text. `await` is dead, `pane_current_command` remains `claude`,
and heartbeat age climbs. A detached pane with no tmux clients rules out a human typing the
follow-up.

**Cause:** the Claude launch omitted `--print`, so stdin supplied the first prompt but the CLI
retained its interactive REPL after answering. Prompt suggestions are UI text, not another
office-space wake.

**Fix:** upgrade to a launcher that passes `--print`, then
`bash src/run-team --restart <wf> <agent>`. On an older launcher, attach and press Ctrl-C before
detaching as a temporary recovery; do not synthesize Escape/Enter in automation.

### C — False “dead” (session up)

| Observation                                                     | Do                                                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| pane `timeout`, “starting CLI turn”                             | Wait — oneshot mid-turn                                                                                                                                                                                                                                                                                                                                              |
| `cli=unsupported`                                               | Expected for stub probes; no CLI busy/idle                                                                                                                                                                                                                                                                                                                           |
| await dead + assigned work during long review                   | Wait unless CLI process is gone                                                                                                                                                                                                                                                                                                                                      |
| Heartbeat age climbing mid-turn                                 | Launch stamp until intercom                                                                                                                                                                                                                                                                                                                                          |
| **`await=never` + pane `timeout` + assigned work**              | Usually **post-respawn mid-oneshot**: launch wipes `health/heartbeats/<agent>.json`; stale `.await-lock-*.json` still points at a dead old poller. **capture-pane** — if CLI is progressing, do **not** restart. Status/monitor should **not** alert `await-dead-with-assigned-work` while pane is busy (`classifyStagnation` treats paneBusy/cliActive as mid-turn) |
| Status “never” right after `run-team --restart` / pane relaunch | Same — wait for first intercom cycle after the turn                                                                                                                                                                                                                                                                                                                  |

**Do not restart** on class C alone.

### D — Orphan pollers

Status mentions pollers that outlived the session.  
**Fix:** `node src/cli.js team stop <wf>` (reaps), then start if needed.

## Test-garden vs product

Before filing a product bug from a failed team-start / run-team test:

- Re-run clean env (`env -u FORCE_COLOR …`) — colored output has broken `jq --argjson`.
- Confirm the test uses an **isolated** workflow name so it is not side-effect of killing dogfood.

## Commands

```bash
node src/cli.js team status <wf>
node src/cli.js team start <wf>     # --ensure semantics; no-op if up
node src/cli.js team stop <wf>
bash src/run-team --ensure <wf>
bash src/run-team --restart <wf> <agent>
```

Prefer `src/` while developing this package.
