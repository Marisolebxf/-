#!/usr/bin/env bash
# Cron 调度门控（Asia/Shanghai）
#   高峰 08:30–01:00（含）：每 15 分钟
#   其余时段：03:00 / 05:00 / 07:00（相对 01:00 每 2 小时；01:00 由高峰末班覆盖）
#
# 退出码：0 = 本次应执行 sync；1 = 跳过（Cron Job 仍视为成功）
set -euo pipefail

export TZ=Asia/Shanghai

h=$(date +%H)
m=$(date +%M)
h=$((10#$h))
m=$((10#$m))
hm=$((h * 60 + m))

in_peak_window() {
  if (( hm >= 510 && hm <= 1439 )); then
    return 0
  fi
  if (( h == 0 && m % 15 == 0 )); then
    return 0
  fi
  if (( h == 1 && m == 0 )); then
    return 0
  fi
  return 1
}

on_peak_15m_grid() {
  if (( h == 8 && m < 30 )); then
    return 1
  fi
  (( m % 15 == 0 ))
}

offpeak_should_run() {
  case "$h:$m" in
    3:0|5:0|7:0) return 0 ;;
    *) return 1 ;;
  esac
}

if in_peak_window && on_peak_15m_grid; then
  echo "[INFO] cron gate: peak → run (${h}:${m})"
  exit 0
fi

if ! in_peak_window && offpeak_should_run; then
  echo "[INFO] cron gate: off-peak 2h → run (${h}:${m})"
  exit 0
fi

echo "[INFO] cron gate: skip (${h}:${m})"
exit 1
