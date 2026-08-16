# Decision: Grok-only lineup (2026-08-15)

The `powerrangers` co-workers run on the `grok` CLI.

## Why

- `devin` is not installed in this workspace. The init default (`cli: devin`, `swe-1-7`) cannot
  launch.
- `claude` is installed and not logged in (`claude -p` returns "Not logged in").
- `grok` is logged in. Live models: `grok-4.6` (default), `grok-4.5`.

## Assignment

| Agent | Model | Effort |
| --- | --- | --- |
| team-lead | grok-4.5 | medium |
| dev-1 | grok-4.6 | high |
| quality | grok-4.6 | high |

The office-space seed catalog lists `grok-4.5` only. `grok-4.6` comes from live `grok models`.
If preflight rejects `grok-4.6`, omit `model` and use the CLI default.

## Revisit

After `claude /login`, move Quality to `cli: claude` and `opus` (or `sonnet`) so review is a
different model family. Run `office-space models audit` before that change.

Thin lineup stays: lead + one implementer + combined reviewer/qa.
