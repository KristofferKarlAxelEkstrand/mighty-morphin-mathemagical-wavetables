---
name: share-skills
description: >-
  Make skills under .agents/skills discoverable to Claude, Cursor, Codex, Copilot, Devin,
  Antigravity, and other agents via native paths, symlinks, or mirrors. Use when wiring skill
  discovery per harness, choosing symlink vs copy, fixing an agent that cannot see a skill, or
  running office-space sync.
---

# Share Skills

Canonical source: **`.agents/skills/<name>/`**. Prefer **no bridge**. Bridge only proven holdouts.

## Do this

1. Confirm the skill lives under `.agents/skills/<name>/SKILL.md`.
2. List target harnesses → [references/harness-matrix.md](references/harness-matrix.md); open each
   `harness-*.md` you care about.
3. Native-in-practice (Codex, Copilot, Devin, Antigravity; Cursor if verified): **stop**. Commit
   canonical only.
4. Holdouts: **Claude** (required `.claude/skills`); **Cursor** if `.agents/` discovery is flaky
   (`.cursor/skills`). Choose bridge → [references/bridge-choice.md](references/bridge-choice.md).
5. office-space: `sync --write` or `sync --write --mirror` (**`--mirror` explicit on Windows CLI**).
   → [references/adapters.md](references/adapters.md).
6. Prove → [references/verify.md](references/verify.md). Ship →
   [references/checklist.md](references/checklist.md).

## Load when

| File                                                                   | Open when                             |
| ---------------------------------------------------------------------- | ------------------------------------- |
| [references/harness-matrix.md](references/harness-matrix.md)           | Which harnesses need a bridge         |
| [references/harness-claude.md](references/harness-claude.md)           | Claude Code paths / bridge            |
| [references/harness-cursor.md](references/harness-cursor.md)           | Cursor paths / `.agents` flake        |
| [references/harness-codex.md](references/harness-codex.md)             | Codex paths                           |
| [references/harness-copilot.md](references/harness-copilot.md)         | Copilot / VS Code paths               |
| [references/harness-devin.md](references/harness-devin.md)             | Devin product + CLI paths             |
| [references/harness-antigravity.md](references/harness-antigravity.md) | Antigravity / Gemini paths            |
| [references/bridge-choice.md](references/bridge-choice.md)             | Symlink vs mirror vs nothing          |
| [references/adapters.md](references/adapters.md)                       | Running sync / repairing adapters     |
| [references/verify.md](references/verify.md)                           | Agent blind to a skill / doctor fails |
| [references/checklist.md](references/checklist.md)                     | Final pass                            |

Authoring → sibling `create-skill`. Repo-wide AGENTS.md / `.agents/` layout → sibling
`agent-agnostic`.

## Gotchas

- **Symlinks are not universally best** — see bridge-choice (Windows git stubs, WSL vs Windows
  checkout).
- **Best bridge is often none** — Codex / Copilot / Devin / Antigravity read `.agents/skills/`
  natively.
- **Claude is the hard holdout** — keep `.claude/skills` adapter.
- **Cursor: trust but verify** — docs say `.agents/skills`; users still hit discovery bugs →
  optional `.cursor/skills` bridge.
- **Devin `.devin/skills` sync is optional** — product recommends `.agents/skills` and scans eight
  trees including it.
- **`doctor` green ≠ Claude ready** — `missing` adapters are allowed; holdouts need a real bridge.
- Never author in adapter trees; never hand-edit `.office-space-generated` mirrors.
- `.github/skills` is **not** created by `office-space sync`.
