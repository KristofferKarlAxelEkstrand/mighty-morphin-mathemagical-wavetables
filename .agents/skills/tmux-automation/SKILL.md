---
name: tmux-automation
description: >-
  Design, script, and debug tmux-based automation for office-space agents. Use when the user asks
  about tmux sessions, panes, send-keys, control mode, TMUX_TMPDIR, targets, sockets, respawn-pane,
  capture-pane, hooks, or testing agent workflows inside tmux.
---

# tmux automation

Script tmux as a headless pane manager for long-running co-workers.

## Do this

1. **Use one named session per workflow** (e.g. `developer-team-agents`).
2. **Create a private socket** with `-L <name>` or `TMUX_TMPDIR` so tests cannot collide with the
   user's default server.
3. **Use pane IDs (`%N`) and window IDs (`@N`)**, never indices, when storing references across
   restarts.
4. **Always pass `-t <target>`** when a script runs outside tmux; never rely on the default target.
5. **Extract state with `-F` formats**:
   ```bash
   tmux list-panes -a -F '#{pane_id} #{pane_pid} #{pane_current_command} #{pane_current_path}'
   ```
6. **Send input safely**: for complex commands, write a script to disk and run it; avoid fragile
   `send-keys` quoting.
7. **Clean up** with `tmux kill-session -t <session>` or `tmux kill-server` tied to the private
   socket.
8. **Detect pane state** with `pane_pid` / `pane_tty` plus `ps` rather than `pane_current_command`
   alone.
9. **Run `office-space sync --write` after adding the skill** if the repo uses harness mirrors.

## Load when

| File                                               | Open when                                                                                                                                  |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| [references/technical.md](references/technical.md) | Deep details on sockets, IDs, control mode, format strings, hooks, respawn, capture/pipe-pane, pitfalls, best practices, command reference |

## Gotchas

- `TMUX_TMPDIR` is only read when the tmux server starts; setting it later is ignored.
- A missing `TMUX_TMPDIR` directory makes tmux silently fall back to `/tmp` for the server socket.
- **Inside an existing tmux pane, inherited `$TMUX` beats `TMUX_TMPDIR`** for socket selection on
  every subsequent call — isolation silently never engages unless you also `unset TMUX`. A
  `cleanup()` trap doing `tmux kill-server`, believing it targets a private socket, then kills the
  pane's own outer session instead. Verified directly in this repo: `selftest-run-team.sh`'s
  `setup_private_tmux()` sets `TMUX_TMPDIR` _and_ `unset TMUX` for exactly this reason.
- `tmux attach-session` fails cleanly ("not a terminal") when headless, but succeeds and hijacks the
  screen when run from inside a real pty nested in another session — don't rely on headless failure
  as a safety net. Automation that creates a session for inspection should start it detached (`-d`)
  and never call `attach-session` at all.
- `send-keys` sends literal keystrokes, not shell-escaped text; quoting can surprise you.
- `kill-pane` / `kill-window` renumber remaining indices; pane/window IDs are stable.
- `TMUX` inside a pane contains the socket path up to the first comma.
- `pane_current_command` is heuristic; use `pane_pid` / `pane_tty` with `ps` for accurate foreground
  detection.
- `respawn-pane` may invoke `default-command` instead of the original pane command if that option is
  set.
- `pane-exited` hooks should be global, not per-pane, because the pane is destroyed before the hook
  fires.
