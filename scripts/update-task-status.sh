#!/usr/bin/env bash
# update-task-status.sh — macOS / Linux entry (Node 18+). WSL NOT required.
#
# Usage:
#   ./scripts/update-task-status.sh --task-id ENT-X --status review
#   ./scripts/update-task-status.sh --task-id ENT-X --status claimed --claimed-by "human:孔东"
#   ./scripts/update-task-status.sh --task-id ENT-X --heartbeat
#   ./scripts/update-task-status.sh --task-id ENT-X --status review --no-sync

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js 18+ required (not found on PATH). WSL is NOT required." >&2
  exit 1
fi

exec node "$ROOT/scripts/lib/board-task-status.mjs" "$@"
