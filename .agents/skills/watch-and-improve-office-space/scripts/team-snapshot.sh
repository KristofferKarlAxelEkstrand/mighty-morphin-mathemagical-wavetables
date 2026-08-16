#!/usr/bin/env bash
# One-shot status for watch-and-improve-office-space.
# Usage: team-snapshot.sh [workflow]
set -euo pipefail

# Package root markers: monorepo (src/cli.js) or flat published (cli.js + package.json name).
# Host markers: .agents/office-space under a checkout.
is_root_candidate() {
    local d="$1"
    if [ -f "$d/src/cli.js" ] || [ -d "$d/.agents/office-space" ]; then
        return 0
    fi
    if [ -f "$d/cli.js" ] && [ -f "$d/package.json" ] &&
        grep -q '@kristoffer-karl-axel-ekstrand/office-space' "$d/package.json" 2>/dev/null; then
        return 0
    fi
    return 1
}

walk_for_root() {
    local d="$1"
    while [ -n "$d" ] && [ "$d" != "/" ]; do
        if is_root_candidate "$d"; then
            printf '%s\n' "$d"
            return 0
        fi
        d="$(dirname "$d")"
    done
    return 1
}

resolve_root() {
    local script_dir d
    # Primary: walk from script dir (realpath so symlink/absolute invoke cannot mis-root).
    script_dir="$(cd "$(dirname "$(realpath "${BASH_SOURCE[0]:-$0}")")" && pwd)"
    if d="$(walk_for_root "$script_dir")"; then
        printf '%s\n' "$d"
        return 0
    fi
    # Secondary: walk from PWD (operator ran from a host checkout).
    # OFFICE_SPACE_ROOT still scopes the workflow tree via OS_ROOT below — it is not the package root.
    if d="$(walk_for_root "$PWD")"; then
        printf '%s\n' "$d"
        return 0
    fi
    # Fail soft: report PWD and say it is not a package/host root.
    echo "team-snapshot: no package/host root from script or PWD; using PWD=$PWD" >&2
    printf '%s\n' "$PWD"
}

ROOT="$(resolve_root)"
WF="${1:-developer-team}"
OS_ROOT="${OFFICE_SPACE_ROOT:-$ROOT/.agents/office-space}"
WF_ROOT="$OS_ROOT/$WF"
HEALTH="$WF_ROOT/health"
SESSION="${WF}-agents"

echo "=== snapshot $(date -u +%Y-%m-%dT%H:%M:%SZ) workflow=$WF ==="
echo "repo=$ROOT"

if [ -f "$ROOT/src/cli.js" ]; then
    (cd "$ROOT" && node src/cli.js team status "$WF" 2>&1) || true
elif [ -f "$ROOT/cli.js" ]; then
    (cd "$ROOT" && node cli.js team status "$WF" 2>&1) || true
elif command -v office-space >/dev/null 2>&1; then
    (cd "$ROOT" && office-space team status "$WF" 2>&1) || true
else
    echo "(no cli — skip team status)"
fi

echo
if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "tmux: UP ($SESSION)"
    # -s = this session only (never -a: fixtures/qualify pollute the list)
    tmux list-panes -t "$SESSION" -s \
        -F '  #{window_name}.#{pane_index} cmd=#{pane_current_command} title=#{pane_title}' 2>/dev/null || true
else
    echo "tmux: DOWN (no session $SESSION)"
fi

other="$(tmux ls -F '#{session_name}' 2>/dev/null | grep -v "^${SESSION}$" || true)"
if [ -n "${other:-}" ]; then
    echo "other tmux sessions (ignore for this workflow):"
    printf '%s\n' "$other" | sed 's/^/  /'
fi

if [ -f "$HEALTH/session-binding.log" ]; then
    stops="$(grep -c 'stop_team' "$HEALTH/session-binding.log" 2>/dev/null || true)"
    stops="${stops:-0}"
    echo "session-binding.log stop_team lines: $stops"
    if [ "$stops" != "0" ]; then
        grep 'stop_team' "$HEALTH/session-binding.log" 2>/dev/null | tail -3 | sed 's/^/  /' || true
    fi
fi

echo
if [ -f "$HEALTH/uptime.log" ]; then
    echo "uptime.log (last 8):"
    tail -8 "$HEALTH/uptime.log" | sed 's/^/  /'
fi

if [ -d "$HEALTH/alerts" ]; then
    # portable count
    alerts=0
    for f in "$HEALTH/alerts"/*; do
        [ -f "$f" ] || continue
        alerts=$((alerts + 1))
    done
    echo "alerts: $alerts"
    if [ "$alerts" -gt 0 ]; then
        for f in "$HEALTH/alerts"/*; do
            [ -f "$f" ] || continue
            echo "  $(basename "$f"): $(tr '\n' ' ' <"$f" | head -c 200)"
        done
    fi
fi

if [ -d "$WF_ROOT/.temp" ]; then
    echo "await locks:"
    shopt -s nullglob 2>/dev/null || true
    for f in "$WF_ROOT/.temp"/.await-lock-*.json; do
        [ -f "$f" ] || continue
        agent="$(basename "$f" .json)"
        agent="${agent#.await-lock-}"
        pid="$(sed -n 's/.*"pid"[[:space:]]*:[[:space:]]*\([0-9][0-9]*\).*/\1/p' "$f" | head -1)"
        if [ -n "${pid:-}" ] && kill -0 "$pid" 2>/dev/null; then
            state=LIVE
        else
            state=DEAD
        fi
        echo "  $agent pid=${pid:-?} $state"
    done
fi

mail_n=0
for f in "$WF_ROOT/mail/in"/*; do
    [ -f "$f" ] || continue
    mail_n=$((mail_n + 1))
done
unread=0
if [ -d "$WF_ROOT/slack" ]; then
    while IFS= read -r -d '' f; do
        unread=$((unread + 1))
    done < <(find "$WF_ROOT/slack" -maxdepth 2 -type f ! -path '*/read/*' ! -path '*/all/*' \
        ! -path '*/health-monitor/*' ! -path '*/quarantine/*' -print0 2>/dev/null || true)
fi
echo "mail/in files: $mail_n  slack unread (excl all/read): $unread"

if [ -d "$WF_ROOT/tasks" ]; then
    echo "board counts:"
    for stage in todo working-on "done"; do
        n=0
        for f in "$WF_ROOT/tasks/$stage"/*.md; do
            [ -f "$f" ] || continue
            n=$((n + 1))
        done
        echo "  tasks/$stage: $n"
    done
fi

if [ -d "$HEALTH/reports" ]; then
    latest=""
    for f in "$HEALTH/reports"/*.md; do
        [ -f "$f" ] || continue
        if [ -z "$latest" ] || [ "$f" -nt "$latest" ]; then
            latest="$f"
        fi
    done
    if [ -n "$latest" ]; then
        echo "latest report: $(basename "$latest")"
    fi
fi
