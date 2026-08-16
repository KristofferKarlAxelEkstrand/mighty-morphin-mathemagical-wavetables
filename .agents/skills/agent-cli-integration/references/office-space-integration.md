# office-space integration and audit

Audit date: 2026-07-31. Scope: the seven entries in `src/known-clis.json`. This is an
evidence-backed baseline, not authorization to change runtime defaults.

## Current matrix

| CLI         | Binary         | Lifecycle  | Prompt transport      | Unattended default   | Activity         |
| ----------- | -------------- | ---------- | --------------------- | -------------------- | ---------------- |
| Claude      | `claude`       | oneshot    | stdin + print         | `bypassPermissions`  | dedicated        |
| Codex       | `codex exec`   | oneshot    | stdin + JSONL wrapper | `danger-full-access` | dedicated        |
| Devin       | `devin`        | oneshot    | prompt file + print   | `dangerous`          | dedicated        |
| Copilot     | `copilot`      | oneshot    | `--prompt` argument   | `allow-all-tools`    | unsupported stub |
| Cursor      | `cursor-agent` | persistent | TUI initial argument  | `force`              | unsupported stub |
| Antigravity | `agy`          | oneshot    | `--print` argument    | skip permissions     | unsupported stub |
| Grok        | `grok`         | oneshot    | `--prompt-file`       | `bypassPermissions`  | unsupported stub |

Lifecycle is a protocol decision:

- oneshot: office-space runs CLI → CLI exits → harness runs `intercom` → next fresh CLI turn;
- persistent: the TUI remains alive and the agent backgrounds/re-arms `intercom` itself.

(`intercom` is the wait/poller process — internal office-space name, not Intercom.com.
`await-messages.js` remains a silent compat alias for one package minor.)

Changing the classification requires coordinated changes to `persistent-clis.json`, prompt
generation, launch commands, health/restart logic, and tests.

## Findings

### A1 — Claude oneshot mode is explicit

- Evidence: Claude Code 2.1.220 remained at its interactive REPL after a completed detached tmux
  turn with no clients. The same authenticated stdin prompt exited successfully with `--print`; a
  no-edit plus workspace-edit regression covers the `bypassPermissions` launch contract.
- Status: **resolved; `src/run-team` now passes `--print`**.
- Boundary: office-space still starts a fresh Claude process per wake. The shell loop detects
  process exit, then runs `intercom`; it does not parse Claude output or prompt suggestions as
  completion.

### A2 — Copilot default is not full unattended authority

- Evidence: current help defines `--allow-all` as tools + paths + URLs, while `--allow-all-tools`
  covers tools only. office-space defaults to the latter.
- Status: **confirmed semantic mismatch in comments/default naming; runtime impact is
  task-dependent**.
- Risk: a worker may stop or fail when a task needs an unapproved path or URL.
- Recommendation: define intended authority first. Prefer scoped allowlists where practical;
  otherwise use `allow-all` and name the security tradeoff. Also evaluate `--no-ask-user`
  separately.

### A3 — Persistent Cursor and Antigravity have one-shot alternatives

- Evidence (Antigravity): a live `developer-team` team observed with all 11 agents idle at the
  `--prompt-interactive` REPL — every agent had completed a real, correct turn and reported
  launching its self-backgrounded `nohup … intercom.js … & disown` watcher per `sleep-step`, but
  zero watcher processes were found alive afterward. Reproduced twice independently (once before,
  once immediately after a full team restart): 0/11 then 0/8 survival. `agy --print '<text>'` was
  confirmed to exit 0 with clean text output.
- Status (Antigravity): **resolved; `src/run-team` now passes `--print`** and `persistent-clis.json`
  reclassifies antigravity as oneshot, matching A1's Claude fix. The shell loop now owns the
  intercom wait between turns instead of the agent backgrounding it inside its own turn.
- Status (Cursor): **design tradeoff, not a defect** — still open, not evaluated. Cursor's
  self-backgrounding has not been observed to fail; do not assume A3's Antigravity finding transfers
  without its own bake-off.
- Risk (Cursor): persistent operation depends on correct in-model backgrounding and re-arming;
  oneshot operation loses native conversation continuity and adds cold starts.
- Recommendation (Cursor): bake off mailbox wake reliability, context continuity, latency,
  timeout/cancellation, and recovery before changing.

### A4 — Four activity adapters are unsupported

- Evidence: `src/lib/cli-activity/adapters/stub.js` returns unsupported for Copilot, Cursor,
  Antigravity, and Grok.
- Status: **confirmed observability limitation**.
- Risk: health decisions rely more heavily on pane and poller evidence and cannot distinguish all
  idle/active session states.
- Recommendation: adopt only stable, checkout-scoped inventories. Do not infer activity from a
  global “latest session” or use control-plane APIs as foreign session observation. Grok exposes
  `sessions list` for a future inventory.

### A5 — Fresh turns versus native resume is undocumented policy

- Evidence: all seven CLIs expose continuation/resume, while office-space oneshot loops generally
  create a fresh CLI process without resuming its prior native session.
- Status: **intent/policy gap**.
- Risk: fresh turns bound hidden harness state but may repeat discovery and lose useful context;
  resume improves continuity but can accumulate stale state and complicate binding/recovery.
- Recommendation: preserve fresh turns until a task demonstrates a measurable benefit. Document
  prompts, memory logs, tasks, and records as the portable continuity layer; evaluate native resume
  per CLI rather than globally.

## Prioritized follow-ups

1. Choose and test the Copilot permission contract from A2.
2. Document fresh-turn policy in user/runtime docs after validating A5.
3. Run a Cursor lifecycle bake-off for A3 (Antigravity resolved).
4. Investigate stable activity APIs for A4 without blocking other improvements.

Each runtime follow-up must identify owned paths and pass `developer-team` implementation → review →
QA. Existing edits in `src/run-team` and activity code belong to active work and must not be
overwritten.
