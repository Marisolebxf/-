#!/usr/bin/env bash
# git-push-registry.sh — commit+push registry YAML + confirm 派单包 (soft-fail on push)
# Whitelist:
#   - agent-delivery/task-registry.yaml
#   - agent-delivery/bitable-inbound-proposals.yaml
#   - agent-delivery/registry-gap-proposals.yaml
#   - agent-delivery/pending-dispatch.yaml
#   - agent-delivery/agent-handoffs/**/*派单包.md  (changed/untracked only)
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
  "agent-delivery/registry-gap-proposals.yaml"
  "agent-delivery/pending-dispatch.yaml"
)

CHANGED=()
for p in "${PATHS[@]}"; do
  [[ -e "$p" ]] || continue
  if [[ -n "$(git status --porcelain -- "$p" 2>/dev/null || true)" ]]; then
    CHANGED+=("$p")
  fi
done

# confirm 生成的派单包：仅纳入有变更/未跟踪的 *派单包.md
while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  case "$line" in
    *派单包.md) ;;
    *) continue ;;
  esac
  path="${line:3}"
  path="${path#"${path%%[![:space:]]*}"}"
  path="${path%\"}"
  path="${path#\"}"
  if [[ "$path" == *" -> "* ]]; then
    path="${path##* -> }"
    path="${path%\"}"
    path="${path#\"}"
  fi
  [[ -z "$path" ]] && continue
  dup=0
  for c in "${CHANGED[@]+"${CHANGED[@]}"}"; do
    [[ "$c" == "$path" ]] && dup=1 && break
  done
  [[ "$dup" -eq 1 ]] && continue
  CHANGED+=("$path")
done < <(git status --porcelain -u -- 'agent-delivery/agent-handoffs/' 2>/dev/null || true)

if [[ ${#CHANGED[@]} -eq 0 ]]; then
  log "no registry/dispatch-package changes; skip commit/push"
  exit 0
fi

log "changes: ${CHANGED[*]}"

if [[ "$DRY" -eq 1 ]]; then
  log "[DRY] would commit+push registry (+ dispatch packages if any)"
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
has_pkg=0
for c in "${CHANGED[@]}"; do
  case "$c" in
    *派单包.md) has_pkg=1; break ;;
  esac
done
if [[ -n "${GKX_GIT_COMMIT_MSG:-}" ]]; then
  commit_msg="$GKX_GIT_COMMIT_MSG"
elif [[ "$has_pkg" -eq 1 ]]; then
  commit_msg="chore(dispatch): sync registry + 派单包 [agent:coordinator]"
else
  commit_msg="chore(registry): sync from Feishu board watch [agent:coordinator]"
fi
if ! git commit -m "$commit_msg" >>"$LOG" 2>&1; then
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
