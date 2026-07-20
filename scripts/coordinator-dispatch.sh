#!/usr/bin/env bash
# coordinator-dispatch.sh — 自动派单 CLI 入口
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ORCH="$(cd "$HERE/.." && pwd)"
cd "$ORCH"
exec node "$HERE/coordinator-dispatch.mjs" "$@"
