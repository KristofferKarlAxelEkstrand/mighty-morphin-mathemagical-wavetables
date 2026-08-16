# Source ledger

Last researched: 2026-07-22. Prefer these primary sources. Re-open them when making current
recommendations; prices, availability, and model status are volatile.

## OpenAI

- [Model selection](https://developers.openai.com/api/docs/models) — official family positioning.
- [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol) — context, tools,
  reasoning, and price.
- [GPT-5.6 Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra) — context, tools,
  reasoning, and price.
- [GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna) — context, tools,
  reasoning, and price.
- [GPT-5.6 launch](https://openai.com/index/previewing-gpt-5-6-sol/) — capability and tier claims.

## Anthropic

- [Claude Fable 5](https://www.anthropic.com/claude/fable) — intended use and safeguard caveats.
- [Claude Opus 4.8](https://www.anthropic.com/news/claude-opus-4-8) — agentic/coding guidance,
  effort, and vendor evaluations.
- [Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5) — balanced agentic tier, price,
  and limitations.
- [Claude Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6) — older balanced tier and 1M
  context.
- [System cards](https://www.anthropic.com/system-cards) — evaluation details and model chronology.

## Google

- [Gemini model list](https://ai.google.dev/gemini-api/docs/models) — current positioning and
  lifecycle.
- [Latest Gemini models](https://ai.google.dev/gemini-api/docs/latest-model) — migration, price,
  context, and agent guidance.

## Cursor

- [Composer 2.5](https://cursor.com/composer) — intended use, price, training base, and vendor
  benchmarks.
- [Composer 2 technical report](https://cursor.com/blog/composer-2-technical-report) — training and
  evaluation method.
- [Cursor model selection](https://docs.cursor.com/guides/selecting-models) — harness-level
  selection guidance.
- [Cursor models and Auto](https://docs.cursor.com/models/) — routing and context behavior.

## GitHub Copilot

- [Auto model selection](https://docs.github.com/en/copilot/concepts/models/auto-model-selection) —
  routing behavior and limitations.
- [Model comparison](https://docs.github.com/en/copilot/reference/ai-models/model-comparison) — task
  guidance.
- [Supported models](https://docs.github.com/en/copilot/reference/ai-models/supported-models) —
  current availability.

## DeepSeek

- [DeepSeek API models](https://api-docs.deepseek.com/) — current IDs and deprecations.
- [DeepSeek V4](https://api-docs.deepseek.com/news/news260424/) — family positioning, context, and
  self-reported evaluations.
- [Thinking mode](https://api-docs.deepseek.com/guides/thinking_mode/) — effort mapping.

## Kimi

- [Kimi models](https://platform.kimi.ai/docs/models) — current official catalog.
- [Kimi K2.6](https://platform.kimi.ai/docs/guide/kimi-k2-6-quickstart) — capabilities and tool
  caveats.

## Z.ai

- [GLM-5](https://docs.z.ai/guides/llm/glm-5) — agentic-engineering positioning and evaluations.
- [ZCode and GLM-5.2](https://zcode.z.ai/en/docs/welcome) — current 5.2 context and long-horizon
  claims.
- [GLM-5.2 model card](https://huggingface.co/zai-org/GLM-5.2) — official open-model materials.

## SpaceXAI

- [Grok 4.5 model](https://docs.x.ai/developers/models/grok-4.5) — specifications and pricing.
- [Grok 4.5 launch](https://x.ai/news/grok-4-5) — intended use and vendor benchmarks.

## NVIDIA

- [Nemotron 3 Ultra](https://research.nvidia.com/labs/nemotron/Nemotron-3-Ultra/) — model overview.
- [Technical report](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Ultra-Technical-Report.pdf)
  — architecture and evaluations.

## Devin

- [SWE-1.7](https://cognition.com/blog/swe-1-7) — training, long-horizon behavior, benchmarks,
  methodology, and scope caveat.
- [SWE-1.6](https://cognition.com/blog/swe-1-6) — tool behavior, speed, model UX, and temporary
  public free tier.
- [Billing](https://docs.devin.ai/admin/billing) and
  [self-serve plans](https://docs.devin.ai/admin/billing/self-serve) — public quota and credit
  model.
- No adequate official public page for the exact `SWE-1.7 Max` label, `Adaptive`, or `Inkling` was
  found on 2026-07-22. Use local evaluations and preserve this uncertainty.
- [There's An AI For That: SWE-1.6](https://theresanaiforthat.com/model/swe-1-6/) — user-supplied
  secondary lead. The page was inaccessible and not indexed during this pass; do not rely on
  unverified claims from it.

## Independent and aggregate evaluations

- [Terminal-Bench repository](https://github.com/harbor-framework/terminal-bench) — tasks, execution
  harness, and verification design.
- [Terminal-Bench 2.1 methodology and results](https://artificialanalysis.ai/evaluations/terminalbench-v2-1)
  — fixed Terminus 2 harness and three repeats per task.
- [SWE-bench leaderboards](https://www.swebench.com/) — repository issue-resolution results with
  agent filtering.
- [Artificial Analysis coding-agent methodology](https://artificialanalysis.ai/methodology/coding-agents-benchmarking)
  — composite construction and limitations.
- [METR long-task study](https://arxiv.org/abs/2503.14499) — 50% task-completion time-horizon
  method.
- [RankedAGI models](https://rankedagi.com/models) and [methodology](https://rankedagi.com/engine) —
  useful discovery index, but 81% of model/benchmark pairs were simulated when checked. It is a
  solo-maintained beta and lacks per-score provenance. Use its actual linked benchmark sources, not
  composite ranks, for decisions.

## Local primary sources

- Package `cli-models.json` (via `office-space models audit`) — accepted local strings and catalog
  provenance.
- `.agents/office-space/<workflow>/co-workers/*.prompt.json` — current CLI/model assignments.
- `.agents/skills/model-chooser/references/role-requirements.json` — curated role candidate lists
  when present.
- User report, 2026-07-22 — Devin `SWE-1.7 Max` has zero marginal cost for this workspace.
- User report, 2026-07-22 — Devin `SWE-1.6` has zero marginal cost for this workspace.
- User report, 2026-07-22 — Devin `GLM-5.2 High` has zero marginal cost for this workspace.
