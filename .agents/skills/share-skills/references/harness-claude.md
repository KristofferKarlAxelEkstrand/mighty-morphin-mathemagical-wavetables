# Claude Code

**Sources:** [Claude Code skills docs](https://code.claude.com/docs/en/skills),
[platform overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview),
open issues requesting `.agents/skills` scan.

## Discovery paths

| Scope             | Path                                                          |
| ----------------- | ------------------------------------------------------------- |
| Project           | `.claude/skills/<name>/SKILL.md`                              |
| Personal          | `~/.claude/skills/<name>/SKILL.md`                            |
| Nested / monorepo | `.claude/skills/` under packages when those files are in play |
| Plugins           | Plugin-bundled skills                                         |
| Legacy            | `.claude/commands/*.md` (commands, not full skills)           |

**Does not** reliably scan `.agents/skills/` as of current docs. Configurable `skillsPaths` has been
requested repeatedly; treat as unavailable unless your installed version documents it.

## Bridge

**Required** for a single canonical tree under `.agents/skills/`:

```bash
# via office-space (preferred in this repo)
office-space sync --write            # or --write --mirror on Windows CLI
# manual
ln -sfn ../.agents/skills .claude/skills
```

## Invoke / verify

- Slash: `/<skill-name>`
- `/skills` list — may glitch on **symlinked** dirs; still try invocation
- Auto-invocation from `description`

## Gotchas

- Symlink UI list bugs ≠ missing skill — verify filesystem + invoke.
- `--add-dir` / extra dirs are session/CLI workarounds, not a team-wide substitute for
  `.claude/skills`.
- Nested package skills use path-qualified names when colliding.

## office-space

Keep `.claude/skills` in `localDiscovery`. Highest-priority adapter.
