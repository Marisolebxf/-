---
name: gkx-metric-progress
description: >
  Regenerates the Feishu-format 指标与数据开发进度 Excel from metrics/registry.
  Use when the user says 指标进度统计, 重新执行一下指标进度统计,
  重新执行一下"指标进度统计", 导出指标进度, 同步指标进度表,
  or metric-progress-export. Calls MCP metric-registry tool metric-progress-export;
  does not write seed/matrix YAML.
---

# 指标进度统计（离线看板）

真源与 Cursor 同文：`.cursor/skills/gkx-metric-progress/SKILL.md`。改技能先改那边。

MCP：`metric-registry` → `metric-progress-export`。xlsx：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`。不写 registry YAML。
