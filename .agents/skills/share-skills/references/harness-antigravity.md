# Antigravity

**Sources:** Antigravity / Gemini ecosystem installers
([antigravity-awesome-skills](https://www.npmjs.com/package/antigravity-awesome-skills)), Google
Cloud + Antigravity skill tutorials, community skill vaults. Confirm against your installed
Antigravity / `agy` CLI version.

## Discovery paths

| Scope                                   | Typical path                                                                                                             |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Project (preferred)                     | `.agents/skills/<name>/SKILL.md`                                                                                         |
| User / global                           | `~/.agents/skills/`                                                                                                      |
| Antigravity / Gemini globals (variants) | `~/.gemini/antigravity/skills/`, `~/.gemini/config/skills/`, `~/.gemini/antigravity-cli/skills/` (CLI channel-dependent) |
| Legacy community                        | `.agent/skills/` (singular) in some older guides — prefer **`.agents/`**                                                 |

Installer tools often treat Antigravity as a **universal `.agents/skills` client** alongside Codex,
Cursor, Copilot, Gemini CLI.

## Bridge

**None** for project skills authored under `.agents/skills/`.

Do not invent `.antigravity/skills` in office-space unless a specific Antigravity release documents
that path as the _only_ scanner and omits `.agents/`.

## Invoke / verify

- Antigravity CLI (`agy`): `/skills` list in the workspace that contains `.agents/skills`
- IDE agent: skill should appear when cwd is the project root
- After install via `npx antigravity-awesome-skills`, confirm files landed under `.agents/skills`
  (project) or `~/.agents/skills` (global)

## Gotchas

- Path sprawl: global Gemini/Antigravity directories differ by channel — for **repo** sharing, stick
  to `.agents/skills/`.
- Singular `.agent/skills` vs `.agents/skills` — if a skill “vanishes,” check both; migrate to
  `.agents/`.
- office-space lists `antigravity` as a known CLI/`--harness` value; that does **not** currently
  imply a skills adapter entry.

## office-space

No skills adapter needed. Ensure `doctor` sees `.agents/skills` authored content; Antigravity reads
that tree directly.
