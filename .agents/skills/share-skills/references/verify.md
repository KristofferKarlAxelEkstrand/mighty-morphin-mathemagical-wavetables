# Verify — prove agents can see the skill

## Repo health (office-space)

```bash
office-space sync --check
office-space doctor
```

**Doctor/`sync --check` treat `missing` as OK.** That means a clone with no `.claude/skills` adapter
can still be “green” while Claude sees nothing.

| Status                                          | Doctor / sync --check | Holdout discovery (Claude/Devin)          |
| ----------------------------------------------- | --------------------- | ----------------------------------------- |
| `symlink` / `generated-mirror`                  | OK                    | Ready                                     |
| `missing`                                       | OK (not an error)     | **Not ready** — run sync for that harness |
| `broken-symlink` / `stale-mirror` / `unmanaged` | Fail                  | Not ready — repair                        |

For every holdout you care about, require a healthy adapter — do not stop at a green doctor.

## Filesystem

```bash
test -f .agents/skills/<name>/SKILL.md && echo canonical_ok
# for each adapter you care about:
test -f .claude/skills/<name>/SKILL.md && echo claude_ok
test -f .devin/skills/<name>/SKILL.md && echo devin_ok
```

Frontmatter `name:` must equal the folder name.

## Per client smoke

| Client            | Check                                                                                        |
| ----------------- | -------------------------------------------------------------------------------------------- |
| Claude Code       | Invoke `/name`; filesystem under `.claude/skills` (symlink UI list may lie)                  |
| Cursor            | Customize → **Skills** (not only Rules); `/name` works from `.agents/` or bridged `.cursor/` |
| Codex             | `$name` / selector from repo `.agents/skills`                                                |
| Copilot / VS Code | `/` skills list; coding agent loads on description                                           |
| Devin             | `@skills:name` or auto; confirm indexed/cloned repo has `.agents/skills`                     |
| Antigravity       | `/skills` (CLI) from project with `.agents/skills`                                           |

## Description trigger test

Ask each agent a prompt that matches the skill `description` **without** naming the skill. It should
load or offer the skill. If only explicit `/name` works, tighten WHAT+WHEN trigger terms (see
`create-skill` → writing).

## Clone / CI traps

- Fresh Windows clone: adapters missing or broken → `sync --write --mirror`.
- CI without symlinks: prefer mirrors or generate adapters in setup.
- `core.symlinks=false` on Windows Git → treat as mirror workflow.

## Failure playbook

1. Canonical file missing → author under `.agents/skills/`.
2. Holdout adapter `missing` (even if doctor is green) → `sync --write` or `sync --write --mirror`.
3. Adapter broken/stale → `sync --write` (+ `--mirror` if needed).
4. `unmanaged` → relocate content to canonical, delete unmanaged, sync.
5. Client still blind → confirm that client’s documented paths; add adapter only if native
   `.agents/` unsupported.
6. Stale behavior after edit → mirror out of date; re-sync; restart agent session.
7. Works in WSL but not Windows Git → stubs; switch that checkout to mirror workflow.
