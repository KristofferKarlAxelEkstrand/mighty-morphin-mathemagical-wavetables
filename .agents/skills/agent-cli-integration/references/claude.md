# Claude Code

Last checked: 2026-07-31. Installed evidence: Claude Code 2.1.220.

## Interface

- Binary: `claude`.
- Interactive mode is the default. `-p`/`--print` is the documented non-interactive,
  exit-after-response mode.
- Print mode supports text, JSON, and stream-JSON output, plus session continuation/resume and
  explicit session ids.
- Relevant permission controls include `--permission-mode`, `--dangerously-skip-permissions`, tool
  allow/deny lists, and organization or settings policy.
- Claude reads `CLAUDE.md`; this repository supplies the required `@AGENTS.md` shim. Skills need the
  `.claude/skills` discovery bridge.

## office-space mapping

- Logical CLI and executable are both `claude`.
- Classified as oneshot, so the shell loop owns `intercom` (mailbox wait/poller).
- Launch redirects the generated prompt to stdin and passes `--print`, making the
  exit-after-response lifecycle explicit. A detached tmux reproduction on 2.1.220 showed the same
  authenticated prompt remained in the interactive REPL without `--print` but exited successfully
  with it.
- `bypassPermissions` is the configured unattended default. Validate that managed policy permits it
  and that the flag maps to the installed version.
- Activity uses Claude's scriptable agent/session inventory and a durable office-space binding.

## Verify before changing

Run both a no-edit and workspace-edit task in a disposable repo. Confirm exit, session id, output
shape, stdin handling, permission behavior, and activity inventory for the installed version.

Observed on 2.1.220: `--print` accepts stdin with `--permission-mode bypassPermissions` and exits
after the turn. The repository regression also requires that command shape before its stub performs
a workspace-edit tool call. Interactive prompt suggestions are not a completion signal; process exit
remains the shell-owned oneshot contract.
