---
name: create-skill
description: >-
  Author portable, token-efficient Agent Skills (SKILL.md + references/scripts). Use when creating,
  rewriting, reviewing, or relocating a skill; when the user mentions SKILL.md, progressive
  disclosure, .agents/skills, or agent-agnostic skills.
---

# Create Skill

Write once under `.agents/skills/`. Keep `SKILL.md` short; load detail only when needed.

## Gather (before writing)

1. Purpose: one coherent job.
2. Triggers: phrases that should activate the skill (WHAT + WHEN).
3. Source: prefer a real task + corrections over inventing process.
4. Scope: project (`.agents/skills/`) vs user (`~/.agents/skills/`).
5. Verbatim: if the user gave exact wording, use it unchanged.

Ask only for gaps. Infer from the conversation when enough is already known.

## Do this

1. Place at `.agents/skills/<name>/SKILL.md` (folder name == `name`).
2. Frontmatter: `name` + `description` (WHAT + WHEN + trigger words).
3. Body: only what the model would get wrong without you. Imperative. Short.
4. Copy skeleton from `assets/SKILL.template.md`; adapt — do not invent layout from scratch.
5. Split: `references/` for deep docs, `scripts/` for repeatable logic, `assets/` for templates.
6. Link references one level deep. Use the load triggers below.
7. Validate with [references/checklist.md](references/checklist.md) before shipping.
8. If holdouts need adapters: follow sibling `share-skills` (symlink vs `--mirror`; don’t assume
   `sync --write` alone).

## Load when

| File                                               | Open when                                                           |
| -------------------------------------------------- | ------------------------------------------------------------------- |
| [references/placement.md](references/placement.md) | Choosing path, personal vs project, harness mirrors, or sync        |
| [references/structure.md](references/structure.md) | Splitting files, frontmatter fields, progressive-disclosure budgets |
| [references/writing.md](references/writing.md)     | Drafting description/prose, templates, anti-patterns                |
| [references/checklist.md](references/checklist.md) | Final ship gate                                                     |
| `assets/SKILL.template.md`                         | Starting a new skill file                                           |

Making every agent **discover** the skill → sibling `share-skills`. Whole-repo portable setup
(AGENTS.md, `.agents/`, shims) → sibling `agent-agnostic`.

## Token rules (activation budget)

- Catalog (`name` + `description`): always ~50–100 tokens/skill.
- `SKILL.md` body: keep lean (well under ~5k tokens).
- `references/` / `scripts/` / `assets/`: free until read or run.
- Default + one escape hatch > option menus. Scripts > pasting long code into markdown.

## Gotchas

- Cursor’s built-in `/create-skill` steers to `.cursor/skills/` — **override**: author under
  `.agents/skills/`.
- This skill’s name matches that built-in on purpose; project `.agents/skills/create-skill` should
  win over the Cursor-default path advice.
- Never author in harness mirrors (`.claude/skills`, `.devin/skills`, generated copies). Edit
  `.agents/skills/` only.
- Gotchas belong in `SKILL.md`, not a reference — the agent often will not know to open a file for a
  non-obvious trap.
- Put `office-space sync` details in placement.md; the one-liner in Do this is enough unless
  adapters are involved.
