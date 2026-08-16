# Harness matrix — common agent CLIs

Canonical authoring: **`.agents/skills/<name>/SKILL.md`**.

| Harness               | Native `.agents/skills`?         | Also scans                                                                                 | Bridge needed?                                   | Detail                                           |
| --------------------- | -------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ |
| **Claude Code**       | No (project = `.claude/skills/`) | `~/.claude/skills/`, plugins, nested `.claude/skills`                                      | **Yes** → `.claude/skills`                       | [harness-claude.md](harness-claude.md)           |
| **Cursor**            | **Docs: yes** / **field: flaky** | `.cursor/skills/`, compat `.claude/`, `.codex/`                                            | **Often yes for reliability** → `.cursor/skills` | [harness-cursor.md](harness-cursor.md)           |
| **Codex**             | **Yes** (walks cwd → repo root)  | `~/.agents/skills/`, admin/system roots                                                    | **No**                                           | [harness-codex.md](harness-codex.md)             |
| **Copilot / VS Code** | **Yes**                          | `.github/skills/`, `.claude/skills/`; `~/.copilot/skills`, `~/.agents/skills`              | **No** (optional `.github/skills`)               | [harness-copilot.md](harness-copilot.md)         |
| **Devin**             | **Yes (recommended)**            | Also `.devin/`, `.github/`, `.claude/`, `.cursor/`, `.codex/`, `.cognition/`, `.windsurf/` | **No** for discovery                             | [harness-devin.md](harness-devin.md)             |
| **Antigravity**       | **Yes** (ecosystem default)      | Global `~/.agents/skills/`, Gemini/Antigravity global variants                             | **No**                                           | [harness-antigravity.md](harness-antigravity.md) |

## office-space sync today

`localDiscovery` (actually synced): `.claude/skills`, `.devin/skills`.

| Path                                  | Why it exists                          | Still needed?                                                            |
| ------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------ |
| `.claude/skills`                      | Claude cannot rely on `.agents/` alone | **Yes — keep**                                                           |
| `.devin/skills`                       | Historical / CLI alternate path        | **Optional** — Devin product docs recommend `.agents/skills` and scan it |
| `.github/skills` (`trackedDiscovery`) | Copilot-centric repos                  | **Not synced** by `office-space sync`; Copilot already reads `.agents/`  |
| `.cursor/skills`                      | Not in defaults                        | **Consider adding** if team hits Cursor `.agents/` discovery bugs        |

## Decision rule

```text
for each target harness:
  open harness-*.md
  if native .agents works in practice → no adapter
  else → bridge via bridge-choice.md (symlink vs mirror)
```

Do not add adapters “for completeness” for Codex/Copilot/Antigravity/Devin when `.agents/skills/` is
already committed.
