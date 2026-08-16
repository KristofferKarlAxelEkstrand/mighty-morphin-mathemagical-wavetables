# Devin CLI

Last checked: 2026-07-31. Installed evidence: devin 3000.3.22. Contract re-verified unchanged
(prompt-file/print, `devin list --format json`, `devin models list --format json`).

## Interface

- Binary: `devin`.
- `--prompt-file ... --print` is a non-interactive, exit-after-task path.
- The CLI exposes `--continue` and `--resume`; print mode does not respect workspace trust by
  default unless explicitly requested.
- Permission modes range from read-oriented `auto` through `accept-edits` and `smart` to
  unrestricted `dangerous`. Optional sandboxing enforces active read/write scopes at OS level.
- Devin supports a strict agent definition file and discovers repository skills, with
  `.agents/skills` the recommended canonical path.

## office-space mapping

- Classified as oneshot. This replaced persistent treatment because installed 3000.2.17 stalled when
  mailbox wake text was typed into the live TUI.
- Launch uses a prompt file plus `--print`; the shell loop owns waiting.
- `dangerous` is the unattended default. Keep its broader authority explicit.
- Activity uses `devin list --json` and a durable session binding.

## Verify before changing

Re-test persistent versus print behavior after meaningful CLI upgrades. Confirm prompt-file parsing,
workspace trust, session inventory, sandbox scopes, exit codes, and whether resume is safe for
repeated mailbox turns.

**Rate limits (observed, undocumented by vendor):** `devin --print` can return
`Error: Agent error: ... Reached overall message rate limit.` with exit code 0 (masked success)
unless the oneshot loop's quota/rate-limit detector treats that output pattern as a real failure and
cools down instead of re-arming immediately. No Devin-published concurrent-session or
requests-per-minute ceiling has been found in this research pass — treat any specific number as
`unknown`, not inferred from one observation. Hosts running several resident agents on the same
Devin account should expect this is a live risk, not hypothetical.
