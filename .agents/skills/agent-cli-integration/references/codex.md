# OpenAI Codex

Last checked: 2026-07-26. Installed evidence: codex-cli 0.145.0.

## Interface

- Binary: `codex`; `codex exec` is the stable non-interactive surface.
- `codex exec --json` emits JSONL events and supports session resume.
- Sandbox and approval policy are independent. `workspace-write` or `read-only` with
  `approval_policy="never"` rejects unavailable escalation;
  `--dangerously-bypass-approvals-and-sandbox` removes both boundaries.
- Model effort is a config value (`model_reasoning_effort`), not a portable model-name convention.
- Codex discovers applicable `AGENTS.md` files and trusted project `.codex/config.toml` layers.

## office-space mapping

- Classified as oneshot; the shell loop owns mailbox waiting.
- Launch uses `codex exec --json ... -` and `src/lib/codex-launch.js`. The wrapper requires the
  first valid `thread.started` event, stores the authoritative thread id, and renders concise
  assistant output.
- Activity uses Codex app-server thread inventory and the captured binding.
- Supported permission modes intentionally distinguish full access, workspace-write, and read-only.

## Verify before changing

Keep JSON event parsing version-aware. Test malformed/missing `thread.started`, non-zero pipeline
propagation, protected paths, project trust, session binding, and thread matching across two
checkouts.
