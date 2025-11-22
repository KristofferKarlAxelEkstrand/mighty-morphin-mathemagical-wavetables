# Husky - Git Hooks Automation

## What is Husky?

Husky is a tool that makes Git hooks easy to use in Node.js projects. Git hooks are scripts that run automatically at specific points in your Git workflow (like before committing or pushing code).

In this project, Husky runs **pre-commit hooks** that automatically check and fix your code before it gets committed.

## Why We Use Husky

**Automated Quality Control**: Husky ensures that every commit meets our quality standards without manual effort.

**Consistency**: Everyone on the project gets the same code formatting and linting checks automatically.

**Catch Issues Early**: Problems are found and fixed before they enter the codebase, keeping the repository clean.

**Save Time**: No need to remember to run linters and formatters manually - Husky does it for you.

## How It Works in This Project

### Installation

Husky is installed as a Node.js dev dependency:

```bash
npm install
```

This runs the `prepare` script which initializes Husky hooks.

### Pre-Commit Hook

When you run `git commit`, Husky automatically:

1.  **Runs lint-staged** - checks only the files you're committing
2.  **Formats Markdown** - uses Prettier to format `.md` files
3.  **Fixes Markdown linting** - uses markdownlint to check and fix Markdown
4.  **Formats JSON/YAML** - uses Prettier for config files

### Configuration Files

**`.husky/pre-commit`**

```bash
npx lint-staged
```

**`package.json` (lint-staged section)**

```json
"lint-staged": {
  "*.md": [
    "prettier --write",
    "markdownlint --fix"
  ],
  "*.{json,yml,yaml}": [
    "prettier --write"
  ]
}
```

### What Gets Checked

**Markdown files (`.md`):**

-  Auto-formatted with Prettier (120 chars line width)
-  Linted with markdownlint (checks for common issues)
-  Auto-fixed where possible

**JSON/YAML files:**

-  Auto-formatted with Prettier
-  Consistent indentation and formatting

## Project Integration

### Python + Node.js Hybrid

This is primarily a **Python project**, but we use Node.js tools (Husky, Prettier, markdownlint) for **documentation quality**.

-  **Python code** → checked with Ruff (linting/formatting), mypy (type checking), Bandit (security)
-  **Documentation** → checked with Husky, Prettier, markdownlint

### Workflow Example

```bash
# 1. Edit some documentation
vim README.md

# 2. Stage your changes
git add README.md

# 3. Commit (Husky runs automatically)
git commit -m "Update documentation"
# → Prettier formats README.md
# → markdownlint checks for issues
# → Files are automatically fixed and re-added
# → Commit proceeds with formatted files

# 4. Push (no additional hooks)
git push
```

### Bypassing Hooks (Not Recommended)

If you need to skip hooks in an emergency:

```bash
git commit --no-verify -m "Emergency fix"
```

**Note**: Only use `--no-verify` when absolutely necessary. Let the hooks run normally to maintain code quality.

## Commands

### Manual Formatting

You can run the formatters manually without committing:

```bash
# Format all Markdown and JSON/YAML files
npm run format

# Check formatting without changing files
npm run format:check

# Format and fix Markdown linting
npm run format:fix

# Lint only Markdown files
npm run lint:md

# Fix Markdown linting issues
npm run lint:md:fix
```

## Benefits for This Project

1.  **Consistent Documentation**: All Markdown files follow the same style
2.  **Professional Quality**: README, docs, and guides are always well-formatted
3.  **No Manual Work**: Formatting happens automatically on commit
4.  **Focus on Content**: Write documentation, let tools handle the formatting
5.  **Clean History**: Every commit has properly formatted files

## Technical Details

**Husky Version**: 9.1.7
**Node Version Required**: ≥22.0.0

**Tools Used**:

-  `husky` - Git hooks manager
-  `lint-staged` - Run linters on staged files only
-  `prettier` - Code formatter for Markdown/JSON/YAML
-  `markdownlint` - Markdown linting and style checking

## Troubleshooting

**Hooks not running?**

```bash
# Reinstall Husky hooks
npm run prepare
```

**Want to update tools?**

```bash
npm run update
```

**Commit blocked by linting errors?**
Fix the issues reported, or check the logs to see what needs attention.

## Summary

Husky makes our documentation quality **automatic and consistent**. It runs in the background, keeps our Markdown files clean, and ensures every commit meets our standards - all without any manual effort.
