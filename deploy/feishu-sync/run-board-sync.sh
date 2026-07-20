#!/usr/bin/env bash
# CronJob：纯 Node 看板 sync（inbound pull + outbound skip-kanban + git push + scan）
set -euo pipefail

ROOT="/orch"
export ROOT
source "$ROOT/deploy/feishu-sync/setup-git-credentials.sh"

cd "$ROOT"

if [[ -d .git ]]; then
  BR="${GIT_BRANCH:-dev}"
  git pull --rebase origin "$BR" || {
    echo "[ERROR] git pull failed; abort sync"
    exit 1
  }
fi

echo "[INFO] feishu-bitable-cron-sync (Node)"
exec node scripts/feishu-bitable-cron-sync.mjs
