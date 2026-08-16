# Cursor

**Sources:** [Cursor skills docs](https://cursor.com/docs/skills),
[help](https://cursor.com/help/customization/skills), forum reports on `.agents/skills` discovery.

## Discovery paths (documented)

| Scope   | Path                                                     |
| ------- | -------------------------------------------------------- |
| Project | `.agents/skills/`, `.cursor/skills/`                     |
| User    | `~/.agents/skills/`, `~/.cursor/skills/`                 |
| Compat  | `.claude/skills/`, `.codex/skills/` (+ user equivalents) |
| Nested  | `apps/web/.agents/skills/` scoped to that tree           |

Built-in `/create-skill` often writes under **`.cursor/skills/`**.

## Reality check

Docs list `.agents/skills/` as first-class. Multiple users (IDE + `agent` CLI, 2026) report:

- Skills under `.agents/skills/` appear under **Rules**, not Skills, or do not show in `/` menu
- Same skill under `.cursor/skills/` works

Treat Cursor as: **prefer verifying on your Cursor version**; if flaky, bridge `.cursor/skills` →
`.agents/skills`.

## Bridge

| Situation                                       | Action                                                                       |
| ----------------------------------------------- | ---------------------------------------------------------------------------- |
| `.agents/skills` shows as Skill + `/name` works | No adapter                                                                   |
| Discovery fails / listed as Rule only           | `ln -sfn ../.agents/skills .cursor/skills` or add to `localDiscovery` + sync |

Do **not** author only in `.cursor/skills/` — keep canonical under `.agents/skills/`.

## Invoke / verify

- `/skill-name` or Customize → Skills
- Confirm entry is under **Skills**, not only Rules
- Optional: `paths` frontmatter (Cursor-specific) for file scoping

## office-space

Not in default `localDiscovery`. Consider adding `.cursor/skills` → `skills` if the team uses Cursor
heavily and hits the discovery bug.
