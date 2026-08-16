# Ship checklist — agent-agnostic repo

## Instructions

- [ ] Root `AGENTS.md` exists; README stays human-focused
- [ ] Lean, command-heavy; includes **Security** and/or **Do not**
- [ ] `CLAUDE.md` is `@AGENTS.md` shim (or symlink) — not a second full copy
- [ ] Nested `AGENTS.md` only where packages truly differ
- [ ] No secrets in instruction files
- [ ] Gemini (if used): reads AGENTS.md via settings or thin GEMINI.md — no dual novels
- [ ] Copilot (if used): shared rules in AGENTS.md; `copilot-instructions.md` thin or absent

## Skills & MCP

- [ ] Skills authored under `.agents/skills/` (`create-skill`)
- [ ] Holdout discovery bridged per `share-skills` (esp. Claude)
- [ ] MCP: single canonical source documented; vendor files derived or single-harness only
- [ ] No hand-maintained duplicate skill trees under `.claude/` / `.cursor/` as source of truth
- [ ] Understood: office-space `sync` ≠ MCP generator

## Vendor leftovers

- [ ] Cursor `.mdc` rules left as Cursor-only; shared policy promoted to AGENTS.md
- [ ] Claude settings/hooks not mistaken for portable policy
- [ ] `.gitignore` covers `settings.local.json`, private skills, sync junk

## Prove

- [ ] At least two different harnesses can follow AGENTS.md setup/test commands
- [ ] Claude session loads policy via shim (not empty / not “only AGENTS.md”)
- [ ] Cursor (if used): AGENTS.md actually in always-applied / injected context — verify, don’t
      assume
- [ ] `office-space doctor` / `sync --check` clean when this is an office-space host
- [ ] Skill visible to Claude (bridged) and to a native `.agents/` client (Codex/Copilot/Devin/…)
