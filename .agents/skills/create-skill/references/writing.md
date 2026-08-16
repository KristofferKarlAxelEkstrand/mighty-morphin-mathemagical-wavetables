# Writing — terse, triggerable, useful

## Description (discovery)

Third person. WHAT + WHEN. Concrete trigger words the user might say.

```yaml
# good
description: >-
  Extract text and tables from PDFs; fill forms; merge files. Use when handling PDFs, forms, or
  document extraction.

# bad
description: Helps with PDFs.
```

- Pushy is OK: list adjacent intents even if the user never says the domain word.
- No implementation internals ("uses library X") unless that is the trigger.
- Quote YAML if the value contains `:`.

## Body style

| Prefer                  | Avoid                      |
| ----------------------- | -------------------------- |
| Imperative steps        | Soft essays                |
| Defaults + one escape   | Five equal options         |
| Concrete paths/commands | Vague "consider…"          |
| Gotchas list            | Restating common knowledge |
| Short examples          | Novel-length tutorials     |

Self-test each paragraph: _Would the agent fail without this?_ If no → delete.

## Patterns that pay rent

**Gotchas** — environment facts that defy defaults. Keep in `SKILL.md` (agent may never open a
reference for them).

**Checklist** — multi-step work the agent must not skip.

**Template** — short output shapes inline; longer skeletons in `assets/` and copy/adapt. Prefer
`assets/SKILL.template.md` when authoring new skills with this skill.

**Plan → validate → execute** — destructive/batch work; validate against a source of truth before
mutating.

**Load triggers** — every reference link needs “open when …”, not a bare “see references/”.

## Anti-patterns

- Explaining industry basics the model already knows.
- Windows `\` paths inside skills.
- Time-gated "before Aug 2025 use v1" without a durable current section.
- Mixing synonyms for one thing (`endpoint` / `URL` / `route`).
- Vague names: `helper`, `utils`, `tools`.
- Deep link trees (`SKILL` → A → B → C).
- Duplicating the same skill into every harness folder.

## Extract from reality

Best skills come from a real task + corrections, not from inventing process in a vacuum. After a
miss: add a gotcha or tighten a step; cut unused text.

## Multi-model note

Instructions that only work for the strongest model are too thin for cheaper ones; instructions that
over-explain waste tokens on strong models. Aim for clear procedures + examples; put encyclopedic
detail in `references/`.
