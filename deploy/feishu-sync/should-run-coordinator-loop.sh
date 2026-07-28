#!/usr/bin/env bash
# Mayor Cron 门控（Asia/Shanghai）
# 工作日感：08:00–20:00 整点每 2 小时跑一次（08/10/12/14/16/18/20）
# 退出码：0 = 应执行；1 = 跳过
set -euo pipefail

export TZ=Asia/Shanghai

h=$(date +%H)
m=$(date +%M)
h=$((10#$h))
m=$((10#$m))

# 仅整点触发（配合 schedule "0 * * * *"）
if (( m != 0 )); then
  echo "[INFO] coordinator-loop gate: skip (not hour mark ${h}:${m})"
  exit 1
fi

case "$h" in
  8|10|12|14|16|18|20)
    echo "[INFO] coordinator-loop gate: run (${h}:00)"
    exit 0
    ;;
  *)
    echo "[INFO] coordinator-loop gate: skip (${h}:00 outside 08–20 /2h)"
    exit 1
    ;;
esac
