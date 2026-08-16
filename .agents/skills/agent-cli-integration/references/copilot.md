# GitHub Copilot CLI

Last checked: 2026-07-26. Installed evidence: GitHub Copilot CLI 1.0.75.

## Interface

- Binary: `copilot`.
- `-p`/`--prompt` runs non-interactively and exits. Text and JSONL output are available; `--silent`
  removes presentation noise.
- Sessions can be named, continued, resumed, or addressed by exact id.
- Permission dimensions include tools, filesystem paths, and URLs. `--allow-all`/`--yolo` covers all
  three; `--allow-all-tools` does not.
- `--no-ask-user` prevents model questions but is separate from tool approval.
- Prompt mode may suppress repository hooks, workspace MCP, or extensions unless trusted or
  explicitly enabled.

## office-space mapping

- Classified as oneshot; the shell loop owns mailbox waiting.
- Current launch passes prompt text as the `--prompt` argument.
- Current unattended default is `allow-all-tools`. This satisfies the CLI's documented tool
  requirement but is not equivalent to full unattended path and URL access. Audit real tasks before
  choosing a safer scoped policy or the broader `allow-all`.
- Activity currently returns an unsupported stub because available foreign session surfaces are not
  a stable activity inventory.

## Verify before changing

Test repository writes, shell commands, outside-root paths, URL access, `ask_user`, workspace
MCP/hooks, JSONL completion, and session selection. Keep managed-policy rejection distinct from an
office-space launch bug.
