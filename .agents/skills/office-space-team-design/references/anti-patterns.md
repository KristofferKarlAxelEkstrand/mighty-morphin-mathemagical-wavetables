# Team-design anti-patterns

Hard “don’ts” when designing or redesigning a host team. If a draft setup matches one of these, fix
it before `team start`.

## God-agent

One co-worker with lead + implementer + reviewer + qa (or “does everything” prose).

**Why it fails:** No independent review, path locks are theater, context bloat, single point of
failure.

**Fix:** Split capabilities. Minimum viable: separate lead from implementer; at least one other
agent holds `reviewer` and/or `qa` (combined is OK on tiny teams).

## Protocol paste

Copying full mail/slack/task protocol into every `.prompt.md` or into `WORKFLOW.md` § Communication.

**Why it fails:** Token tax on every turn; protocol updates never reach prompts; agents disagree
with the skill.

**Fix:** One line pointer to skill `office-space-protocol`. Role prompts keep Own / Never /
Incomplete Exit only. Workflow-specific extras stay short in WORKFLOW.

## Vendor trees as source of truth

Authoring or editing skills under `.claude/skills`, `.cursor/skills`, `.devin/skills`, etc., as if
those were canonical.

**Why it fails:** `sync` and other harnesses diverge; package refresh cannot find the real skill;
doctor may look fine while Claude sees stale copies.

**Fix:** Canonical = `.agents/skills/<name>/` only. Adapters are bridges (`share-skills` /
`office-space sync`).

## Skip Quality to go faster

Pipeline that jumps `implementing` → `done`, or one agent self-approves review.

**Why it fails:** Spec drift and silent regressions; thrash costs more than the gate.

**Fix:** Keep a `review` stage with a `reviewer: true` agent (machine checks optional pre-filter).
Mid-reject stays focused — speed the **checks**, not the absence of review.

## Copy dogfood WORKFLOW verbatim

Pasting this package’s `developer-team` mission, epic ids, or product-test folklore into a host
repo.

**Why it fails:** Wrong product policy; agents optimize for office-space internals instead of the
host app; eternal confusion about “default” roles.

**Fix:** Keep the **section structure** from the mission template. Write a host mission, host
quality bars, host backlog. Dogfood is an example, not a template body.

## Fork package `_shared` without a refresh plan

Editing `co-workers/_shared/*.md` shipped by init (concurrency, messaging, …) in place as the only
customization path.

**Why it fails:** Later `init --force` can overwrite package partials (with warn); hosts lose edits
or diverge silently from package doctrine.

**Fix:** Prefer role-prompt overlays and host-only partial filenames. If you must fork a package
partial, document it in WORKFLOW changelog and expect `init --force` / future partial-refresh to
clobber — treat git as backup.

## Eternal seed backlog

Leaving welcome `T001` / explore-only tasks as the board forever.

**Why it fails:** No `owned_paths` discipline, no real acceptance, team looks “busy” while
delivering nothing.

**Fix:** Replace with a real epic and tasks that have acceptance criteria, paths, and a verification
expectation.

## Second board / second protocol

Inventing parallel task folders, chat conventions, or status files beside `tasks/`, `mail/`,
`slack/`.

**Why it fails:** Pollers and `task-transition.js` ignore them; dual claims and lost wakes.

**Fix:** Extend `space.json` stages/types if needed; stay on the file protocol the package
implements.

## Model/CLI change without audit

Swapping harness or model strings by hand and assuming entitlements and probes still work.

**Fix:** `office-space models audit` (+ propose/apply when used); re-smoke launch.

## Init --force as “upgrade skills”

Using force re-scaffold to pick up package skill fixes.

**Why it fails:** Clobbers workflow prompts/mission; wrong tool for skill updates.

**Fix:** Package skill updates go through the documented **skills refresh** path (when available) +
`sync --write` + `doctor`. See `office-space-onboard` keep path — not this skill’s greenfield steps.
