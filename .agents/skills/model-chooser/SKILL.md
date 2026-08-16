---
name: model-chooser
description:
  Choose and compare CLI/model assignments for co-workers using the live local catalog, workspace
  entitlements, role requirements, current vendor documentation, and repository-specific
  evaluations. Use when selecting, changing, reviewing, benchmarking, or explaining a co-worker's
  cli, model, reasoning tier, cost tier, or a mixed-model set of co-workers.
---

# Model Chooser

Choose a model for a job, not a winner in the abstract.

## Required workflow

1. Read any local notes under `references/` (workspace entitlements, constraints) when present.
2. Inspect the package catalog via `office-space models audit` (or the shipped `cli-models.json`).
   Treat it as the authority for strings accepted by each CLI, not as evidence of capability or
   price.
3. Read the target co-worker's `.prompt.md` and `.prompt.json`. Check its live capability assignment
   with `office-space team roles <workflow>`; agent ids are not evidence of role. Reduce the prompt
   and enabled `lead`, `implementer`, `reviewer`, and `qa` capabilities to the factors in
   `references/decision-framework.md`.
4. Read only the relevant model-family sections in `references/vendor-models.md` and the matching
   source entries in `references/sources.md`.
5. Run `npx @kristoffer-karl-axel-ekstrand/office-space models audit` (or
   `office-space models audit`). Add `--live` to query installed CLIs for current availability and
   account-scoped cost; `--live` includes the per-row live data in the report. Resolve or clearly
   report catalog and research gaps; never hide `unknown`, `private`, or router entries.
6. Produce a shortlist of two or three valid CLI/model pairs. State evidence quality, expected
   strengths, risks, cost status, and what remains unknown.
7. Prefer local evaluation results over vendor claims. If no relevant local result exists, recommend
   a bounded bake-off from `references/decision-framework.md`.
8. Before changing a config, validate the exact model string, effort, and CLI-specific permission
   mode against the catalog and the agent's `.prompt.json`. Change `cli`, `model`,
   `reasoning_effort`, and `permission_mode` together.

## Live audit output

When `models audit --live` runs, each row includes a `live` object with:

- `available`: `available`, `unavailable`, `unknown`, or `error`
- `scope`: `account`, `workspace`, `public`, or `unknown`
- `observed_at`: ISO timestamp of the live probe
- `provenance`: the command or note that produced the data
- `cost`: separate `public`, `workspace`, `quota`, `multiplier`, `tier`, and `summary` fields
- `error`: `null` or a short failure reason

Devin output is parsed from the nested `families[].variants[]` object returned by
`devin models list --format json`; each variant's `model_uid` becomes the row `model`, and
`cost_tier` and `cost_summary` are preserved. Cursor and Grok report availability from
`cursor-agent models` and `grok models` text output; cost is `unknown` when those CLIs do not expose
account pricing. Models discovered live but absent from the static catalog are appended as
`catalog_source: "live"` rows with `evidence: "unknown"` and the same `live` block; validate them
before use. Never treat `tier` or `summary` as a per-token price and never infer zero marginal cost
from subscription inclusion.

## Full-team workflow

Generate a non-mutating proposal:

```bash
npx @kristoffer-karl-axel-ekstrand/office-space models propose --output .tmp/model-coworkers.json
```

(or `office-space models propose --output .tmp/model-coworkers.json` if installed locally.)

Review the exact diff and the `locally_validated` flags. Validate without writing by omitting
`--confirm`:

```bash
npx @kristoffer-karl-axel-ekstrand/office-space models apply .tmp/model-coworkers.json
```

(or `office-space models apply .tmp/model-coworkers.json` if installed locally.)

Only after explicit approval, repeat with `--confirm`. Applying configs does not restart running
co-workers.

## Evidence rules

- Rank evidence: repository task evaluation > observed workspace behavior and entitlement >
  reproducible third-party evaluation > vendor technical report/system card > vendor product page >
  anecdote.
- Keep model capability, harness quality, reasoning effort, latency, quota, and price separate. A
  model result from one harness does not transfer cleanly to another CLI.
- Treat vendor benchmark comparisons as directional. Record the harness, effort, date, and whether
  the vendor evaluated itself.
- Do not infer that aliases, display labels, fast modes, priority modes, context variants, or
  reasoning levels are distinct base models.
- Mark undocumented catalog entries `unknown`; never invent specifications.
- Date all volatile facts. Refresh web research when a source or catalog is older than 30 days, a
  model is preview/evaluation-only, or the user asks for current advice.
- Treat user-reported workspace pricing as authoritative for that workspace while labeling it
  `local entitlement`, not public pricing.

## Decision output

Return:

1. recommended CLI/model and exact accepted catalog string;
2. reason tied to the role's work;
3. cost and availability status for this workspace;
4. confidence (`high`, `medium`, or `low`) and evidence basis;
5. fallback model;
6. evaluation needed before permanently changing this co-worker's model.

For the full set of co-workers, include correlated-failure risk. Assign independent reviewers or
parallel implementers to different model families when the expected quality benefit exceeds CLI and
prompt-behavior variance.
