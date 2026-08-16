# Bridge choice — symlink vs mirror vs nothing

## Ranked options

| Rank   | Approach                                              | When it wins                                                                 | When it loses                                                                       |
| ------ | ----------------------------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **1**  | **Nothing** — client reads `.agents/skills/`          | Codex, Copilot, Devin, Antigravity; Cursor when verified                     | Claude Code; Cursor when `.agents/` discovery fails                                 |
| **2**  | **Client config** (`skillsPaths` / vendor equivalent) | Client supports extra skill roots                                            | Claude: requested, not a reliable default yet                                       |
| **3a** | **Directory symlink** (Unix)                          | Local dev, macOS/Linux, WSL with working symlinks; live single source        | Committed into git for mixed Windows teams without `core.symlinks` + Developer Mode |
| **3b** | **Generated real copies (mirror)**                    | Cross-OS git; CI; Windows without symlink privilege; office-space `--mirror` | Must re-sync after every skill edit or copies go stale                              |
| **4**  | **Hand-maintained duplicates**                        | Never                                                                        | Drift is guaranteed                                                                 |

Spec direction
([agentskills.io client guide](https://agentskills.io/client-implementation/adding-skills-support)):
clients should scan **both** `.<vendor>/skills/` **and** `.agents/skills/`. As that spreads, bridges
shrink.

## Symlink — honest assessment

**Pros (why Vercel Skills CLI defaults to symlink):**

- One canonical tree; edits propagate instantly.
- Disk-cheap; `update` once.
- Fine polyfill when Claude only looks at `.claude/skills/`.

**Cons (why teams drop them):**

- Git on Windows often materializes symlinks as **plain text files** (~path stub) unless
  `core.symlinks=true` **and** OS symlink rights (Developer Mode/admin). Skills then silently
  disappear.
- CI / restricted FS may not create symlinks.
- Some UIs (Claude `/skills` list) glitch on symlinked dirs even when load still works.
- Claude’s own feature requests call symlinks a **poor** long-term workaround vs `skillsPaths`.

**Production lesson:** [Nethermind](https://github.com/NethermindEth/nethermind/pull/11842) replaced
committed git symlinks with **real file copies + sync scripts + CI `--check`** so Windows teammates
actually load skills.

## Mirror / copy — honest assessment

**Pros:**

- Works everywhere Git works; no symlink privilege.
- office-space marks mirrors with `.office-space-generated` and can detect `stale-mirror`.
- Safe to commit _if_ CI enforces sync (or regenerate in bootstrap).

**Cons:**

- Stale unless every edit re-runs sync.
- Larger diffs; risk of editing the copy by mistake (`unmanaged` / drift).

## Decision rule (use this)

```text
targets ⊆ native-.agents clients (Codex, Copilot, Devin, Antigravity; Cursor if verified)?
  → commit .agents/skills only. No adapter.

need Claude?
  → bridge .claude/skills (required).

Cursor .agents discovery flaky on your build?
  → bridge .cursor/skills (reliability).

Unix-only / symlink-safe team?
  → directory symlink. Prefer generate locally; document clone setup.
mixed OS or commit adapters to git?
  → real copies + sync --write --mirror + CI sync --check.
client gains skillsPaths / reliable .agents scan?
  → delete the bridge.
```

## office-space mapping

| Goal             | Command                              | Mechanism      |
| ---------------- | ------------------------------------ | -------------- |
| Symlink adapters | `office-space sync --write`          | symlink        |
| Portable copies  | `office-space sync --write --mirror` | generated copy |

CLI: **`--mirror` is explicit** — Windows does not auto-select mirror via the CLI flag alone; pass
it when you want copies. That dual path matches industry practice: **symlink when safe, copy when
portable** — not “symlinks always.”

## What not to do

- Symlink _and_ mirror the same path.
- Add `.cursor/skills` / Codex adapters “just in case” when those clients already read
  `.agents/skills/`.
- Commit gitmode `120000` symlinks without a Windows clone story.
- Treat symlink UI bugs as “skills missing” without filesystem verification.
