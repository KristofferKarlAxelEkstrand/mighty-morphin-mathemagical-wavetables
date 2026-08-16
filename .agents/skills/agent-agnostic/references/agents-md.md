# Writing AGENTS.md

Standard: [agents.md](https://agents.md) (Agentic AI Foundation / Linux Foundation stewardship).
Plain Markdown — **no required schema**.

## Purpose

README for **agents**: build/test commands, conventions, and boundaries they cannot infer from the
code. Keep human onboarding in `README.md`.

## Recommended sections

Popular choices from the standard + what works in practice:

1. **Project** — one screen of what/why + stack versions that matter.
2. **Setup / build / test** — exact shell commands (incl. single-test). Agents run what you list.
3. **Conventions** — only deltas from language defaults; non-obvious architecture.
4. **Security** — secrets, PII, forbidden network/data paths.
5. **Do not** — hard negatives (generated paths, forbidden refactors, “never commit X”).
6. **Git / PR** — if agents commit or open PRs.
7. **Pointers** — skills path, key docs — not pasted manuals.

## Writing rules

- Imperative, copy-pasteable commands > prose.
- Self-test: _Would the agent fail without this line?_ If no → cut.
- Prefer ~**150–200 lines** at root; push depth to docs or skills.
- Update in the same PR as the behavior change (living doc).
- Nested files: put package-local AGENTS.md where agents edit; **closest wins**; user chat overrides
  all.
- Always-on file: every line costs context on every turn for agents that inject it. Prefer skills
  for long procedures.

## What not to put here

- Long API references → `references/` in a skill or docs/.
- Secrets, tokens, private URLs.
- Vendor-only UI toggles → vendor config files.
- Duplicate README marketing copy.
- Full copies of skill workflows (link the skill name/path instead).

## Migration

| Have today                                  | Do                                                                                                       |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Only `CLAUDE.md`                            | Move body → `AGENTS.md`; leave `CLAUDE.md` as `@AGENTS.md` + Claude-only notes                           |
| Only `.cursorrules` / Copilot instructions  | Extract shared policy → `AGENTS.md`; keep thin vendor adapters if needed                                 |
| Both full `AGENTS.md` + full `CLAUDE.md`    | Merge into AGENTS.md; shrink Claude to shim + overrides                                                  |
| Symlink `CLAUDE.md` → `AGENTS.md`           | Fine on symlink-safe Unix teams with **no** Claude-only notes; prefer `@AGENTS.md` on Windows / mixed OS |
| Reverse symlink (`AGENTS.md` → `CLAUDE.md`) | Avoid for multi-agent repos — makes Claude the canonical owner                                           |

### Claude import (official)

From [Claude Code memory docs](https://code.claude.com/docs/en/memory#agents-md): Claude reads
`CLAUDE.md`, not `AGENTS.md`. Put `@AGENTS.md` in `CLAUDE.md` (or `./.claude/CLAUDE.md`); Claude
loads the import at session start, then **appends** anything below it. Put Claude-only notes after
the import. HTML comments in CLAUDE.md are stripped from context (safe for maintainer notes). Prefer
`@AGENTS.md` on Windows (symlink needs Admin/Developer Mode).

Personal gitignored extras: `CLAUDE.local.md` (loads alongside; worktree-local unless you import
from home).

### Myth to ignore

“Claude reads AGENTS.md as a fallback when CLAUDE.md is missing” — **false** per official docs. A
repo with only `AGENTS.md` gives Claude Code zero project instructions (silent).

## Prove the file

- List a real test command; run it once yourself.
- Ask two harnesses the same “how do I run tests?” question after loading the repo.
- Confirm Claude session shows policy via shim (not empty).
