# GitHub Copilot / VS Code

**Sources:**
[About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills),
[VS Code agent skills](https://code.visualstudio.com/docs/agent-customization/agent-skills),
[add skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills).

## Discovery paths

| Scope    | Path                                                                      |
| -------- | ------------------------------------------------------------------------- |
| Project  | `.agents/skills/`, `.github/skills/`, `.claude/skills/`                   |
| Personal | `~/.agents/skills/`, `~/.copilot/skills/` (and often `~/.claude/skills/`) |

Works with Copilot cloud agent, Copilot CLI, VS Code / JetBrains agent mode (per GitHub docs).

VS Code setting `chat.agentSkillsLocations` can add extra project roots.

## Bridge

**None required** for canonical `.agents/skills/`.

Optional `.github/skills` mirror only if the team wants Copilot-centric paths or older habits —
**not** created by `office-space sync` (`trackedDiscovery` is manifest-only today).

Community “awesome-copilot” guidance still often shows `.github/skills/` as the _example_ project
path; `.agents/skills/` remains supported.

## Invoke / verify

- `/` skills list in chat / CLI
- `gh skill` / Copilot CLI skill subcommands for install/list
- Coding agent should load on matching `description`

## Gotchas

- Prefer one project location to avoid duplicate `name` confusion (`.agents/` + `.github/` +
  `.claude/` all populated with copies).
- Personal `~/.copilot/skills` vs `~/.agents/skills` — pick one for user-global skills.

## office-space

No `localDiscovery` entry required. Do not invent a sync for `.github/skills` unless product code
gains it.
