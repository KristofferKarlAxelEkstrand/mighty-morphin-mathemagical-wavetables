# Git Hooks

This project uses Husky for git hooks to maintain code quality.

## Pre-commit Hook

Before each commit, lint-staged runs on staged files:

1. **Ruff** formats and lints Python
2. **Prettier** formats Markdown, JSON, and YAML
3. **markdownlint** checks Markdown

See `docs/tech/husky.md`.

## Manual Commands

```bash
# Format and fix everything
npm run format:fix

# Just format
npm run format

# Just lint markdown
npm run lint:md:fix
```

## Skipping Hooks (Emergency Only)

If you absolutely need to skip the pre-commit hook:

```bash
git commit --no-verify -m "your message"
```

**Note:** Only use `--no-verify` in emergencies. The hooks help maintain code quality!
