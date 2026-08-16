# Adapters — apply the chosen bridge

How to apply symlink or mirror after [bridge-choice.md](bridge-choice.md).

## Symlink (Unix / symlink-safe)

```bash
# from repo root — relative link
ln -sfn ../.agents/skills .claude/skills
ln -sfn ../.agents/skills .devin/skills
```

Or: `office-space sync --write` (creates/repairs `localDiscovery` symlinks).

Verify:

```bash
ls -la .claude/skills
test -f .claude/skills/<name>/SKILL.md
```

Prefer **not** committing the symlink unless every clone OS is symlink-safe. Many teams gitignore
harness adapters and run sync after clone.

## Mirror (portable / Windows CLI)

```bash
office-space sync --write --mirror
```

**Windows note:** the CLI always passes the `--mirror` flag through. `sync --write` alone does
**not** auto-mirror on Windows — pass `--mirror` explicitly (or call the library without overriding
`forceMirror`).

After editing `.agents/skills/**`, re-run mirror sync. Look for `.office-space-generated` inside the
adapter tree — do not hand-edit those files.

## office-space sync

```bash
office-space sync --check
office-space sync --write            # symlink (Unix-safe)
office-space sync --write --mirror   # real copies (required for portable/Windows via CLI)
```

Only paths in `adapters.localDiscovery` are synced (default: `.claude/skills`, `.devin/skills`).

| Status             | Meaning                           | Action                                                           |
| ------------------ | --------------------------------- | ---------------------------------------------------------------- |
| `symlink`          | Healthy link                      | None                                                             |
| `missing`          | No adapter                        | `--write` (holdouts need this even though doctor allows missing) |
| `broken-symlink`   | Dangling                          | `--write`                                                        |
| `generated-mirror` | Healthy copy                      | Re-mirror after skill edits                                      |
| `stale-mirror`     | Copy ≠ canonical                  | `--write --mirror`                                               |
| `unmanaged`        | Real foreign tree at adapter path | Move into `.agents/skills/`, remove unmanaged, then sync         |

## Config future

If Claude (or another holdout) gains project `skillsPaths: [".agents/skills"]`, remove that harness
from `localDiscovery` and delete the adapter. Native scan beats any bridge.
