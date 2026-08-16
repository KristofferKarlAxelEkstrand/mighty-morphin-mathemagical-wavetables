# Init templates

`office-space init` scaffolds from **`src/templates/`** and role→partial maps in
**`src/init-office-space.js`**. Dogfood may drift ahead; check-ins should close **general** gaps so
new teams inherit what works.

## Map

| Live                         | Init source                                                          |
| ---------------------------- | -------------------------------------------------------------------- |
| `co-workers/_shared/*.md`    | `src/templates/partials/*.md`                                        |
| Mission / WORKFLOW           | `src/templates/mission-doc.md`                                       |
| Seeded host skills           | `src/templates/office-space-*-skill.md`, `model-chooser-skill.md`, … |
| Spec / records / epics stubs | `spec-*.md`, `records-readme.md`, `epics-readme.md`                  |
| Seed tasks                   | `seed-task.md`, `seed-todo.md`                                       |
| AGENTS / CLAUDE              | `agents-md.md`, `claude-shim.md`                                     |

**Role bodies and which partials each role gets** are controlled in `src/init-office-space.js`, not
by partial files alone.

## When to edit templates

Update templates (and init map if needed) only if **all** hold:

1. Lesson is **general** (any team), not dogfood epic trivia
2. Evidence from evaluate or diagnose
3. Small enough to review (one partial or section)

**Promote:** messaging routing, owned_paths discipline, sleep-step oneshot expectations, short-mail
style, lock rules.  
**Keep dogfood-only:** package epic IDs, host model picks, qualify paths.

## Audit (Deep mode)

1. Diff `src/templates/partials/*` vs live `co-workers/_shared/` and protocol skill
2. Diff `mission-doc.md` vs live `WORKFLOW.md` — promote reusable bits only
3. Confirm init role map still assigns messaging / locks / sleep / self-verification / git as
   intended
4. Seeded skill templates should not contradict `.agents/skills/office-space*/SKILL.md`
5. Optional smoke: `init --workflow tmp-…` in a **temp** dir; delete after

## Edit rules

- Update **templates** for defaults **and** live workflow if behavior should change now
- `node src/cli.js sync --write` if host skill bridges need refresh
- No secrets or host-specific paths in templates
- Touching `init-office-space.js` → run init-related unit tests

## Partials that must stay true

| Partial                | Core truth                                 |
| ---------------------- | ------------------------------------------ |
| `messaging.md`         | mail vs slack routing; short messages      |
| `concurrency-locks.md` | owned_paths / claim discipline             |
| `sleep-step.md`        | oneshot wait + re-enter                    |
| `self-verification.md` | cheapest checks before review              |
| `git-commits.md`       | human owns commits unless asked            |
| `mailbox-hygiene.md`   | read/archive; no re-noise                  |
| `memory-discipline.md` | compact logs; durable decisions in records |
| `spec-discipline.md`   | spec before drive-by features              |
| `plan-approval.md`     | when plans need a gate                     |
