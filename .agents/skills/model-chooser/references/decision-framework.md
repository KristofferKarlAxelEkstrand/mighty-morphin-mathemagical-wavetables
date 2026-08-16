# Decision framework

## Score the work

Score each factor from 0 (irrelevant) to 3 (critical):

| Factor        | Meaning                                                     |
| ------------- | ----------------------------------------------------------- |
| Correctness   | Cost of a subtle wrong result.                              |
| Long horizon  | Need to preserve goals across many tool calls.              |
| Code depth    | Architecture, debugging, C++, DSP, or repository reasoning. |
| Judgment      | Ambiguity, taste, prioritization, or trade-offs.            |
| Throughput    | Frequency and volume of repeated tasks.                     |
| Latency       | Benefit of quick turns and short feedback loops.            |
| Context       | Amount of code, logs, or history needed at once.            |
| Independence  | Value of a different model family's failure modes.          |
| Cost pressure | Need to minimize marginal spend or quota.                   |

Use frontier/high-effort models when correctness, long horizon, code depth, or judgment dominates.
Use balanced models for bounded implementation and verification. Use fast/cheap models for
deterministic monitoring, extraction, formatting, or initial triage. Never use a cheap model for a
high-risk role merely because it is free.

## Separate model from harness

Record these independently:

- base model family and version;
- reasoning/effort level;
- CLI harness and tool set;
- context and compaction behavior;
- subscription quota or marginal cost;
- latency and reliability in this workspace.

Changing more than one dimension makes a comparison harder to interpret.

## Repository bake-off

Use three to five completed historical tasks whose expected outcome is known:

1. a bounded implementation in the repository's primary language;
2. a defect review containing seeded or previously fixed issues;
3. a build/test failure diagnosis;
4. a workflow or documentation consistency task;
5. a long-horizon coordination task when evaluating leads.

Run each candidate at least three times when cost permits. Keep prompt, starting commit,
permissions, and available tools fixed. Use a fresh worktree or restore an identical snapshot
between runs.

Score:

| Metric                                      | Weight |
| ------------------------------------------- | -----: |
| Correct final behavior and verdict          |     30 |
| Material defects found or avoided           |     20 |
| Verification quality                        |     15 |
| Scope discipline and unnecessary changes    |     10 |
| Instruction and real-time-safety compliance |     10 |
| Completion rate without human rescue        |      5 |
| Wall time                                   |      5 |
| Marginal cost or quota use                  |      5 |

Apply hard failures before totals: fabricated verification, unsafe audio-thread code, destructive
out-of-scope changes, or a false approval of a known critical defect disqualifies the run.

## Recommendation confidence

- `high`: at least three relevant local runs with consistent results and known cost.
- `medium`: relevant official evidence plus one or two local runs.
- `low`: vendor claims, cross-harness benchmarks, undocumented models, or unknown local cost.

Keep a stable baseline. Change one or two roles at a time, observe for a full task cycle, and retain
a fallback. Re-evaluate after catalog changes or repeated role-specific failures.

## External benchmark use

Use external benchmarks to form candidates, not to make the final assignment:

- Prefer Terminal-Bench for terminal operation and tool coordination.
- Prefer SWE-bench variants for repository issue resolution.
- Prefer long-task evaluations such as METR's time horizon for autonomous roles.
- Record the model, reasoning effort, agent harness, task subset, repeats, timeout, and evaluation
  date.
- Do not compare scores across different harnesses as if they isolate model capability.
- Discount self-reported launch scores and saturated or contaminated benchmarks.

The local bake-off remains decisive because these coworkers use repository-specific prompts, locks,
MCP tools, and handoff rules that public benchmarks do not measure.
