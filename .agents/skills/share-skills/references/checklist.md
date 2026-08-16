# Ship checklist — cross-agent skill visibility

## Canonical

- [ ] Skill authored only under `.agents/skills/<name>/`
- [ ] `name` frontmatter matches folder
- [ ] No duplicate hand-maintained copies under `.claude/`, `.cursor/`, `.devin/`, `.github/`

## Coverage

- [ ] Target harnesses listed; matrix + each relevant `harness-*.md` consulted
- [ ] Native clients (Codex/Copilot/Devin/Antigravity): **no** unnecessary vendor trees
- [ ] Claude: `.claude/skills` bridge healthy
- [ ] Cursor: either `.agents/` verified as Skills, or `.cursor/skills` bridged
- [ ] Holdout bridges chosen via bridge-choice (symlink vs mirror), not by habit
- [ ] Mixed-OS / committed adapters: prefer mirror + CI `sync --check`, not bare git symlinks

## Sync (office-space)

- [ ] `office-space sync --check` clean for skills adapters
- [ ] Windows/no-symlink path documented; re-sync after skill edits
- [ ] No `unmanaged` / `broken-symlink` / `stale-mirror` left unresolved
- [ ] Team knows whether adapters are committed or generated post-clone

## Prove

- [ ] For each holdout: adapter is `symlink` or fresh `generated-mirror` (not merely doctor-green
      with `missing`)
- [ ] Filesystem test: canonical + each required adapter path resolves to the same `SKILL.md`
- [ ] At least one real client invocation (implicit or `/skill`) succeeded
- [ ] Team docs note “run sync after clone” when symlinks are not committed or OS differs
- [ ] WSL vs Windows Git story covered if both check out the repo
