# tmux technical reference

## Architecture

tmux is a terminal multiplexer built from four layers:

1. **Server** — one daemon per socket. Holds all sessions, windows, panes, buffers, and
   global/server options.
2. **Session** — a container of windows with a name (e.g. `myteam-agents`).
3. **Window** — a container of panes with an index and optional name; can be linked to multiple
   sessions.
4. **Pane** — a pseudo-terminal running a process.
5. **Client** — a process that attaches to a session and renders it.

Every `tmux` invocation is a client talking to the server over a Unix socket. The server starts
automatically on first use unless `-D` (no daemon) or `-N` (do not start) is used.

## Sockets and isolation

Default socket: `/tmp/tmux-$UID/default`. The directory prefix is controlled by `TMUX_TMPDIR`
(default `/tmp`).

```bash
# Private server (same UID, different socket name inside TMUX_TMPDIR)
tmux -L myserver new-session -d -s foo

# Private socket at an exact path (ignores -L and the default directory)
tmux -S /secure/tmux.sock new-session -d -s foo

# Private directory (create it first — tmux silently falls back to /tmp if missing)
mkdir -m700 /tmp/mytest-tmux
TMUX_TMPDIR=/tmp/mytest-tmux tmux new-session -d -s foo
```

Key properties:

- `TMUX_TMPDIR` is read **only when the server starts**. Setting it later is ignored.
- `-L <name>` creates a socket named `<name>` inside `TMUX_TMPDIR/tmux-$UID/`.
- `-S <path>` creates the socket at an exact path and overrides `-L`.
- The `tmux-UID` directory is created by tmux and must not be world-readable/writable.
- If `TMUX_TMPDIR` is missing, tmux silently falls back to `/tmp` **unless** the directory was
  expected to exist. For deterministic test isolation, always `mkdir -p` and `chmod 700` the desired
  `TMUX_TMPDIR` before the first `tmux` command.
- On some filesystems (network/passthrough mounts, e.g. WSL2's drvfs/9p) `chmod 700` can report
  success while the directory is still readable/writable by others — tmux's own safety check then
  rejects it as "unsafe permissions" regardless of the chmod exit code. Verify with
  `stat -c '%a' "$dir"` after chmod, don't trust the exit code alone; if it still comes back wrong,
  put `TMUX_TMPDIR` under a genuine local filesystem (e.g. `/tmp`) instead of a repo directory that
  might be on such a mount.
- Use `tmux -L name` (or `-S path`) on **every** command that targets a non-default server.
- **Nested tmux: `$TMUX` beats `TMUX_TMPDIR`.** If a script that sets `TMUX_TMPDIR` is itself
  running inside an existing tmux pane, the inherited `$TMUX` (pointing at the _outer_ session's
  socket) takes priority over `TMUX_TMPDIR` for every subsequent tmux invocation — private-socket
  isolation silently never engages. Verified directly: with `TMUX_TMPDIR` exported but `$TMUX` still
  inherited, `tmux new-session` landed on the outer session's default socket; nothing was ever
  created at the isolated path. Fix: `unset TMUX` immediately after setting `TMUX_TMPDIR`, before
  the first tmux call. Skipping this is dangerous, not just ineffective — a `cleanup()` trap calling
  `tmux kill-server`, believing it's isolated, instead kills the outer session. See
  `selftest-run-team.sh`'s `setup_private_tmux()` in this repo for a working fix.

Inside a pane tmux sets:

- `TMUX` — socket path plus internal token. Use `[ -n "$TMUX" ]` to detect tmux.
- `TMUX_PANE` — pane ID like `%42`. Use `tmux display-message -t "$TMUX_PANE"` to query the pane
  from inside or outside tmux.

## Identifiers and targets

Three identifiers exist for each object:

| Object  | Stable ID | Index                  | Name           |
| ------- | --------- | ---------------------- | -------------- |
| Session | `$N`      | none                   | `session-name` |
| Window  | `@N`      | `0,1,2…`               | `window-name`  |
| Pane    | `%N`      | `0,1,2…` within window | none           |

**Prefer IDs over indexes.**

- Window and pane indexes are **renumbered** when a window or pane is closed.
- A recorded pane index can silently point to a different pane after one dies.
- Pane, window, and session IDs are never reused within a server.

Target grammar for `-t`:

```
session:window.pane
session:window
session
window.pane    # needs current session
window         # needs current session
%N             # pane ID only
@N             # window ID only
$N             # session ID only
```

Examples:

```bash
tmux send-keys -t mysess:@7.%42 'echo hi' C-m
tmux capture-pane -t '%42' -p
tmux kill-pane -t '%42'
```

## Scripting commands

Most commands accept `-t <target>`. Common automation commands:

```bash
# Create or check session
tmux has-session -t "$SESSION" 2>/dev/null   # exit 0 if exists
tmux new-session -d -s "$SESSION" -n win -c "$DIR"

# Windows and panes
tmux new-window -d -t "$SESSION" -n monitor -c "$DIR"
tmux split-window -d -t "$SESSION:win" -c "$DIR"
tmux split-window -h -t "$SESSION:win" -c "$DIR"
tmux select-layout -t "$SESSION" tiled

# Send input
tmux send-keys -t "$SESSION:win.%1" 'echo hi' C-m

# Lifecycle
tmux respawn-pane -k -t '%42'              # kill and restart
tmux respawn-pane -t '%42'                 # restart dead pane with same command
tmux kill-pane -t '%42'
tmux kill-session -t "$SESSION"
tmux kill-server
```

`send-keys` caveats:

- Literal text is sent as keystrokes; do not use for untrusted input.
- `C-m` is Enter. `C-c` sends SIGINT to the foreground process.
- `Space` is the keyword for a space; quote literal text or use a script.
- For complex commands, write a script to disk and run it so keystrokes never have to survive
  quoting.

## Format strings

`-F` (or `-P` with `display-message`) expands tmux format variables. These are essential for
extracting state:

```bash
# All panes with stable IDs, PID, command, cwd
tmux list-panes -a -F '#{pane_id} #{pane_pid} #{pane_current_command} #{pane_current_path}'

# All windows
tmux list-windows -a -F '#{session_name} #{window_id} #{window_index} #{window_name}'

# Query a single pane
tmux display-message -t '%42' -p '#{pane_current_command} #{pane_pid}'
```

Useful automation variables:

| Variable                          | Meaning                                                           |
| --------------------------------- | ----------------------------------------------------------------- |
| `#{pane_id}`                      | Stable pane ID `%N`                                               |
| `#{window_id}`                    | Stable window ID `@N`                                             |
| `#{session_id}`                   | Stable session ID `$N`                                            |
| `#{pane_pid}`                     | PID of the first process spawned in the pane                      |
| `#{pane_current_command}`         | Name of the current foreground command (can be stale/approximate) |
| `#{pane_current_path}`            | Current working directory                                         |
| `#{pane_tty}`                     | TTY path of the pane; use with `ps -t`                            |
| `#{pane_active}`                  | `1` if this pane is active in its window                          |
| `#{window_active}`                | `1` if this window is active in its session                       |
| `#{window_index}`                 | Numeric index (can change)                                        |
| `#{window_name}`                  | Window name                                                       |
| `#{session_name}`                 | Session name                                                      |
| `#{socket_path}`                  | Path to the server socket                                         |
| `#{client_name}`, `#{client_tty}` | Client metadata                                                   |

**Detecting the real foreground process.** `pane_current_command` is heuristic and can be wrong for
shell scripts, `less` invoking `$EDITOR`, or programs with child processes. More reliable:

```bash
# Last line of ps for the pane's TTY (Linux)
tmux run "ps -o comm= -t '#{pane_tty}'" | tail -1

# Or use pane_pid plus process tree
pane_pid=$(tmux display-message -t '%42' -p '#{pane_pid}')
ps -o comm= --ppid "$pane_pid" | tail -1
```

## Control mode

`tmux -C` (or `-CC`) starts a control-mode client. This is a text protocol for external programs:

```bash
tmux -C attach-session -t mysession
```

Properties:

- Commands are sent as plain text lines.
- Responses are wrapped in `%begin <time> <cmdnum>` … `%end <time> <cmdnum>` or
  `%error <time> <cmdnum> <msg>`.
- Asynchronous notifications are prefixed with `%` (e.g. `%output %42 text`, `%window-add @7`).
- Pane output is escaped and delivered as `%output` lines.
- `-C` leaves the terminal in canonical mode (useful for testing); `-CC` disables echo and sends a
  `\033P1000p` DSC sequence.
- Good for IDE integrations; overkill for most shell automation.

## Waiting and synchronization

`wait-for` provides named channels:

```bash
# Block until signaled (from another pane/process)
tmux wait-for mychannel

# Signal
tmux wait-for -S mychannel

# Lock-style
tmux wait-for -L mychannel   # acquire
tmux wait-for -U mychannel   # release
```

Caveats:

- Channels are server-local and volatile; they do not survive server restart.
- `run-shell` does not work correctly if the entire server exits, so a `pane-exited` hook may miss
  the last pane.
- Hooks on objects being destroyed (e.g. `pane-exited`) historically have had issues with per-pane
  hooks because the pane options are gone by the time the hook fires; prefer global hooks for
  `pane-exited`.

## Respawning and dead panes

`respawn-pane` and `respawn-window` restart the pane/window command without recreating the pane:

```bash
tmux respawn-pane -t '%42'          # restart with original command (only if pane is dead)
tmux respawn-pane -k -t '%42'       # kill existing process and restart
tmux respawn-pane -t '%42' bash     # start a new command in the same pane
```

`remain-on-exit` keeps a pane around after its command exits:

```bash
tmux set-option -t mysess:0 remain-on-exit on
tmux set-option -g remain-on-exit on   # all windows
```

When `remain-on-exit` is on and the command exits, the pane shows "Pane is dead" and can be
respawned.

## Capturing and piping pane output

```bash
# Capture visible pane content
tmux capture-pane -t '%42' -p

# Capture with line range (negative = scrollback)
tmux capture-pane -t '%42' -p -S -100 -E -1

# Preserve escape sequences/colors
tmux capture-pane -t '%42' -e -pS -1000

# Join wrapped lines
tmux capture-pane -t '%42' -J -pS -1000

# Pipe live output to a command
tmux pipe-pane -t '%42' -o 'cat >> /tmp/pane-%42.log'
tmux pipe-pane -t '%42'            # turn off
```

Differences:

- `capture-pane` is a one-shot snapshot of visible/scrollback content.
- `pipe-pane` streams output to a command as it is produced.
- `-e` keeps ANSI escape codes; strip them if you want plain text.
- `-J` joins wrapped lines (useful for logs).

## Hooks

`set-hook` runs tmux commands on events. Hooks can be global (`-g`), session (`-t session`), window
(`-t window`), or pane (`-t pane`).

```bash
# Global hook examples
tmux set-hook -g pane-exited 'display "Pane #{pane_id} died"'
tmux set-hook -g window-renamed 'run-shell "tmux-session-save #{session_name}"'
tmux set-hook -g session-closed 'run-shell "notify-send tmux \"Session closed\""'
```

Useful hooks for automation:

- `pane-exited` — pane process exited.
- `pane-died` — pane process died (non-zero or signal).
- `window-renamed` — window name changed.
- `session-closed` — session destroyed.
- `after-new-session`, `after-new-window`, `after-split-window` — after creation.

**Important:** hooks run synchronously and commands from a hook do not fire hooks again.
`run-shell -b` can be used for background work.

## Conditional and shell commands

`run-shell` executes a shell command or tmux command:

```bash
tmux run-shell "echo hello"
tmux run-shell -b "sleep 5 && tmux display delayed"   # background
tmux run-shell -C "new-window"                        # execute as tmux command
```

`if-shell` branches on a shell command or a format expression:

```bash
tmux if-shell 'test $(date +%H) -lt 12' 'renamew morning' 'renamew afternoon'
tmux if-shell -F '#{>:#{session_windows},1}' 'display "many windows"'
```

`%if` in config files is parsed at load time; `if-shell` is a runtime command.

## Environment variables and options

Inside panes:

- `TMUX` — socket path and internal token. Test with `[ -n "$TMUX" ]`.
- `TMUX_PANE` — current pane ID.
- `TMUX_TMPDIR` — only meaningful **before** the server starts.

Options:

```bash
# Global option
tmux set-option -g status-style bg=blue

# Window option
tmux set-option -w -t mysess:0 monitor-activity on

# Session environment
tmux set-environment -t mysess MYVAR value

# Global environment
tmux set-environment -g MYVAR value

# Hidden environment (not inherited by new processes)
tmux set-environment -h MYVAR value

# Custom variable visible to formats
tmux set-option -g @myvar value
tmux display-message -p '#{@myvar}'
```

## Key bindings and key tables

Key tables: `prefix` (default `C-b`), `root`, `copy-mode`, `copy-mode-vi`, and custom tables.

```bash
# List bindings
tmux list-keys
tmux list-keys -T prefix
tmux list-keys -T copy-mode-vi

# Bind/unbind
tmux bind-key -T prefix r source-file ~/.tmux.conf \; display 'reloaded'
tmux unbind-key -T prefix C-b
```

## Layouts and pane sizing

Built-in layouts:

- `even-horizontal`, `even-vertical`
- `main-horizontal`, `main-vertical`
- `tiled`
- Custom layout strings (base64-ish tree description)

```bash
tmux select-layout -t mysess:win tiled
tmux resize-pane -t '%42' -x 80 -y 24
tmux resize-pane -t '%42' -R 5      # grow right by 5
tmux resize-pane -Z -t '%42'        # zoom/unzoom
```

`tiled-layout-max-columns` limits columns in tiled layout (default 0 = unlimited).

## Alerts and monitoring

- `monitor-activity` — flag window when non-active pane has activity.
- `monitor-bell` — flag on BEL.
- `monitor-silence` — flag after N seconds of no output.
- `visual-activity`, `visual-bell`, `visual-silence` — show in status line.

These are useful for dashboards, not for precise automation.

## Common pitfalls

1. **Pane/window index renumbering.** After `kill-pane` or `kill-window`, indexes are reused. Always
   store pane IDs (`%N`) or window IDs (`@N`), never indices.
2. **Default target ambiguity.** Commands run inside a pane use that pane as the default target.
   Scripts that run from outside tmux must always use `-t`.
3. **TMUX_TMPDIR race.** `TMUX_TMPDIR` is read when the server starts. Set it before the first
   `tmux` command and create the directory with mode 700.
4. **send-keys quoting.** Complex strings with quotes, spaces, or control chars are fragile. Prefer
   writing to a file and running it.
5. **Silent fallbacks.** If `TMUX_TMPDIR` is missing, tmux may silently fall back to `/tmp`. Always
   verify the directory exists.
6. **Server persistence.** The tmux server keeps running after all clients detach. Use
   `tmux kill-server` or `kill-session` to stop it.
7. **pane_current_command is heuristic.** It may return `bash` for a foreground process launched by
   a script. Use `pane_tty` + `ps` or `pane_pid` + process tree for accuracy.
8. **Hooks on destruction.** `pane-exited` hooks cannot reliably be per-pane because the pane is
   destroyed before the hook fires; use global hooks.
9. **pipe-pane single consumer.** Only one pipe can be attached to a pane at a time; a new
   `pipe-pane` closes the old one.
10. **respawn-pane and default-command.** If `default-command` is set, `respawn-pane` may invoke it
    instead of the original command. Verify behavior if you rely on respawn restarting the exact
    original command.
11. **`attach-session` doesn't fail safely inside a real pty.** Headless (stdout redirected to a
    file/pipe), an attach attempt fails immediately with "not a terminal" — easy to mistake for a
    universal safety net. From inside an actual terminal — including one that's itself a tmux pane —
    the same attach can succeed and hijack that pane's screen into the nested session instead of
    failing. Automation that creates a session for inspection, not interactive use, should always
    create it detached (`-d`) and never call `attach-session` at all, rather than relying on non-tty
    stdout to make attach fail.
12. **Nested `$TMUX` silently defeats `TMUX_TMPDIR` isolation.** See "Sockets and isolation" above —
    this is the single most expensive gotcha for testing agent automation that itself runs inside
    tmux.

## Best practices for automation

- **One session per workflow** with a descriptive name.
- **Private socket per test/environment** via `-L` or `TMUX_TMPDIR`.
- **Capture pane IDs from `new-window`/`split-window`** with `-P -F '#{pane_id}'` so you never rely
  on indexes.
- **Snapshot state with `list-panes -a -F`**, not `list-panes` default output.
- **Use `has-session` to test existence** before creating sessions in idempotent setup scripts.
- **Send input via scripts, not long `send-keys` strings.**
- **Clean up in `trap`:** `tmux kill-session -t "$SESSION"` on script exit.
- **For streaming output**, use `pipe-pane` or control mode; `capture-pane` is only a snapshot.
- **For live process detection**, combine `pane_pid`, `pane_tty`, and `ps` rather than
  `pane_current_command` alone.
- **Never parse human-readable `list-*` default output.** Always use `-F`.

## Useful command quick reference

```bash
tmux has-session -t NAME
tmux new-session -d -s NAME -n WIN -c DIR [command]
tmux new-window -d -t SESS -n WIN -c DIR [command]
tmux split-window -d -h -v -t TARGET -c DIR [command]
tmux list-sessions -F '#{session_id} #{session_name}'
tmux list-windows -a -F '#{session_name} #{window_id} #{window_name}'
tmux list-panes -a -F '#{pane_id} #{pane_pid} #{pane_current_command} #{pane_current_path}'
tmux send-keys -t TARGET 'text' C-m
tmux capture-pane -t TARGET -pS -1000
tmux pipe-pane -t TARGET -o 'cat >> /tmp/log'
tmux respawn-pane -k -t TARGET [command]
tmux kill-pane -t TARGET
tmux kill-session -t NAME
tmux kill-server
tmux display-message -t TARGET -p 'FORMAT'
tmux set-hook -g EVENT 'COMMAND'
tmux wait-for -S mychannel
tmux wait-for mychannel
tmux set-environment -g KEY value
tmux source-file ~/.tmux.conf
```

## Sources

- tmux man page: https://man7.org/linux/man-pages/man1/tmux.1.html
- tmux GitHub wiki — Control Mode: https://github.com/tmux/tmux/wiki/Control-Mode
- tmux GitHub wiki — Advanced Use: https://github.com/tmux/tmux/wiki/Advanced-Use
- Tao of tmux: https://tao-of-tmux.readthedocs.io/
- tmux scripting guide: https://tmux-tmux.mintlify.app/guides/scripting
- tmux source code: `cmd-respawn-pane.c`, `cmd-pipe-pane.c`, `cmd-wait-for.c`, `server.c`,
  `key-bindings.c`
