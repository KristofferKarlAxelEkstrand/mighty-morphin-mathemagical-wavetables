# OpenAI Codex

**Sources:** [Codex skills](https://developers.openai.com/codex/skills), symlink support PRs/issues.

## Discovery paths

| Scope          | Path                                                              |
| -------------- | ----------------------------------------------------------------- |
| Repo           | `.agents/skills` from **cwd upward to repo root** (nested + root) |
| User           | `$HOME/.agents/skills`                                            |
| Admin / system | e.g. `/etc/codex/skills`, bundled system skills                   |

Optional per-skill UI metadata: `agents/openai.yaml` beside `SKILL.md` (Codex-specific; ignore
elsewhere).

## Bridge

**None** when skills live in `.agents/skills/`.

Codex follows symlinks to skill folders (with cycle/depth limits). Keep `.agents/skills` a **real
directory** (canonical), not a symlink to somewhere else, unless the link is valid — broken relative
links cause “no skills.”

## Invoke / verify

- `$skill-name` / skill selector
- Fresh session from repo root should list repo skills
- `allow_implicit_invocation` (default true) for auto use

## Gotchas

- Duplicate `name` across scopes: Codex may show both (no silent merge).
- Live file-watch updates may not follow symlinks; restart CLI after skill edits via links.
- Do not add a redundant `.codex/skills` adapter if `.agents/skills` is already committed.

## office-space

No adapter entry needed.
