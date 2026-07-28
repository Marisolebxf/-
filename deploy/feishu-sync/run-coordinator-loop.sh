#!/usr/bin/env bash
# CronJob：Mayor 建议包（A3 · Path A light）
# 默认：git pull → coordinator-loop.mjs（不 apply-leases、不 confirm、不开 agent）
# 可选：COORDINATOR_LOOP_APPLY_LEASES=1 时回收过期 claimed 并 git-push-registry
set -euo pipefail

ROOT="/orch"
export ROOT
source "$ROOT/deploy/feishu-sync/setup-git-credentials.sh"

cd "$ROOT"

BR="${GIT_BRANCH:-dev}"
LIMIT="${COORDINATOR_LOOP_LIMIT:-8}"
APPLY="${COORDINATOR_LOOP_APPLY_LEASES:-0}"
SKIP_SCAN="${COORDINATOR_LOOP_SKIP_SCAN:-0}"
LOG_DIR="$ROOT/agent-delivery/_tmp"
LATEST="$LOG_DIR/coordinator-loop-latest.txt"
mkdir -p "$LOG_DIR"

if [[ -d .git ]]; then
  echo "[INFO] git pull --rebase origin ${BR}"
  git pull --rebase origin "$BR" || {
    echo "[ERROR] git pull failed; abort coordinator-loop"
    exit 1
  }
else
  echo "[WARN] no .git after setup; using image copy of /orch"
fi

ARGS=(scripts/coordinator-loop.mjs --limit "$LIMIT")
if [[ "$APPLY" == "1" || "$APPLY" == "true" || "$APPLY" == "yes" ]]; then
  ARGS+=(--apply-leases)
fi
if [[ "$SKIP_SCAN" == "1" || "$SKIP_SCAN" == "true" ]]; then
  ARGS+=(--skip-scan)
fi

echo "[INFO] node ${ARGS[*]}"
set +e
OUT="$(node "${ARGS[@]}" 2>&1)"
CODE=$?
set -e
printf '%s\n' "$OUT" | tee "$LATEST"
echo "[INFO] wrote $LATEST (ephemeral in Job pod; see kubectl logs)"

if [[ "$APPLY" == "1" || "$APPLY" == "true" || "$APPLY" == "yes" ]]; then
  echo "[INFO] git-push-registry after apply-leases"
  bash "$ROOT/scripts/lib/git-push-registry.sh" || echo "[WARN] git-push-registry failed"
fi

echo "[INFO] coordinator-loop done exit=$CODE"
# 建议包即使 soft/hard 告警也视为 Job 成功，避免 Cron 红灯；硬失败仅 node 崩
exit 0
