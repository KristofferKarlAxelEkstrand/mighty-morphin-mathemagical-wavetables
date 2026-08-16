# POWERRANGERS

This is the mission doc for the `powerrangers` workflow. Package machinery (mail, Slack, tasks,
health, memory, records, CLI) lives in the `office-space` package. This file is the product policy
for this wavetable repo.

## 1. Mission

This team writes and reviews offline mathematical wavetable generators so a second agent can catch
bad phase math, DC offset, and broken periodicity before a formula ships as a WAV.

A single agent would self-approve a waveform that only looks like code. The team exists so
implementation and audio-contract review fail in different ways.

Non-goals:

- Not a real-time audio engine
- Not sampled-audio wavetables
- Not a synthesizer UI, plugin host, or web app
- Not a second task board outside `tasks/`, `mail/`, and `slack/`

## 2. Co-workers

- **Team Lead** (`team-lead`) — Triage `mail/in/`, split epics into tasks with `owned_paths` and a
  `verification_tier`, assign with capability aliases, and unblock. Does not write product code.
- **Implementer** (`dev-1`) — Implements one task at a time: generators, core, tests, and the docs
  that belong to that change. Moves work to review when the handoff evidence exists.
- **Quality** (`quality`) — Independent review of math and code, then QA against the evidence
  ladder. Combined `reviewer` + `qa` is the gate for this small library.

Agent ids are names. Pipeline authority comes from `.prompt.json` flags: exactly one enabled agent
has `lead: true`. Inspect live assignment with `office-space team roles powerrangers`.

Do not add a second implementer, scout, or writer until `tasks/todo/` stays piled while `dev-1` is
busy.

## 3. Claiming and locks

- Active tasks declare `owned_paths`. Overlaps fail closed. Every implementer follows
  `co-workers/_shared/concurrency-locks.md`.
- One active implementation task per implementer.
- Path families the lead uses when splitting work:
  - `maths/<name>.py` plus matching tests — one generator at a time
  - `generator/wavetable_synthesis/core/` vs `cli/` vs `export/` — do not overlap
  - `generator/wavetable_tests/` — only one implementer
  - `.agents/skills/wavetable-generator/` — its own task

There is no scout. Do not invent hunt cards. Absorb near-duplicates into the open parent task.

## 4. The pipeline

Stages (`space.json` → `tasks.stages`): queued → implementing → review → qa → human → blocked →
done.

Use `--assignee auto-implementer` at `implementing`, `--assignee auto-reviewer` at `review`, and
`--assignee auto-qa` at `qa`.

## 5. Human gate protocol

A human is required only for:

- Changing the public `generate(theta, u)` / `BaseGenerator` / `ProcessingConfig` contract
- Adding a runtime Python or npm dependency
- Publishing to PyPI, or shipping a public WAV collection

New generators, tests, docs, and core bugfixes proceed once review and QA pass. Do not park routine
waveform work on `human`.

## 6. Quality bars

`verification_tier` is required on every task. Implementers never rewrite a tier downward.

Allowed `verification_tier` values: `focused`, `package`, `integration`, `release`.

| Tier | When | Evidence |
| --- | --- | --- |
| `focused` | While editing | `python -m ruff check <touched-paths>` and the narrowest `pytest --no-cov` path that exercises the change |
| `package` | Default before review | `python -m ruff check generator/ maths/` plus `python -m ruff format --check` on those trees plus `pytest --no-cov generator/wavetable_tests` |
| `integration` | Core pipeline, registry, CLI, export, or processing | `package` plus `python -m mypy --strict generator/wavetable_synthesis/` plus `python -m wavetable_synthesis --list` plus generate one named generator |
| `release` | Public contract, new runtime dep, publish | named ACK in `mail/out/` (this is the human gate) |

Coverage target is 90% on `wavetable_synthesis`. Default pytest in `pyproject.toml` enables
`--cov`. Use `--no-cov` for `focused` and `package`. Run coverage on `integration`, or when the
task touches core.

Review (`quality` as reviewer) rejects when any of these fail. The contract is spec `S001`. Load
skill `wavetable-generator` for the procedure.

- `theta` is one cycle in radians (`0` to `2π`). `u` is in `[0, 1]`. Generators call `_validate_u`.
- Raw `generate()` returns `float64`, same length as `theta`, all finite, not all zeros.
- After the processing pipeline: peak in `±1`, DC near 0. Loop wrap matches the formula (sine stays
  continuous; a saw may jump once).
- Math only. No sampled audio as the waveform source.
- Code stays readable. This repo teaches. Clever NumPy golf is a reject.
- Tests must cover **all** registered generators, not only the first registry entry.

QA (`quality` as qa) re-runs the task's named tier and confirms the reported commands exist and
cover the submitted paths. Empty LGTM is a reject.

Machine review (`space.json` `review.machineChecks`) runs workflow integrity, ruff, and
`pytest --no-cov generator/wavetable_tests` before a human or Quality spends a turn. `mypy --strict` is not a
machine-review check.

## 7. Project-health cadence

No resident runners. Do not add a runner until the test garden stalls the gate.

If a periodic job is added later, put it in `runners/` with `runner: true` and
`start_mode: "one-shot"`, document the clock here, and let the controller dispatch it. The lead
does not run jobs inline.

Until then, Quality owns flaky-test notes in `records/` when a gate fails twice on the same
fingerprint.

## 8. Communication and kanban

See skill `office-space-protocol` for mail, Slack, tasks, and memory. Workflow extras:

- Lead owns `mail/in/`. Implementers do not triage it.
- Handoffs name the task file, the diff or paths, the exact commands run, and the next stage.
- Review rejects are a numbered fix list. Implementers fix only that list.
- Human questions go to `mail/out/` with a bare `Answer:` line.

## 9. Bootstrapping

1. Ensure root `AGENTS.md` and `CLAUDE.md` exist (`CLAUDE.md` starts with `@AGENTS.md`).
2. Create and activate a venv on this Linux host: `python -m venv .venv` then
   `source .venv/bin/activate`.
3. Install: `pip install -e ".[dev]"` and `npm install`.
4. Discover skills: `office-space sync --write`.
5. Prove: `office-space check-system`, `office-space doctor`, `office-space check --tier fast`.
6. Start: `office-space team start powerrangers`.

After an office-space package bump: `office-space whats-new` →
`office-space skills refresh --check|--write` →
`office-space partials refresh --check|--write --workflow powerrangers` →
`office-space sync --write` → `office-space doctor`.

All three co-workers use the `grok` CLI. Devin is not installed here. Claude is installed but not
logged in. Revisit mixed-family review (Grok implements, Claude reviews) after `claude /login`.

## 10. Changelog

- 2026-08-15 — Rewrote mission, quality bars, human gates, and Grok CLI assignment for this
  wavetable repo. Replaced seed T001 with E001.
- 2026-08-15 — Workflow scaffolded by `office-space init`.
