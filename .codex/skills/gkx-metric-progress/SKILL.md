---
name: gkx-metric-progress
description: >
  Regenerates the Feishu-format 指标与数据开发进度 Excel from metrics/registry.
  Use when the user says 指标进度统计, 重新执行一下指标进度统计,
  重新执行一下"指标进度统计", 导出指标进度, 同步指标进度表,
  or metric-progress-export. Calls MCP metric-registry tool metric-progress-export;
  does not write seed/matrix YAML. Excel includes 域 (Chinese domain enum).
---

# 指标进度统计（离线看板）

真源与 Cursor 同文：`.cursor/skills/gkx-metric-progress/SKILL.md`。改技能先改那边。

MCP：`metric-registry` → `metric-progress-export`。xlsx：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`。不写 registry YAML。

表列：`指标名` 后有 **决策清单中的编号**（客户决策清单 Q 号；飞书进度表不加），再后是 **域**（中文枚举，不是 8 件套）；**模块** 列名不改；其后 **模块说明** 为中文。`lifecycle_stage` 离线列名 **语义层开发阶段**（飞书仍叫「填齐阶段」）。合同集合后有 **差集判定**（A2 mapped/missing/other_system/n/a_ops；飞书进度表不加）。合同集合：无 A2 挂接 = L−F，不要再报成未分拣。表头单元格带 Excel 批注。对人回报须含 `domain` 分桶（与 `algorithm_type` / `contract_set` / `overall` 并列）。枚举：`scripts/lib/metric-domain-enum.json`、`scripts/lib/metric-module-enum.json`。
