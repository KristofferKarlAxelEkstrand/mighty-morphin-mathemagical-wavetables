# Ship checklist

## Location

- [ ] Lives under `.agents/skills/<name>/` (source of truth)
- [ ] Folder name matches `name` frontmatter
- [ ] Not authored only in `.claude/` / `.cursor/` / `.devin/`
- [ ] If this repo uses adapters: `office-space sync --check` clean (or `--write` after add)

## Frontmatter

- [ ] `name`: ≤64, `[a-z0-9-]+`, no leading/trailing/double hyphens
- [ ] `description`: ≤1024, WHAT + WHEN, trigger terms, third person
- [ ] No broken YAML (quote values with `:`)

## Body

- [ ] Gathered purpose, triggers, and source (or inferred) before writing
- [ ] Short procedure; no filler the model already knows
- [ ] Default tool/path chosen; alternatives minimal
- [ ] Gotchas in `SKILL.md` if any (not only in a reference)
- [ ] References linked one level deep with explicit load triggers
- [ ] Started from a template/skeleton when creating a new skill
- [ ] Scripts referenced by relative path; runnable non-interactively
- [ ] Canonical path is `.agents/skills/` (not `.cursor/skills/` as source of truth)

## Tokens

- [ ] Catalog description alone is enough to _select_ the skill
- [ ] `SKILL.md` body lean (well under ~5k tokens guidance)
- [ ] Heavy docs / tables / long examples in `references/`
- [ ] Repeated logic in `scripts/`, not pasted into markdown

## Smoke

- [ ] Open `SKILL.md` cold: can an agent execute without the chat that created it?
- [ ] Trigger phrases in the description match how users ask
- [ ] Frontmatter valid (name matches folder; WHAT+WHEN description); if developing the office-space
      package, `npm run validate:skills` also passes
