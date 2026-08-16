# Redesign playbooks

Use when the host already has a workflow and the org, harness, or load changed. Prefer surgical
edits over re-init. After any playbook: `office-space team roles <workflow>`, then `sync --write` /
`doctor` if skills or adapters moved.

Paths are under `.agents/office-space/<workflow>/` unless noted.

---

## Add an agent

1. Decide the **capability gap** (second implementer, dedicated reviewer, scout, researcher, etc.) —
   not a vanity id.
2. Prefer `office-space init` agent flags only for **new** workflows. On an existing workflow, add:
   - `co-workers/<id>.prompt.json` — capabilities, cli, model, enabled
   - `co-workers/<id>.prompt.md` — Own / Never / Incomplete Exit; link protocol, do not paste it
3. **Optional specialty templates:** start from package `templates/co-worker-roles/` (`architect`,
   `researcher`, `product`, `tech-writer`, `security`, `release`) when the gap matches. Most use
   `=none` (no pipeline flags); `tech-writer` is `implementer` for docs-only work. Do not invent a
   fifth capability flag for research/security.
4. Update `WORKFLOW.md` § Co-workers (mission description of who does what).
5. Choose cli/model with `model-chooser` if non-default.
6. `team stop` / `team start` (or host equivalent) so the new pane exists. Confirm `team roles`.

## Remove an agent

1. Drain work: no `working-on` tasks assigned to that id; reassign or finish first.
2. Set `enabled: false` **or** delete the co-worker pair **after** updating any hard-coded assignee
   strings in prompts/partials (prefer capability auto-assignees).
3. Ensure remaining agents still cover `lead`, and whatever pipeline stages you keep (`implementer`,
   `reviewer`, `qa`).
4. Update `WORKFLOW.md`. Restart team; confirm `team roles` shows one lead and required gates.

## Change default harness / CLI

1. Edit each affected `.prompt.json` `cli` (and model flags as needed).
2. Run **`office-space models audit`** (then propose/apply when changing CLIs or models) so
   assignments stay entitled and coherent.
3. Re-check harness launch, activity probes, and permissions (doctor, CLI help, vendor docs) if
   agents fail to start or stagnant-restart misbehaves.
4. `sync --write` if skill bridges must match the new harness. Smoke: one agent wake + `doctor`.

## Split lead vs implementer

**Symptom:** Lead implements, triage starves, or one “tech lead” god-agent holds all paths.

1. Ensure exactly one `lead: true` with **no** `implementer: true` (or document a rare dual-hat
   exception in WORKFLOW — default is split).
2. Move implementation Own/Never bullets to implementer prompt(s); lead keeps triage, spawn,
   npm-request, unblock only.
3. Re-queue any lead-held implementation tasks to an implementer with fresh `owned_paths`.
4. Update human expectations in WORKFLOW (lead does not merge product diffs).

## Introduce runners

**When:** Periodic, bounded jobs (format sweep, dependency audit, flaky triage) — not a second
resident implementer.

1. Add `runners/<id>.prompt.json` with `runner: true` and `start_mode: "one-shot"`, plus
   `.prompt.md`.
2. Document cadence in `WORKFLOW.md` § Project-health (or equivalent).
3. Dispatch: `office-space run <id>` / `type: run-request` mail — while the team is up, the
   **controller** owns schedule (do not assume the lead runs jobs inline).
4. Runners still use `owned_paths` and the normal pipeline unless the host documents a narrow
   formatter fast-path.

## Narrow or widen human gates

1. List stages that **must** wait on a human (release, security, irreversible migrate). Everything
   else stays autonomous after machine + Quality/QA gates.
2. Edit `WORKFLOW.md` § Human gate protocol only — avoid sprinkling “ask human” into every prompt.
3. **Widen** only with a named risk (compliance, prod data). **Narrow** when humans rubber-stamp
   every task and become the bottleneck.
4. If you add a `human` stage transition, ensure `space.json` `tasks.transitions` allow return paths
   (`human` → `implementing` / `done` / `blocked` as appropriate).

## After harness or model shifts — models audit

Any change to default CLI, model id, or reasoning tier:

```bash
office-space models audit
# then propose / apply per CLI help when the host uses those subcommands
```

Re-open `model-chooser` for role fit. Confirm agents still launch under `team start`.

## Fix drift that needs redesign

If onboard’s drift checklist flags placeholder mission, eternal `T001`, protocol pasted into
prompts, or vendor skill trees as SoT:

| Smell                                   | Fix (this skill)                                                   |
| --------------------------------------- | ------------------------------------------------------------------ |
| Placeholder WORKFLOW / template markers | Rewrite mission + quality bars (§ greenfield 1, 4, 6)              |
| Only seed task left                     | Author real epic + tasks (§ 7)                                     |
| Protocol pasted into every prompt       | Strip to Own/Never; link `office-space-protocol`                   |
| Skills only under `.claude/skills`      | Restore `.agents/skills/` SoT; bridges via `share-skills` / `sync` |
| Wrong lineup for load                   | Add/remove agent playbooks above                                   |

Onboard diagnoses “is the host set up?”; **you** own the shape fix. Do not duplicate onboard’s
install/refresh sequence here.
