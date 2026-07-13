#!/usr/bin/env bash
# git-push-registry.sh — projector: commit+push task-registry after Feishu sync (soft-fail on push)
# Usage:
#   ./scripts/lib/git-push-registry.sh
#   ./scripts/lib/git-push-registry.sh --dry-run

set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
mkdir -p "$ROOT/agent-delivery/_tmp"
LOG="$ROOT/agent-delivery/_tmp/board-sync-watch.log"
log() { echo "[$(date -Iseconds 2>/dev/null || date)] git-push-registry: $*" | tee -a "$LOG"; }

DRY=0
[[ "${1:-}" == "--dry-run" ]] && DRY=1

PATHS=(
  "agent-delivery/task-registry.yaml"
  "agent-delivery/bitable-inbound-proposals.yaml"
)

CHANGED=()
for p in "${PATHS[@]}"; do
  [[ -e "$p" ]] || continue
  if [[ -n "$(git status --porcelain -- "$p" 2>/dev/null || true)" ]]; then
    CHANGED+=("$p")
  fi
done

if [[ ${#CHANGED[@]} -eq 0 ]]; then
  log "no registry changes; skip commit/push"
  exit 0
fi

log "changes: ${CHANGED[*]}"

if [[ "$DRY" -eq 1 ]]; then
  log "[DRY] would commit+push registry"
  exit 0
fi

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
if [[ -z "$branch" ]]; then
  log "ERROR: not a git repo"
  exit 1
fi

if ! git pull --rebase "origin" "$branch" >>"$LOG" 2>&1; then
  log "WARN: git pull --rebase failed; will still try commit"
fi

git add -- "${CHANGED[@]}"
if ! git commit -m "chore(registry): sync from Feishu board watch [agent:coordinator]" >>"$LOG" 2>&1; then
  if [[ -z "$(git status --porcelain -- "${CHANGED[@]}" 2>/dev/null || true)" ]]; then
    log "nothing to commit after staging"
    exit 0
  fi
  log "WARN: git commit failed"
  exit 1
fi

if ! git push origin HEAD >>"$LOG" 2>&1; then
  log "WARN: git push failed (check credentials / remote); local commit kept"
  exit 1
fi

log "ok pushed on $branch"
exit 0
