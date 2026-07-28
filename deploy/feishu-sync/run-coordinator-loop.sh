#!/usr/bin/env bash
# CronJob：Mayor 建议包 + 派单门控（A3 · Path A light）
# 默认：git pull → coordinator-loop --propose-dispatch（IM 淮政玮）→ git-push-registry
# 不自动 confirm / 不开 agent；confirm 由飞书「派单门控=已确认」webhook 完成
# 可选：COORDINATOR_LOOP_APPLY_LEASES=1 时回收过期 claimed
# 可选：COORDINATOR_LOOP_PROPOSE_DISPATCH=0 关掉门控/IM；COORDINATOR_LOOP_NO_NOTIFY=1 只写门控不发 IM
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
# 默认开启：pending + 派单门控待确认 + IM 通知淮政玮（可用 env 关掉）
PROPOSE="${COORDINATOR_LOOP_PROPOSE_DISPATCH:-1}"
if [[ "$PROPOSE" == "1" || "$PROPOSE" == "true" || "$PROPOSE" == "yes" ]]; then
  ARGS+=(--propose-dispatch)
fi
if [[ "${COORDINATOR_LOOP_NO_NOTIFY:-0}" == "1" ]]; then
  ARGS+=(--no-notify)
fi

echo "[INFO] node ${ARGS[*]}"
set +e
OUT="$(node "${ARGS[@]}" 2>&1)"
CODE=$?
set -e
printf '%s\n' "$OUT" | tee "$LATEST"
echo "[INFO] wrote $LATEST (ephemeral in Job pod; see kubectl logs)"

# propose-dispatch 会改 pending-dispatch.yaml；apply-leases 会改 task-registry
NEED_PUSH=0
if [[ "$APPLY" == "1" || "$APPLY" == "true" || "$APPLY" == "yes" ]]; then
  NEED_PUSH=1
fi
if [[ "$PROPOSE" == "1" || "$PROPOSE" == "true" || "$PROPOSE" == "yes" ]]; then
  NEED_PUSH=1
fi
if [[ "$NEED_PUSH" -eq 1 ]]; then
  echo "[INFO] git-push-registry after mayor loop (pending / leases)"
  if [[ "$PROPOSE" == "1" || "$PROPOSE" == "true" || "$PROPOSE" == "yes" ]]; then
    export GKX_GIT_COMMIT_MSG="chore(dispatch): mayor-loop propose 派单门控待确认 [agent:coordinator]"
  fi
  bash "$ROOT/scripts/lib/git-push-registry.sh" || echo "[WARN] git-push-registry failed"
fi

echo "[INFO] coordinator-loop done exit=$CODE"
# 建议包即使 soft/hard 告警也视为 Job 成功，避免 Cron 红灯；硬失败仅 node 崩
exit 0
