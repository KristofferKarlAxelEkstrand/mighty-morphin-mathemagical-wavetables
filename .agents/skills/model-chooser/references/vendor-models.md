# Vendor and model-family notes

Last researched: 2026-07-22. These notes normalize families found in the local CLI catalog. Read
`sources.md` before relying on a volatile claim.

## OpenAI

- **GPT-5.6 Sol:** flagship/frontier tier for complex professional work, coding, research, and long
  tool-driven tasks. Official API list price is $5/M input and $30/M output; 1.05M context. Use as a
  quality baseline for leads, difficult DSP, and high-risk review.
- **GPT-5.6 Terra:** balanced intelligence/cost tier at $2.50/M input and $15/M output; same
  published context. Test for bounded implementation, QA triage, and routine review.
- **GPT-5.6 Luna:** fastest, cost-sensitive GPT-5.6 tier at $1/M input and $6/M output; roughly the
  earlier nano tier. Test for monitoring, extraction, and low-risk repetitive work.
- **GPT-5.5, GPT-5.4, GPT-5.4 mini, GPT-5.3 Codex/Spark:** older or specialized catalog options.
  Prefer current official model pages and local evals; do not assume version number alone predicts
  role fit.

Official pricing is an API reference point, not Codex, Cursor, Copilot, or Devin billing.

## Anthropic

- **Claude Fable 5:** Anthropic describes it as its most capable generally available model and best
  for ambitious, long-running asynchronous work. Strong safeguards may route or limit some
  cyber/biology work. Treat it as a frontier candidate for complex leads and independent review.
- **Claude Opus 4.8/4.7/4.6:** high-capability coding and agent tier. Opus 4.8 emphasizes
  long-running tasks, judgment, tool use, and a 1M context window; official price begins at
  $5/M input and $25/M output. Older Opus versions remain candidates only when a CLI lacks newer
  entries or local results favor them.
- **Claude Sonnet 5/4.6/4.5:** balanced agentic coding tier. Anthropic positions Sonnet 5 close to
  Opus 4.8 on some tasks at lower cost and Sonnet 4.6 as a coding, planning, and long-context
  upgrade. Good candidate for developers, fixers, and routine review.
- **Claude Haiku 4.5:** fast tier. Use for extraction and bounded low-risk work after measuring
  false positives and tool reliability.

The local `claude` CLI seed catalog may lag newer full IDs. Validate exact availability.

## Google

- **Gemini 3.1 Pro:** preview advanced-intelligence tier for complex problem solving, agentic work,
  and coding. Preview status increases stability risk.
- **Gemini 3.5 Flash:** Google describes it as a strong sustained agentic and coding model. Consider
  it a balanced/high-throughput candidate, not merely a summarizer.
- **Gemini 3 Flash:** older preview family. Prefer 3.5 where the active CLI exposes it unless local
  evaluation says otherwise.
- **gpt-oss-120b-medium in Antigravity:** an OpenAI open-weight model served through Google's
  harness; vendor, host, and harness differ. Treat its local behavior as unknown until evaluated.

## Cursor

- **Composer 2.5:** Cursor-only, coding-specialized model for hands-on agentic coding, long-running
  tasks, and high-volume work. Cursor reports $0.50/M input and $2.50/M output for standard mode,
  with a higher-priced fast mode. Strong candidate for developers and fixers; vendor benchmarks use
  the Cursor harness and need local confirmation.
- **Auto:** routes based on reliability/demand and may change models. Use for convenience, not
  controlled evaluation or roles requiring stable failure modes.
- Cursor also exposes OpenAI, Anthropic, Gemini, Grok, and GLM families. Their behavior and cost can
  differ from first-party CLIs.

## GitHub Copilot

- **Auto:** GitHub says task optimization considers task complexity, health, and availability. It
  can reduce rate limiting but weakens reproducibility and model-specific accountability.
- **GPT-5.4:** GitHub recommends it for deep reasoning, debugging, multi-step problems, and
  architecture-level code analysis. The local seed catalog exposes only this fixed option and Auto.

## Devin and Cognition models

- **SWE-1.7:** Cognition's Kimi K2.7-based coding-agent model, trained for longer asynchronous tasks
  and self-compaction. Cognition reports 1000 tokens/second in Devin, up to six-hour training
  trajectories, deeper codebase exploration, and stronger edge-case probing. It also discloses a
  tendency toward wider change scope. Vendor evaluations used maximum effort and different native
  harnesses for some competitors, so compare cautiously.
- **SWE-1.7 Max:** present in the live Devin catalog and free for this workspace according to the
  user. The launch post documents SWE-1.7 but does not clearly define the `Max` label, so treat
  Max-specific behavior as a local question.
- **SWE-1.6:** coding-agent model optimized for speed, parallel tool use, shorter trajectories,
  fewer loops, and smoother interaction. Cognition reports benchmark parity with its preview and 200
  tokens/second for the free version. It is present in the live Devin catalog and free for this
  workspace according to the user.
- **SWE-1.7 / Medium / Lightning and SWE-1.6 Fast:** catalog entries with insufficient official
  public model documentation found during this research. Do not infer quality order or entitlement
  coverage beyond confirmed labels.
- **Adaptive:** likely a routing option, but no adequate official description was found. Do not use
  in controlled comparisons.
- **Inkling:** multiple effort variants appear in the Devin catalog without adequate public official
  documentation. Mark unknown.
- Devin exposes many third-party model aliases. Prefer canonical lowercase IDs when available and
  verify what the CLI actually launches.

## DeepSeek

- **DeepSeek V4 Pro:** official flagship V4 tier for reasoning, coding, and agentic work with 1M
  context and thinking/non-thinking modes.
- **DeepSeek V4 Flash:** faster, cheaper tier that DeepSeek says approaches Pro reasoning and
  matches it on simple agent tasks. Consider for bounded coding and high-volume work.
- Vendor benchmark claims are self-reported. Local catalog availability is through Devin, so harness
  behavior is a major variable.

## Z.ai / GLM

- **GLM-5.2:** current catalog family with high/max and 1M variants. Official ZCode material
  describes stable 1M context, flexible effort, coding, and long-horizon tasks. The exact
  `GLM-5.2 High` entry is free for this workspace according to the user, making it a priority
  bake-off candidate.
- **GLM-5:** official foundation model aimed at agentic engineering, backend refactoring, debugging,
  and long tasks.

## Moonshot / Kimi

- **Kimi K2.6:** official general flagship in the researched catalog: multimodal,
  thinking/non-thinking, code, self-correction, and longer software-engineering tasks. Consider for
  coding and agent work after local tests.
- **Kimi K2.7:** appears in the Devin catalog, but adequate official documentation for the exact
  entry was not established in this pass. Keep unknown rather than extrapolating from K2.6.

## SpaceXAI / Grok

- **Grok 4.5:** coding and agentic engineering model with 500K context, reasoning, function calling,
  and published API pricing of $2/M input and $6/M output. Vendor reports fast serving and strong
  engineering benchmarks. Available through Devin/Cursor; test harness-specific behavior.

## NVIDIA

- **Nemotron 3 Ultra:** open 550B-total/55B-active hybrid MoE model for agentic reasoning, coding,
  research, and long-running agents. Appears through Devin. Deployment quality can vary by host and
  quantization, including the separate `nvfp4` catalog entry.

## Models with insufficient evidence

Treat private IDs, `MODEL_PRIVATE_*`, generic aliases such as `claude`, `gpt`, `gemini`, and any
unverified display-label duplicate as unknown. Do not recommend them when an exact documented model
is available.
