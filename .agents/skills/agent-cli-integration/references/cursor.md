# Cursor Agent

Last checked: 2026-07-26. Installed evidence: cursor-agent 2026.07.23-e383d2b.

## Interface

- Product key: `cursor`; executable: `cursor-agent`.
- Interactive mode accepts an initial prompt and retains a TUI session.
- `--print` provides text, JSON, or stream-JSON automation and exits.
- `--force`/`--yolo` auto-approves commands unless denied; project and global permission files can
  narrow access. Official pages have differed on whether print mode alone writes files, so test the
  installed build.
- `--workspace` pins the root. Sessions support continue and resume by chat id.
- Cursor reads its rules plus root `AGENTS.md`/`CLAUDE.md`; skill discovery should be verified on
  the installed version.

## office-space mapping

- Classified as persistent. office-space launches a workspace-pinned TUI with the generated prompt;
  the agent backgrounds `intercom` between turns.
- `force` is the unattended default.
- Activity currently returns an unsupported stub: there is no adopted, scriptable inventory for the
  tmux-resident session.
- Cursor also supports print mode. Compare persistent and oneshot operation under real mailbox wakes
  before changing classification, because the choice also changes generated sleep instructions.

## Verify before changing

Test workspace trust, file edits, denied commands, prompt delivery, await re-arming, resume ids,
structured output, TUI survival, and interruption.
