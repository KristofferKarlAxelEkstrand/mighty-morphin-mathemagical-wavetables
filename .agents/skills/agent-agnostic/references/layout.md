# Layout — agent-agnostic repo

## Target shape

```text
repo/
  AGENTS.md                 # portable instructions (agents.md / AAIF)
  CLAUDE.md                 # @AGENTS.md shim (+ Claude-only overrides)
  README.md                 # humans

  .agents/
    skills/<name>/SKILL.md  # portable skills (agentskills.io)
    mcp/servers.json        # canonical MCP defs (if used)
    office-space/           # office-space workflows (this ecosystem)
    # optional: scripts/ for link/sync helpers; skills-local/ gitignored

  .claude/                  # Claude adapters + Claude-only
    skills/                 # bridge → .agents/skills (symlink or mirror)
    settings.json           # hooks etc. — agent-specific
  .cursor/                  # Cursor-only rules; optional skills bridge
  .devin/                   # optional skills bridge
  .github/                  # CI; optional copilot-instructions.md (Copilot-only)
  .gemini/                  # optional settings.json for context.fileName
```

## What belongs where

| Asset                      | Home                                                                      |
| -------------------------- | ------------------------------------------------------------------------- |
| Shared agent policy        | Root `AGENTS.md`                                                          |
| Package-specific policy    | Nested `AGENTS.md` (closest wins)                                         |
| Reusable workflows         | `.agents/skills/<name>/`                                                  |
| MCP server defs            | `.agents/mcp/servers.json` → **derive** vendor files (see adapters)       |
| office-space teams         | `.agents/office-space/<workflow>/`                                        |
| Cursor glob rules          | `.cursor/rules/*.mdc` (stay)                                              |
| Claude hooks / local perms | `.claude/settings.json` / `.claude/settings.local.json` (gitignore local) |
| Claude personal notes      | `CLAUDE.local.md` (gitignore; worktree-local)                             |
| Copilot-only extras        | `.github/copilot-instructions.md` (thin; shared rules stay in AGENTS.md)  |

## Ownership split (context budget)

| Layer                | When loaded                                                  | Put here                                 |
| -------------------- | ------------------------------------------------------------ | ---------------------------------------- |
| `AGENTS.md`          | Always-on / ambient for supporting agents                    | Commands, boundaries, security, pointers |
| Skills               | Progressive disclosure (description always; body on trigger) | Multi-step workflows                     |
| Vendor rules / hooks | Harness-specific                                             | Globs, permissions, UI toggles           |

Do not paste skill-length procedures into AGENTS.md.

## office-space host

This package expects `.agents/office-space/` for workflows and `.agents/skills/` as authored skills.
Doctor requires `.agents/skills` and canonical MCP path (default `mcp/servers.json`).
**`office-space sync` bridges skill discovery dirs only** — it does not render MCP vendor files.
Skills bridges → sibling `share-skills`.

## Anti-patterns

- Full instruction text duplicated in `AGENTS.md` + `CLAUDE.md` + `.cursorrules` +
  `copilot-instructions.md`.
- Authoring skills only under `.claude/skills/` or `.cursor/skills/`.
- Hand-editing generated MCP adapter files while also editing canonical (pick one source of truth).
- Stuffing monorepo-wide novels into one root AGENTS.md instead of nesting.
- Assuming `doctor` green means Claude sees skills or MCP adapters exist.
