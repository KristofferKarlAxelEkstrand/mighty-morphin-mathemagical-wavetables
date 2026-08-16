---
name: agent-agnostic
description: >-
  Set up a portable, multi-agent repository: AGENTS.md, CLAUDE.md shim, .agents/ layout, skills,
  MCP, and vendor adapters. Use when making a repo agent-agnostic, adding AGENTS.md, migrating
  CLAUDE.md/.cursorrules, structuring .agents/, or avoiding vendor lock-in across Claude, Cursor,
  Codex, Copilot, Devin, Antigravity.
---

# Agent-Agnostic Setup

One canonical tree. Vendor dirs are adapters — not second sources of truth.

## Classify every artifact

| Kind                    | Strategy                                                                                          | Examples                                              |
| ----------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Portable**            | Store once; agents read natively or via thin shim                                                 | `AGENTS.md`, `.agents/skills/**`                      |
| **Generated / derived** | Canonical in `.agents/`; render thin vendor files (do **not** assume office-space sync does this) | MCP → `.mcp.json` / `.cursor/mcp.json`                |
| **Agent-specific**      | Leave in vendor dir; never invent a fake portable twin                                            | `.cursor/rules/*.mdc`, `.claude/settings.json`, hooks |

## Gather (before changing files)

1. Which harnesses must work? (Claude needs a shim; Gemini may need `context.fileName`.)
2. What already exists? (`CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`,
   `.agents/`.)
3. Office-space host? → doctor expects `.agents/skills` + `.agents/mcp/servers.json`; sync bridges
   **skills**, not MCP.
4. Shared policy vs Cursor-only globs vs Claude-only hooks — classify before moving.

Ask only for gaps. Infer from the tree when enough is known.

## Do this

1. Write root [AGENTS.md](https://agents.md) — agent README (commands, boundaries, security).
   Template → `assets/AGENTS.template.md`.
2. Add Claude shim `CLAUDE.md` with `@AGENTS.md` first; Claude-only overrides **below**. →
   `assets/CLAUDE.shim.template.md`.
3. Ensure `.agents/skills/` and (if used) `.agents/mcp/`. Layout →
   [references/layout.md](references/layout.md).
4. Put reusable workflows in skills (`create-skill`); discovery bridges → `share-skills`. Keep
   AGENTS.md always-on and lean.
5. Keep vendor-only config where it belongs. Adapters →
   [references/adapters.md](references/adapters.md).
6. Nest `AGENTS.md` in packages when monorepo needs differ (**closest wins**; chat overrides all).
7. Ship gate → [references/checklist.md](references/checklist.md).

## Load when

| File                                               | Open when                                     |
| -------------------------------------------------- | --------------------------------------------- |
| [references/layout.md](references/layout.md)       | Designing `.agents/` tree / office-space host |
| [references/agents-md.md](references/agents-md.md) | Writing, trimming, or migrating AGENTS.md     |
| [references/adapters.md](references/adapters.md)   | Per-harness instruction files, MCP, shims     |
| [references/checklist.md](references/checklist.md) | Final pass / migration audit                  |
| [references/sources.md](references/sources.md)     | Verifying claims against upstream docs        |
| `assets/AGENTS.template.md`                        | Scaffolding AGENTS.md                         |
| `assets/CLAUDE.shim.template.md`                   | Scaffolding Claude pointer                    |

Sibling skills: `create-skill` (author SKILL.md), `share-skills` (harness discovery bridges).

## Gotchas

- **AGENTS.md ≠ README** — humans keep README; agents get operational commands and hard boundaries.
- **Claude Code does not read AGENTS.md alone** — no silent fallback. Without `CLAUDE.md`, Claude
  gets **zero** project instructions. Use `@AGENTS.md` (or symlink). Claude-only notes go **below**
  the import (appended after load).
- **Do not port Cursor `.mdc` into a fake shared format** — shared policy → AGENTS.md; MDC stays for
  glob / `alwaysApply` only.
- Keep AGENTS.md lean (aim ≪ 200 lines). Long workflows → skills (progressive disclosure), not more
  AGENTS.md.
- Cursor: docs say native `AGENTS.md`; treat as **trust but verify** (version / worktree regressions
  have happened).
- office-space `sync` syncs **skill** adapters only — it does **not** generate `.mcp.json` from
  `.agents/mcp/servers.json`.
- Skills live under `.agents/skills/`, not only under `.claude/skills/` — see `share-skills`.
