---
name: gkx-metric-srs-export
description: >
  Regenerates the full 指标需求来源 Excel (registry catalog + SRS book/seq/name/brief).
  Use when the user says 导出指标需求来源, 带有需求来源的完整Excel,
  带需求来源的完整Excel, 指标需求来源表, or metric-srs-export.
  Calls MCP metric-registry tool metric-srs-export; does not write seed/matrix YAML.
---

# 指标需求来源（完整 Excel）

真源与 Cursor 同文：`.cursor/skills/gkx-metric-srs-export/SKILL.md`。改技能先改那边。

MCP：`metric-registry` → `metric-srs-export`。xlsx：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`。不写 registry YAML，不改飞书进度表列。
