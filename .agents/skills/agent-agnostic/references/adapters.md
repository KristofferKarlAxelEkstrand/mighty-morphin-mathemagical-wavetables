# Adapters — vendor files without drift

## Instructions (how each agent gets policy)

| Agent                             | Portable path                      | Adapter / notes                                                                                                                                                                                                                          |
| --------------------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Codex                             | Root `AGENTS.md` native            | Nested AGENTS.md supported                                                                                                                                                                                                               |
| Cursor                            | Root `AGENTS.md` (intended native) | Also `.cursor/rules/*.mdc`. **Verify** injection on your version; worktree / alwaysApply bugs have existed. `@AGENTS.md` in chat forces load.                                                                                            |
| Copilot coding agent              | Root `AGENTS.md`                   | Optional thin `.github/copilot-instructions.md` for Copilot-only extras — do not duplicate AGENTS.md                                                                                                                                     |
| Devin / Antigravity / many others | Root `AGENTS.md`                   | Prefer canonical; avoid second novels                                                                                                                                                                                                    |
| Claude Code                       | **Does not** read AGENTS.md alone  | `./CLAUDE.md` or `./.claude/CLAUDE.md` with `@AGENTS.md` (or symlink). Optional `CLAUDE.local.md`. Path rules: `.claude/rules/`. [Docs](https://code.claude.com/docs/en/memory#agents-md).                                               |
| Aider                             | Configure                          | `.aider.conf.yml` → `read: AGENTS.md`                                                                                                                                                                                                    |
| Gemini CLI                        | Default historically `GEMINI.md`   | Prefer `.gemini/settings.json` → `context.fileName` includes `AGENTS.md`, **or** thin `GEMINI.md` that stays Claude-shim-thin. Do not maintain two full policy files. Newer Gemini builds may list AGENTS.md in defaults — still verify. |

Never maintain a second **full** policy file for Claude / Cursor / Copilot / Gemini.

## Skills

Canonical: `.agents/skills/`. Bridges for holdouts → sibling **`share-skills`** (Claude
`.claude/skills` required; Cursor optional; symlink vs mirror).

In office-space repos: `office-space sync --write` / `--mirror` (**`--mirror` must be explicit on
Windows CLI**).

## MCP (derived — not office-space sync)

Canonical in this ecosystem: `.agents/mcp/servers.json` (doctor checks it exists).

| Consumer | Typical vendor file                                            |
| -------- | -------------------------------------------------------------- |
| Claude   | `.mcp.json`                                                    |
| Cursor   | `.cursor/mcp.json`                                             |
| Codex    | often user/`repo` config TOML merge — check current Codex docs |

**Important:** `office-space sync` does **not** generate these from `servers.json`. Treat MCP as:

1. Edit canonical JSON only, then
2. Render or maintain thin vendor files with a script/tooling you own, **or**
3. Document the single file your team actually loads if you are single-harness for MCP.

Formats differ (JSON vs TOML, `type` fields) — **do not symlink** MCP configs across agents.

## Agent-specific (leave alone)

- `.cursor/rules/*.mdc` — glob / `alwaysApply` have no portable twin; put _shared_ rules in
  AGENTS.md instead of translating MDC.
- `.claude/settings.json` / hooks / `settings.local.json` (gitignore local).
- `.claude/rules/*.md` — Claude path-scoped rules (like Cursor MDC); not a portable twin of
  AGENTS.md.
- Claude subagent / persona files under `.claude/agents` if used — not the same as skills.
- Copilot path-specific instruction files under `.github/` beyond the thin root adapter.

## Decision tree

```text
Same bytes work for every agent?
  → portable (AGENTS.md / .agents/skills)

Same data, different file shape?
  → derived from .agents/ (script or manual render — not assumed sync)

Unique harness feature?
  → agent-specific dir; mention existence in AGENTS.md Pointers
```
