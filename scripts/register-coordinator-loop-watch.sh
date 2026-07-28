#!/usr/bin/env bash
# register-coordinator-loop-watch.sh — macOS launchd 注册 Mayor 定时建议（A3）
#
# Usage:
#   ./scripts/register-coordinator-loop-watch.sh
#   ./scripts/register-coordinator-loop-watch.sh --minutes 120
#   ./scripts/register-coordinator-loop-watch.sh --apply-leases
#   ./scripts/register-coordinator-loop-watch.sh uninstall

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LABEL="com.gkx.coordinatorloopwatch"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
MINUTES=120
APPLY_LEASES=0
ACTION=install

while [[ $# -gt 0 ]]; do
  case "$1" in
    uninstall) ACTION=uninstall; shift ;;
    --minutes) MINUTES="$2"; shift 2 ;;
    --apply-leases) APPLY_LEASES=1; shift ;;
    *) echo "Unknown: $1" >&2; exit 2 ;;
  esac
done

SECONDS_INTERVAL=$((MINUTES * 60))
WATCH="$ROOT/scripts/coordinator-loop-watch.sh"

if [[ "$ACTION" == "uninstall" ]]; then
  launchctl unload "$PLIST" 2>/dev/null || true
  rm -f "$PLIST"
  echo "Unregistered: $LABEL"
  exit 0
fi

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js 18+ required." >&2
  exit 1
fi

mkdir -p "$HOME/Library/LaunchAgents" "$ROOT/agent-delivery/_tmp"
NODE_BIN="$(command -v node)"

ARGS_XML="    <string>/bin/bash</string>
    <string>${WATCH}</string>"
if [[ "$APPLY_LEASES" -eq 1 ]]; then
  ARGS_XML="${ARGS_XML}
    <string>--apply-leases</string>"
fi

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>${LABEL}</string>
  <key>WorkingDirectory</key><string>${ROOT}</string>
  <key>ProgramArguments</key>
  <array>
${ARGS_XML}
  </array>
  <key>StartInterval</key><integer>${SECONDS_INTERVAL}</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>${ROOT}/agent-delivery/_tmp/coordinator-loop-watch.launchd.out.log</string>
  <key>StandardErrorPath</key><string>${ROOT}/agent-delivery/_tmp/coordinator-loop-watch.launchd.err.log</string>
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
echo "  Latest: $ROOT/agent-delivery/_tmp/coordinator-loop-latest.txt"
echo "  Log:    $ROOT/agent-delivery/_tmp/coordinator-loop-watch.log"
echo "Default: suggestions only. Use --apply-leases to clear expired claimed + push."
echo "Does NOT sync Feishu (use board-sync watch for that)."
