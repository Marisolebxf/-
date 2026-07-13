#!/usr/bin/env bash
# board-sync-watch.sh — Projector (macOS / Linux, always-on)
# Feishu sync then commit+push task-registry (unless --no-git-push).
#
# Usage:
#   ./scripts/board-sync-watch.sh
#   ./scripts/board-sync-watch.sh --outbound-only
#   ./scripts/board-sync-watch.sh --bidirectional   # requires pwsh
#   ./scripts/board-sync-watch.sh --dry-run
#   ./scripts/board-sync-watch.sh --no-git-push

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p "$ROOT/agent-delivery/_tmp"
LOG="$ROOT/agent-delivery/_tmp/board-sync-watch.log"
log() { echo "[$(date -Iseconds 2>/dev/null || date)] $*" | tee -a "$LOG"; }

OUTBOUND_ONLY=1
DRY=0
NO_GIT=0
SPRINT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --outbound-only) OUTBOUND_ONLY=1; shift ;;
    --bidirectional) OUTBOUND_ONLY=0; shift ;;
    --dry-run) DRY=1; shift ;;
    --no-git-push) NO_GIT=1; shift ;;
    --sprint-id) SPRINT="$2"; shift 2 ;;
    *) echo "Unknown: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$SPRINT" ]]; then
  SPRINT="$(grep -E '^\s*current_sprint:' "$ROOT/agent-delivery/scrum-sprint.yaml" | head -1 | sed -E 's/.*:\s*"?([^"]+)"?.*/\1/' | tr -d '[:space:]')"
fi

log "board-sync-watch start sprint=$SPRINT outboundOnly=$OUTBOUND_ONLY dryRun=$DRY noGitPush=$NO_GIT"

if [[ "$OUTBOUND_ONLY" -eq 0 ]]; then
  if command -v pwsh >/dev/null 2>&1; then
    if [[ "$DRY" -eq 1 ]]; then
      pwsh -File "$ROOT/scripts/sync-feishu-bitable-bidirectional.ps1" -DryRun -SprintId "$SPRINT"
    else
      pwsh -File "$ROOT/scripts/sync-feishu-bitable-bidirectional.ps1" -DryRun:$false -SprintId "$SPRINT"
    fi
  else
    log "WARN: --bidirectional needs pwsh; falling back to Node outbound-only (no WSL required)"
    OUTBOUND_ONLY=1
  fi
fi

if [[ "$OUTBOUND_ONLY" -eq 1 ]]; then
  if ! command -v node >/dev/null 2>&1; then
    log "ERROR: Node.js 18+ required"
    exit 1
  fi
  if [[ -f "$ROOT/.env" ]]; then set -a; # shellcheck disable=SC1091
    # shellcheck source=/dev/null
    source "$ROOT/.env"; set +a; fi
  ARGS=(node "$ROOT/scripts/lib/board-task-status.mjs" --watch-outbound)
  [[ -n "$SPRINT" ]] && ARGS+=(--sprint-id "$SPRINT")
  [[ "$DRY" -eq 1 ]] && ARGS+=(--dry-run)
  "${ARGS[@]}"
fi

if [[ "$NO_GIT" -eq 0 ]]; then
  log "git-push-registry after Feishu sync"
  if [[ "$DRY" -eq 1 ]]; then
    bash "$ROOT/scripts/lib/git-push-registry.sh" --dry-run || true
  else
    bash "$ROOT/scripts/lib/git-push-registry.sh" || log "WARN: git-push-registry exit nonzero (soft)"
  fi
else
  log "git push skipped (--no-git-push)"
fi

log "board-sync-watch ok"
