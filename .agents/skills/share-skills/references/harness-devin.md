# Devin (Cognition)

**Sources:** [Devin product skills](https://docs.devin.ai/product-guides/skills),
[Devin CLI skills overview](https://docs.devin.ai/cli/extensibility/skills/overview).

## Discovery paths

### Product (cloud / indexed + cloned repos)

**Recommended:** `.agents/skills/<name>/SKILL.md`

Also scanned in every repo:

- `.devin/skills/`
- `.github/skills/`
- `.claude/skills/`
- `.cursor/skills/`
- `.codex/skills/`
- `.cognition/skills/`
- `.windsurf/skills/`

Indexed org repos + on-disk scan after clone; re-scan when clone finishes mid-session.

### Devin CLI

| Scope   | Path                                                                                |
| ------- | ----------------------------------------------------------------------------------- |
| Project | `.agents/skills/`, `.devin/skills/`, `.windsurf/skills/`                            |
| Global  | `~/.agents/skills/`, `~/.config/devin/skills/` (Windows: `%APPDATA%\devin\skills\`) |

## Bridge

**Not required** for discovery if skills are under `.agents/skills/`.

`.devin/skills` remains a supported alternate (and what older office-space sync maps). Keeping a
symlink there is redundant but harmless; editing only `.devin/skills` without `.agents/` hurts other
agents.

## Invoke / verify

- Auto from `description` (unless `triggers: ["user"]`)
- `@skills:name` / `@skills:name args` in prompts
- CLI: `/skill-name`
- One active skill at a time (product limitation)

## Extra frontmatter (Devin)

Beyond agentskills core: `argument-hint`, `triggers`, dynamic `` !`cmd` `` blocks, `$ARGUMENTS` /
`$0` substitution. Other harnesses ignore unknown keys.

## Gotchas

- Skills ≠ Playbooks (playbooks are org UI templates; skills are repo files).
- Only one skill active at a time in product Devin.
- office-space still syncs `.devin/skills` — treat as optional compatibility, not proof that Devin
  cannot read `.agents/`.

## office-space

`.devin/skills` in `localDiscovery` is **optional** for Devin visibility. Safe to keep for teams
that also open `.devin/` trees; not the discovery bottleneck Claude is.
