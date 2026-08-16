---
name: agent-cli-integration
description: >-
  Research, add, audit, and debug office-space integrations for Claude Code, Codex, Devin, GitHub
  Copilot CLI, Cursor Agent, Antigravity CLI, and Grok Build CLI. Use when changing harness launch
  commands, permissions, sessions, prompt transport, activity probes, model flags, workspace
  handling, or supported agent CLIs.
---

# Agent CLI Integration

Integrate the harness actually installed, not a remembered interface.

## Do this

1. Run `node .agents/skills/agent-cli-integration/scripts/probe-agent-clis.mjs`.
2. Read [references/research-method.md](references/research-method.md), then the target CLI
   reference.
3. Compare three layers separately: current official docs, installed CLI `--help`/`--version`, and
   office-space launch/monitor code.
4. Read [references/office-space-integration.md](references/office-space-integration.md) before
   changing lifecycle, permissions, prompt transport, or activity probes.
5. Validate binary, authentication, workspace, prompt I/O, session behavior, permissions, output,
   exit/signal behavior, and observability together.
6. Update the dated source ledger and target reference with evidence. Mark unknowns; never turn an
   experiment into a universal claim.
7. Keep runtime fixes in `src/`, add focused tests, and follow the `developer-team` review and QA
   gates.

## Load when

| File                                                                             | Open when                                    |
| -------------------------------------------------------------------------------- | -------------------------------------------- |
| [references/research-method.md](references/research-method.md)                   | Researching or refreshing any CLI            |
| [references/office-space-integration.md](references/office-space-integration.md) | Auditing or changing shared runtime behavior |
| [references/claude.md](references/claude.md)                                     | Working on Claude Code                       |
| [references/codex.md](references/codex.md)                                       | Working on OpenAI Codex                      |
| [references/devin.md](references/devin.md)                                       | Working on Devin CLI                         |
| [references/copilot.md](references/copilot.md)                                   | Working on GitHub Copilot CLI                |
| [references/cursor.md](references/cursor.md)                                     | Working on Cursor Agent                      |
| [references/antigravity.md](references/antigravity.md)                           | Working on Antigravity CLI (`agy`)           |
| [references/grok.md](references/grok.md)                                         | Working on Grok Build CLI (`grok`)           |
| [references/sources.md](references/sources.md)                                   | Refreshing claims or adding a CLI            |

Model selection belongs to sibling `model-chooser`. Skill discovery paths and bridges belong to
sibling `share-skills`.

## Gotchas

- Product name is not always the executable: Cursor is `cursor-agent`; Antigravity is `agy`.
- “Interactive”, “print”, and “persistent” are CLI semantics. office-space's persistent/oneshot
  classification also controls who owns mailbox waiting.
- An auto-approve flag may cover tools but not paths, URLs, workspace trust, hooks, MCP startup, or
  organization policy.
- Never test unattended behavior by assuming a TTY prompt will fail safely.
- Model names, effort encoding, flags, and defaults are CLI-specific.
- Vendor docs can lag the installed binary. Preserve the contradiction and test the installed
  version before changing runtime behavior.
