import { existsSync } from "node:fs";

const skipDir = (file) =>
  file.includes("/.agents/") ||
  file.startsWith(".agents/") ||
  file.includes("/.claude/") ||
  file.startsWith(".claude/") ||
  file.includes("/.devin/") ||
  file.startsWith(".devin/");

const keep = (files) => files.filter((file) => !skipDir(file) && existsSync(file));

export default {
  "*.md": (files) => {
    const staged = keep(files);
    if (staged.length === 0) {
      return [];
    }
    return [`prettier --write ${staged.join(" ")}`, `markdownlint --fix ${staged.join(" ")}`];
  },
  "*.{json,yml,yaml}": (files) => {
    const staged = keep(files).filter((file) => !file.endsWith("package-lock.json"));
    if (staged.length === 0) {
      return [];
    }
    return [`prettier --write ${staged.join(" ")}`];
  },
  "*.py": (files) => {
    if (files.length === 0) {
      return [];
    }
    const list = files.join(" ");
    return [`python -m ruff format ${list}`, `python -m ruff check --fix ${list}`];
  },
};
