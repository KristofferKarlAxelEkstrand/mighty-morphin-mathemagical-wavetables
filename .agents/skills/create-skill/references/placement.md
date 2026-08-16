# Placement — agent-agnostic skills

## Canonical home

```text
.agents/skills/<skill-name>/SKILL.md
```

Why:

- Open Agent Skills format ([agentskills.io](https://agentskills.io)) is harness-neutral.
- Cursor discovers `.agents/skills/` as a first-class project path (also `~/.agents/skills/`
  globally).
- office-space treats `.agents/skills` as **authored content**; harness trees are adapters.
- One source → many agents (Claude, Cursor, Codex, Devin, …) via symlink/mirror — no N copies to
  edit.

## Do / don't

| Do                                                 | Don't                                                  |
| -------------------------------------------------- | ------------------------------------------------------ |
| Author under `.agents/skills/`                     | Author only under `.claude/skills` or `.cursor/skills` |
| Keep folder name == `name` frontmatter             | Rename folder without updating `name`                  |
| Sync/mirror for harnesses that need a native path  | Hand-edit generated mirrors                            |
| Use `~/.agents/skills/` for personal global skills | Put team skills only in a personal Cursor dir          |

## office-space hosts

Load this section when the repo has `.agents/office-space/` / discovery adapters.

Default skill adapters (symlink or mirror via `office-space sync`):

- `.claude/skills` → `.agents/skills` (required for Claude Code)
- `.devin/skills` → `.agents/skills` (optional; Devin also reads `.agents/` natively)
- tracked (not auto-synced): `.github/skills` → `.agents/skills`

After editing a skill:

```bash
office-space sync --write           # symlink adapters
office-space sync --write --mirror  # portable copies (pass --mirror explicitly on Windows CLI)
office-space sync --check
```

Only `localDiscovery` paths are synced (`.claude/skills`, `.devin/skills` by default). Unix: usually
symlinks. Mirrors include `.office-space-generated`. Do not hand-edit those mirrors. Full bridge
choice → sibling skill `share-skills`.

## Personal vs project

| Scope            | Path                |
| ---------------- | ------------------- |
| Project (shared) | `.agents/skills/`   |
| User (all repos) | `~/.agents/skills/` |

Project overrides user on name collision (typical client rule).

## Nested / monorepo

Optional: `apps/web/.agents/skills/...` for package-scoped skills. Prefer repo-root
`.agents/skills/` unless the skill is useless outside that package.

## Cross-agent discovery

Who reads `.agents/skills/` natively vs who needs a symlink/mirror → activate sibling skill
`share-skills`.
