# Structure — progressive disclosure

## Layout

```text
.agents/skills/<name>/
├── SKILL.md           # required — metadata + short procedure
├── references/        # optional — read when SKILL.md says so
├── scripts/           # optional — run; code stays out of context
└── assets/            # optional — templates, schemas, samples
```

Spec: [agentskills.io/specification](https://agentskills.io/specification).

## Frontmatter (required)

```yaml
---
name: skill-name # ≤64 chars; a-z 0-9 hyphens; = folder name
description: >- # ≤1024 chars; WHAT + WHEN + triggers
  Does X. Use when Y or Z.
---
```

Optional (spec): `license`, `compatibility`, `metadata`, `allowed-tools`.

Client extras (e.g. Cursor `paths`, `disable-model-invocation`) are fine in project skills when
needed — keep core portable; document client-only keys in `compatibility` or a short note.

## Three tiers

1. **Catalog** — clients load only `name` + `description` for every skill (~50–100 tokens each).
2. **Activation** — full `SKILL.md` body when the task matches (keep lean; ≪ 5k tokens / ≤ ~500
   lines guidance).
3. **Execution** — open `references/*` or run `scripts/*` only when instructions point there.

An agent with 20 skills should not pay for 20 full bodies up front.

## Reference discipline

- Paths relative to the skill root.
- **One level deep** from `SKILL.md` → `references/foo.md`. No reference chains.
- Each reference file = one concern (small files = less context when loaded).
- In `SKILL.md`, name the file and the trigger: "Load `references/api.md` when calling the HTTP
  API."

## Scripts vs prose

| Prefer script when     | Prefer prose when     |
| ---------------------- | --------------------- |
| Same logic every run   | Judgment / style      |
| Fragile exact sequence | Many valid approaches |
| Validation / parsing   | Teaching a pattern    |

Script code does not enter context; **output** does. Keep scripts non-interactive, clear exit codes,
useful stderr.

## Degrees of freedom

- **High** — heuristics, review, design.
- **Medium** — template + allowed variation.
- **Low** — exact command / "do not add flags".

Calibrate per step, not per whole skill.
