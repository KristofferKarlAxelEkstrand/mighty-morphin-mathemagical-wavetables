# Research method

Use this order for every harness change.

## Evidence

1. **Repository behavior:** inspect `src/lib/cli-tools.sh`, `src/run-team`, prompt generation,
   activity adapters, tests, and the target co-worker config.
2. **Installed interface:** record resolved binary, version, top-level help, relevant subcommand
   help, authentication status, and model-list behavior.
3. **Official primary sources:** CLI reference, configuration and permission docs, release
   notes/changelog, official source repository or README when published.
4. **Controlled experiment:** use a disposable repository and the least privilege needed. Record
   command, version, TTY/non-TTY state, exit code, stdout/stderr shape, files changed, and session
   artifacts.
5. **Secondary evidence:** use issues and community reports only to discover failure modes to
   reproduce.

Prefer observed repository tests over vendor marketing. A successful run on one version, OS,
account, model, or permission policy is not a universal guarantee.

## Required integration questions

For each CLI answer:

- What binary and versions are supported? How is authentication checked?
- Does cwd define the workspace? Are extra roots explicit?
- How is a prompt supplied without shell/TTY ambiguity?
- Does the process exit after one task or retain an interactive session?
- Can a session be named, identified, resumed, or continued deterministically?
- Which permissions cover tools, files, shell, network/URLs, MCP, hooks, and trust? Can managed
  policy override them?
- Which model and effort forms are accepted by this installed version?
- Is output text, JSON, JSONL, or a TUI? What identifies completion and failure?
- What are timeout, cancellation, signal, retry, and rate-limit behaviors?
- Can office-space inspect live activity without confusing another checkout or session?
- Which instruction, skill, plugin, MCP, hook, and config layers load?

## Refresh and decisions

- Date every volatile source. Re-open facts older than 30 days, preview/beta behavior, and anything
  contradicted by installed help.
- Label each conclusion `documented`, `observed`, `inferred`, or `unknown`.
- Record the exact version for observed behavior.
- Change lifecycle or permission defaults only after an authenticated smoke test and a focused
  regression test.
- When onboarding another CLI, first add it to the research set. Do not add it to
  `CLI_TOOLS_SUPPORTED` until launch, permissions, waiting, and failure behavior are all defined.
