#!/usr/bin/env bash
# coordinator-loop-watch.sh — 本机/投影机 Mayor 建议包（A3，与 *.ps1 对齐）
#
# Usage:
#   ./scripts/coordinator-loop-watch.sh
#   ./scripts/coordinator-loop-watch.sh --apply-leases
#   ./scripts/coordinator-loop-watch.sh --limit 10 --skip-scan
#   ./scripts/coordinator-loop-watch.sh --dry-run

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT/agent-delivery/_tmp"
LOG="$LOG_DIR/coordinator-loop-watch.log"
LATEST="$LOG_DIR/coordinator-loop-latest.txt"
mkdir -p "$LOG_DIR"

LIMIT=8
APPLY_LEASES=0
SKIP_SCAN=0
DRY=0
NO_PULL=0
NO_PUSH=0
JSON=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --limit) LIMIT="$2"; shift 2 ;;
    --apply-leases) APPLY_LEASES=1; shift ;;
    --skip-scan) SKIP_SCAN=1; shift ;;
    --dry-run) DRY=1; shift ;;
    --no-git-pull) NO_PULL=1; shift ;;
    --no-git-push) NO_PUSH=1; shift ;;
    --json) JSON=1; shift ;;
    -h|--help)
      sed -n '1,20p' "$0"
      exit 0
      ;;
    *) echo "Unknown: $1" >&2; exit 2 ;;
  esac
done

log() {
  local line="[$(date -Iseconds 2>/dev/null || date)] $*"
  echo "$line" | tee -a "$LOG"
}

cd "$ROOT"
log "coordinator-loop-watch start limit=$LIMIT applyLeases=$APPLY_LEASES dry=$DRY"

if [[ "$NO_PULL" -eq 0 ]]; then
  branch="$(git rev-parse --abbrev-ref HEAD)"
  log "git pull --rebase origin $branch"
  if [[ "$DRY" -eq 1 ]]; then
    log "[DRY] would git pull"
  else
    if [[ -n "$(git status --porcelain 2>/dev/null || true)" ]]; then
      git stash push -m "coordinator-loop-watch: auto-stash $(date -Iseconds 2>/dev/null || date)" || {
        log "ERROR: stash failed"; exit 1
      }
      STASHED=1
    else
      STASHED=0
    fi
    git fetch origin
    if ! git pull --rebase origin "$branch"; then
      log "ERROR: git pull failed"
      [[ "${STASHED:-0}" -eq 1 ]] && git stash pop || true
      exit 1
    fi
    [[ "${STASHED:-0}" -eq 1 ]] && git stash pop || true
  fi
fi

ARGS=(scripts/coordinator-loop.mjs --limit "$LIMIT")
[[ "$APPLY_LEASES" -eq 1 ]] && ARGS+=(--apply-leases)
[[ "$SKIP_SCAN" -eq 1 ]] && ARGS+=(--skip-scan)
[[ "$JSON" -eq 1 ]] && ARGS+=(--json)

if [[ "$DRY" -eq 1 ]]; then
  log "[DRY] would: node ${ARGS[*]}"
  log "coordinator-loop-watch ok (dry)"
  exit 0
fi

if ! command -v node >/dev/null 2>&1; then
  log "ERROR: node not found"
  exit 1
fi

log "run: node ${ARGS[*]}"
set +e
OUT="$(node "${ARGS[@]}" 2>&1)"
CODE=$?
set -e
printf '%s\n' "$OUT" > "$LATEST"
printf '%s\n' "$OUT" | while IFS= read -r line; do
  [[ -n "$line" ]] && log "loop: $line"
done

if [[ "$APPLY_LEASES" -eq 1 && "$NO_PUSH" -eq 0 ]]; then
  log "git-push-registry after --apply-leases"
  bash "$ROOT/scripts/lib/git-push-registry.sh" || log "WARN: git-push-registry failed"
fi

log "coordinator-loop-watch ok (exit=$CODE)"
exit 0
