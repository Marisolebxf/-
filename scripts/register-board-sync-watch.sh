#!/usr/bin/env bash
# register-board-sync-watch.sh — macOS launchd projector (optional). No WSL.
#
# Usage:
#   ./scripts/register-board-sync-watch.sh           # install (every 3600s / 1h)
#   ./scripts/register-board-sync-watch.sh uninstall
#   ./scripts/register-board-sync-watch.sh --minutes 60

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LABEL="com.gkx.boardsyncwatch"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
MINUTES=60
ACTION=install

while [[ $# -gt 0 ]]; do
  case "$1" in
    uninstall) ACTION=uninstall; shift ;;
    --minutes) MINUTES="$2"; shift 2 ;;
    *) echo "Unknown: $1" >&2; exit 2 ;;
  esac
done

SECONDS_INTERVAL=$((MINUTES * 60))
WATCH="$ROOT/scripts/board-sync-watch.sh"

if [[ "$ACTION" == "uninstall" ]]; then
  launchctl unload "$PLIST" 2>/dev/null || true
  rm -f "$PLIST"
  echo "Unregistered: $LABEL"
  exit 0
fi

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js 18+ required on projector Mac." >&2
  exit 1
fi

mkdir -p "$HOME/Library/LaunchAgents" "$ROOT/agent-delivery/_tmp"

# Resolve node absolute path for launchd
NODE_BIN="$(command -v node)"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>${LABEL}</string>
  <key>WorkingDirectory</key><string>${ROOT}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>${WATCH}</string>
    <string>--outbound-only</string>
  </array>
  <key>StartInterval</key><integer>${SECONDS_INTERVAL}</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>${ROOT}/agent-delivery/_tmp/board-sync-watch.launchd.out.log</string>
  <key>StandardErrorPath</key><string>${ROOT}/agent-delivery/_tmp/board-sync-watch.launchd.err.log</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:${NODE_BIN%/*}</string>
  </dict>
</dict>
</plist>
EOF

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "Registered $LABEL every ${MINUTES} min"
echo "  Plist: $PLIST"
echo "  After Feishu sync: commit+push task-registry if changed"
echo "  Log:   $ROOT/agent-delivery/_tmp/board-sync-watch.log"
echo "Projector only. Ensure non-interactive git push credentials."
echo "Engineers use ./scripts/update-task-status.sh"
