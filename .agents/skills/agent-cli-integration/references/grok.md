# Grok Build CLI

Last checked: 2026-07-28. Installed evidence: Grok CLI 0.2.112 (stable).

## Interface

- Product key: `grok`; executable: `grok`.
- Install: `curl -fsSL https://x.ai/cli/install.sh | bash`.
- Interactive TUI is the default. Headless single-turn paths:
  - `-p` / `--single <PROMPT>` — prompt on the command line; prints and exits.
  - `--prompt-file <PATH>` — single-turn prompt from a file; exits (do **not** combine with
    `--single`).
- Auth: `grok login` (browser/OAuth), `XAI_API_KEY`, or session in `~/.grok/auth.json`.
  `grok models` prints `You are logged in…` when session auth works.
- Permissions: `--permission-mode` values
  `default | acceptEdits | auto | dontAsk | bypassPermissions | plan`, plus `--always-approve` for
  tool auto-approval.
- Model: `-m` / `--model`. Observed catalog (0.2.112): `grok-4.5`.
- Effort: `--reasoning-effort` / `--effort`. office-space preflight allows the observed model-menu
  tiers only: `low`, `medium`, `high` (broader values in generic help are not accepted until proven
  for the selected model).
- Sessions: `--continue`, `--resume`, `grok sessions list`.
- Cwd: `--cwd` optional; cwd alone is used for project discovery in practice.
- Auto-update: no CLI flag on 0.2.x. For unattended hosts set `[cli] auto_update = false` in
  `~/.grok/config.toml`.

## office-space mapping

- Classified as **oneshot**. Launch uses `--prompt-file` so the process exits after one turn; the
  shell loop owns `intercom` (mailbox wait/poller).
- Unattended default permission mode: `bypassPermissions`.
- Effort is native-flag (`--reasoning-effort`); valid values `low|medium|high`.
- Auth status prefers `grok models` “logged in” text over bare `~/.grok/auth.json` presence
  (`XAI_API_KEY` short-circuits as env token).
- Activity currently returns an unsupported stub (no checkout-scoped inventory adopted yet;
  `grok sessions list` exists for future work).

## Verify before changing

Confirm installed version, that `--prompt-file` still exits without a TTY, permission-mode vs
`--always-approve` interaction on tool-heavy turns, model list parse shape, effort tiers vs the live
model menu, and whether a stable session inventory can drive activity probes without cross-checkout
confusion.
