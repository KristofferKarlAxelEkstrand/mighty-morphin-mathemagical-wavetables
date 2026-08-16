# Sources — agent-agnostic research notes

Dated claims for this skill. Re-check before contradicting upstream.

| Topic                                                           | Source                                                                      | Note                                                                                     |
| --------------------------------------------------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| AGENTS.md purpose, nesting, FAQ (Aider/Gemini config)           | https://agents.md (fetched 2026-07-25)                                      | No required schema; closest nested wins; chat overrides                                  |
| Claude reads CLAUDE.md not AGENTS.md; `@AGENTS.md` import       | https://code.claude.com/docs/en/memory#agents-md (fetched 2026-07-25)       | No silent AGENTS.md fallback; append notes below import; Windows prefer `@` over symlink |
| Claude HTML comments stripped; CLAUDE.local.md; `.claude/rules` | Same memory docs                                                            | Safe maintainer comments; personal local file; path-scoped rules stay Claude-only        |
| Cursor AGENTS.md native + injection bugs                        | Cursor forum threads 2026 (alwaysApply / worktrees)                         | Trust but verify                                                                         |
| Gemini `GEMINI.md` + `context.fileName`                         | https://geminicli.com/docs/cli/gemini-md/                                   | Prefer configure AGENTS.md over dual full files                                          |
| Copilot AGENTS.md + `.github/copilot-instructions.md`           | agents.md “supported agents”; harness matrices 2026                         | Keep Copilot file thin                                                                   |
| office-space sync scope                                         | office-space package: skill discovery adapters only; doctor checks MCP path | Do not claim sync generates `.mcp.json`                                                  |
| Skills progressive disclosure                                   | agentskills.io + sibling `create-skill`                                     | AGENTS.md always-on vs skills on demand                                                  |

Sibling research: `share-skills/references/harness-*.md` for skill discovery per harness.
