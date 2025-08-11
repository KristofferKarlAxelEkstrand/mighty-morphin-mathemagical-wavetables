# Git Hooks

This project uses Husky for git hooks to maintain code quality.

## Pre-commit Hook

Before each commit, the following automatically happens:

1.  **Prettier** formats all markdown, JSON, YAML files
2.  **Markdownlint** fixes common markdown issues

This ensures all committed files are properly formatted and linted.

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
