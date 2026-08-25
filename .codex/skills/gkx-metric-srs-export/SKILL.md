---
name: gkx-metric-srs-export
description: >
  Regenerates the full 指标需求来源 Excel (registry catalog + SRS book/seq/name/brief
  + 展示系统/专题系统). Use when the user says 导出指标需求来源,
  带有需求来源的完整Excel, 指标需求来源表, 需求来源没有填全,
  来自专题还是展示, 来源系统, or metric-srs-export.
  Rebuilds metric-srs-map.yaml from A1/A2 first, then exports. Does not write seed/matrix YAML.
---

# 指标需求来源（完整 Excel）

真源与 Cursor 同文：`.cursor/skills/gkx-metric-srs-export/SKILL.md`。改技能先改那边。

MCP：`metric-registry` → `metric-srs-export`（先重建 sidecar 再导出）。xlsx：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`。

目录列 **来源系统**；明细列 **系统**（展示系统 / 专题系统 / 展示+专题 / 算法库）。`指标名` 后有 **决策清单中的编号**（客户决策清单 Q 号）。

后备：`node scripts/build-metric-srs-map.mjs`，再 `python agent-delivery/metrics/registry/export/export_metric_srs_board.py --json`。只跑 Python 不会更新 map。

对人报 `with_refs` / `without_refs` / `by_book` / `by_system`（展示系统 / 专题系统 / 展示+专题 / 算法库）。`by_system` 是明细行。空 = 未从 A1/A2 对上，不是无需求。不要手填 `srs_refs`。
