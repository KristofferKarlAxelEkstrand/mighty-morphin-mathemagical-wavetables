# Improve this skill

After a **check-in** or **deep** pass: would the _next_ agent do better if this skill already
contained what we just learned? If yes, edit **this** skill in the same session.

## Triggers

Edit when any:

1. Mis-classification or missed collaboration issue the skill should have caught
2. New repeatable check/command not already in a sibling skill
3. Gotcha that burned real time
4. Scorecard missing a dimension that mattered
5. Script wrong or incomplete
6. User asked for a new watch/eval dimension

Skip when the lesson is pure package code with no operator procedure.

## Where

| Change                         | File                       |
| ------------------------------ | -------------------------- |
| Steps, modes, handoff, gotchas | `SKILL.md` (keep lean)     |
| Downtime patterns              | `diagnose-downtime.md`     |
| Scorecard rows                 | `evaluate-team.md`         |
| Fix priorities                 | `improvement-playbook.md`  |
| Init promotion                 | `init-templates.md`        |
| Self-edit rules                | this file                  |
| Signals                        | `scripts/team-snapshot.sh` |
| Discovery text                 | YAML `description`         |

Prefer append a row/bullet over rewriting a section.

## Quality bar

1. Evidence one-liner (what happened)
2. Actionable without this chat
3. Link siblings; do not paste protocol/tmux/model-chooser
4. `npm run validate:skills`
5. List paths under handoff **Changes**

## Anti-patterns

- SKILL.md essay growth
- Logging ticks into the skill
- Unverified theories as gotchas
- Editing `.claude/skills` mirrors — only `.agents/skills/`
- More than one self-improve pass per check-in unless user asks

## End-of-check-in

```text
Skill self-review:
- Struggle without guidance? → add
- Guidance wasted time? → fix/delete
- Snapshot miss? → extend script
- Description match how users ask? → update frontmatter
```

## Changelog (trim to ~15 lines)

- 2026-07-29: Deep qa pile — concurrent full gardens thrash; prefer one garden + Tests own-prior
  full-unit reuse; archive non-primary `[TASK]` wakes (dogfood §6.4 / package-test-gates 8/10).
- 2026-07-28: Scorecard **D9** post-epic idle — empty board + idle implementers OK when scout
  woke/hunting; silent scout >~1h is the fail (check-in after E006–E008 close).
- 2026-07-28: `await=never` + timeout pane post-respawn = false dead (class C); capture-pane before
  restart.
- 2026-07-28: When tests stall the team, rework garden (fast/integration split) is first-class;
  scorecard D5 suite cost.
- 2026-07-28: Throughput×quality — one gate task/turn; lead clears stale blocked_by; flow scorecard;
  package-test-gates.
- 2026-07-28: Self-improve track; stop_team name collision; list-panes scope; oneshot false-dead;
  qualify-* noise; FORCE_COLOR/jq flake; dual-claim; stop audit; mode-based SKILL refactor.
