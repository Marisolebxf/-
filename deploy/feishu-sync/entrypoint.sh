#!/usr/bin/env bash
set -euo pipefail

ROOT="/orch"
export ROOT
source "$ROOT/deploy/feishu-sync/setup-git-credentials.sh"

cd "$ROOT"

if [[ -d .git ]]; then
  BR="${GIT_BRANCH:-dev}"
  echo "[INFO] git pull --rebase origin ${BR}"
  git fetch origin "$BR" 2>/dev/null || true
  git pull --rebase origin "$BR" 2>/dev/null || echo "[WARN] git pull failed; using image copy"
fi

echo "[INFO] starting feishu-bitable-webhook-handler on :${FEISHU_BITABLE_WEBHOOK_PORT:-8787}"
exec node scripts/feishu-bitable-webhook-handler.mjs
