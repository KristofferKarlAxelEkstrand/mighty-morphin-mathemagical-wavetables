# Antigravity CLI

Last checked: 2026-07-26. Installed evidence: Antigravity CLI 1.1.7.

## Interface

- Product key: `antigravity`; executable: `agy`.
- `--prompt-interactive` supplies an initial prompt and continues the TUI. `--print` is the
  exit-after-response automation path.
- `--add-dir` is required to make an intended repository an explicit workspace; cwd alone has not
  been reliable for office-space.
- Conversations support continue and resume by id.
- Permission controls include unrestricted `--dangerously-skip-permissions`, `accept-edits`, `plan`,
  and optional sandboxing.
- Effort may be a native flag or encoded in a model id. Passing both for an encoded model can fail
  resolution and fall back to another model.

## office-space mapping

- Classified as oneshot, so the shell loop owns `intercom` (mailbox wait/poller). Launch pins the
  repository with `--add-dir` and uses `--print "$(cat prompt_file)"`, which exits after the turn.
- `dangerously-skip-permissions` is the unattended default.
- Activity currently returns an unsupported stub because no stable list plus activity interface has
  been adopted.
- Previously classified persistent (`--prompt-interactive`, agent self-backgrounds `intercom` via
  `sleep-step`). Reclassified to oneshot after a live `developer-team` team showed the
  self-backgrounded watcher did not survive turn exit (0/11 processes alive, reproduced 0/8 after a
  full team restart) — see `office-space-integration.md` A3.

## Verify before changing

Confirmed on this pass: `agy --print '<text>'` exits 0 with clean text output (~6s for a trivial
prompt); `--add-dir` plus `"$(cat prompt_file)"` matches the shell-expansion idiom already proven
safe for `--prompt-interactive`.

Still open: `--print-timeout` behavior on a long/stuck turn, `--output-format` alternatives
(json/stream-json), conversation-id continuity across oneshot turns (each turn is now a fresh
process, matching Claude/Codex policy — see office-space-integration.md A5), signal handling, and
whether a stable activity inventory has appeared.
