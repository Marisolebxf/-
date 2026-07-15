#!/usr/bin/env bash
# board-sync-watch.sh — Projector (macOS / Linux, always-on)
# git pull 主仓 → Feishu sync → commit+push task-registry (unless --no-git-push).
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

# Prerequisite: sync must run on latest main-orch registry.
branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
if [[ -z "$branch" ]]; then
  log "ERROR: not a git repo; abort before Feishu sync"
  exit 1
fi
log "git pull --rebase origin $branch (before Feishu sync)"
if [[ "$DRY" -eq 1 ]]; then
  log "[DRY] would git pull --rebase origin $branch"
else
  DID_STASH=0
  if [[ -n "$(git status --porcelain 2>/dev/null || true)" ]]; then
    log "local changes detected; stash before pull"
    if ! git stash push -m "board-sync-watch: auto-stash before pull $(date -Iseconds 2>/dev/null || date)" >>"$LOG" 2>&1; then
      log "ERROR: git stash failed; abort Feishu sync"
      exit 1
    fi
    DID_STASH=1
  fi
  PULL_OK=1
  if ! git fetch origin >>"$LOG" 2>&1; then
    log "ERROR: git fetch failed"
    PULL_OK=0
  elif ! git pull --rebase origin "$branch" >>"$LOG" 2>&1; then
    log "ERROR: git pull --rebase failed"
    PULL_OK=0
  fi
  if [[ "$DID_STASH" -eq 1 ]]; then
    log "restore stash after pull"
    if ! git stash pop >>"$LOG" 2>&1; then
      log "WARN: stash pop failed (conflict?); keep stash on stack, check git stash list"
    fi
  fi
  if [[ "$PULL_OK" -eq 0 ]]; then
    log "ERROR: git pull --rebase failed; abort Feishu sync"
    exit 1
  fi
  log "git pull ok on $branch"
fi

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
