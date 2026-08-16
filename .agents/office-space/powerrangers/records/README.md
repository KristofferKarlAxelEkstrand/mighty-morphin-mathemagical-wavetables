# Durable workflow records

This folder is the tracked continuity layer. Live mail, Slack, tasks, health, and memory logs are
runtime state and are ignored by Git.

| Folder         | Durable content                                                      |
| -------------- | -------------------------------------------------------------------- |
| `checkpoints/` | Restart state and exact resume actions for active or human-held work |
| `decisions/`   | Human product, gate, and workflow decisions                          |
| `memory/`      | Compacted lessons promoted from live per-agent memory                |
| `retros/`      | Workflow retrospectives and measured operating changes               |

Use `office-space state checkpoint powerrangers` before maintenance or shutdown. A task entering
`human` or `blocked` receives its own checkpoint automatically. Once answered, promote the result
into the relevant canonical spec or evidence file and remove the resolved checkpoint in a normal
reviewed change.

`office-space state compact powerrangers` writes a pre-compaction checkpoint before applying this
workflow's configured retention values (see `space.json` `state.retention`). Health report keep
count is `state.retention.healthReports` (default 3): continuous `health-report` write-prune and
`state compact` both honor it. Write-prune deletes only `[HEALTH-REPORT]-*` files; compact may thin
all files under `health/reports/` by mtime. Invalid `healthReports` values default to 3.
