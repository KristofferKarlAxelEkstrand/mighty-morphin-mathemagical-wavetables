# Source ledger

Last researched: 2026-07-31. Re-open volatile sources after 30 days, after a meaningful
installed-version change, or when installed help disagrees.

## Claude Code

- [CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage) — interactive versus
  print mode, prompt I/O, output, sessions, models, and permissions.
- [Permissions](https://docs.anthropic.com/en/docs/claude-code/permissions) — permission modes, tool
  rules, and managed controls.
- Local `claude --version` and `claude --help` — installed interface authority; observed 2.1.220
  with `--print`, `--permission-mode`, and `--prompt-suggestions` on 2026-07-31.
- Detached private-tmux comparison on 2.1.220 — authenticated stdin turn stayed in the interactive
  REPL without `--print` and exited 0 with `--print`.

## OpenAI Codex

- [CLI command reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli) — `exec`,
  JSONL, resume, flags, and maturity.
- [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) — automation,
  authentication, and output.
- [Approvals and sandboxing](https://learn.chatgpt.com/docs/agent-approvals-security) — approval
  policy, sandbox combinations, and security boundaries.
- [Configuration](https://learn.chatgpt.com/docs/config-file/config-basic) — config precedence,
  project trust, models, and effort.
- Local `codex --version`, `codex exec --help`, and app-server behavior.

## Devin CLI

- [Documentation index](https://docs.devin.ai/llms.txt) — discover current CLI and product pages
  before relying on a remembered URL.
- [CLI skills overview](https://docs.devin.ai/cli/extensibility/skills/overview) — CLI skill
  behavior.
- [Product skills](https://docs.devin.ai/product-guides/skills) — canonical paths, invocation,
  discovery, and product limitations.
- Local `devin --version`, `devin --help`, and `devin list --help`.

## GitHub Copilot CLI

- [Command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)
  — modes, flags, permissions, sessions, configuration, and environment.
- [Programmatic reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-programmatic-reference)
  — non-interactive operation and auditing considerations.
- [Autopilot](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/autopilot) — autonomy
  versus permissions and continuation limits.
- Local `copilot --version` and `copilot --help`.

## Cursor Agent

- [CLI overview](https://docs.cursor.com/en/cli/overview) — interactive, non-interactive, and
  session surfaces.
- [CLI parameters](https://docs.cursor.com/en/cli/reference/parameters) — command and flag
  reference.
- [Headless mode](https://docs.cursor.com/en/cli/headless) — print-mode automation and documented
  `--force` behavior.
- [Permissions](https://docs.cursor.com/en/cli/reference/permissions) — project/global allow and
  deny policy.
- [Output format](https://docs.cursor.com/en/cli/reference/output-format) — JSON and stream-JSON
  schemas.
- Local `cursor-agent --version` and `cursor-agent --help`.

## Antigravity CLI

- [CLI getting started](https://antigravity.google/docs/cli-getting-started) — official installation
  and CLI overview.
- [Google hands-on codelab](https://codelabs.developers.google.com/antigravity-cli-hands-on) —
  authentication, trust, settings, print mode, and model selection.
- [Google structured-workflow codelab](https://codelabs.developers.google.com/sdd-agy-cli) — current
  CLI help surface, skills, and MCP workflow.
- Local `agy --version`, `agy --help`, `agy models`, and `agy changelog`.

## Grok Build CLI

- Install script and product entry: [x.ai CLI install](https://x.ai/cli/install.sh) (via
  `curl -fsSL https://x.ai/cli/install.sh | bash`).
- Bundled local README at `~/.grok/README.md` after install — headless mode, auth (`grok login`,
  `XAI_API_KEY`), permissions, sessions.
- Local `grok --version`, `grok --help`, `grok models`, `grok login --help` (observed 0.2.112 on
  2026-07-28).

## Repository primary sources

- `src/known-clis.json` — logical CLI keys.
- `src/lib/cli-tools.sh` — binaries, supported set, permissions, effort, authentication, and model
  discovery.
- `src/persistent-clis.json` — office-space lifecycle classification.
- `src/run-team` — command construction, waiting, preflight, and tmux launch.
- `src/generate-prompt.js` — lifecycle-specific mailbox instructions.
- `src/lib/cli-activity/` — activity inventory and unsupported boundaries.
- `test/cli-tools.test.js`, `test/run-team.test.js`, and `test/generate-prompt.test.js` — executable
  repository expectations.

## Evidence notes

- Official Cursor pages have described print-mode write behavior differently. Installed-version
  experiments must decide runtime behavior.
- No stable public Devin page was found for every installed 3000.2.17 flag. Installed help is
  primary evidence for those exact flags; retain uncertainty.
- Antigravity is evolving quickly. Prefer the installed changelog and Google documentation over
  community summaries.
