---
name: gkx-metric-srs-export
description: >
  Regenerates the full 指标需求来源 Excel (registry catalog + SRS book/seq/name/brief).
  Use when the user says 导出指标需求来源, 带有需求来源的完整Excel,
  带需求来源的完整Excel, 指标需求来源表, 需求来源完整表, 需求来源Excel,
  or metric-srs-export. Calls MCP metric-registry tool metric-srs-export;
  does not write seed/matrix YAML and does not change Feishu progress columns.
  Not for single-metric 8件套 lookup (use gkx-metric-lookup) and not for
  指标进度统计 (use gkx-metric-progress).
---

# 指标需求来源（完整 Excel）

把当前 `metrics/registry/` 全量投影成带 **SRS 需求来源** 的 Excel。与飞书「指标与数据开发进度」**分文件**，禁止往进度表加列。上手：`agent-delivery/metric-mcp-usage-guide.md` §3.5。Codex 指针：`.codex/skills/gkx-metric-srs-export/`。

产物：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`（汇总 / 指标目录 / 需求来源明细）。

## 何时用

用户说 **导出指标需求来源** / **带有需求来源的完整 Excel** / **指标需求来源表** / `metric-srs-export`。

不要用本 skill：查单条 8 件套或单条 SRS → `gkx-metric-lookup`；导出飞书同列进度表 → `gkx-metric-progress`；改 seed/矩阵 → data-agent；重新生成 sidecar → `node scripts/build-metric-srs-map.mjs`（本 skill 只导出，不重建 map）。

## 怎么跑

1. 调 MCP `metric-registry` → **`metric-srs-export`**（无参数）。
2. 面板若仍只有 4 个工具：提示 Reload Window 后再调。MCP 未加载时才用后备：

```powershell
python agent-delivery/metrics/registry/export/export_metric_srs_board.py --json
```

3. 对人只报：`xlsx` 路径、`catalog_rows` / `with_refs` / `without_refs`、`by_book`。若 `xlsx_locked=true`：主文件正被 Excel 打开，已写时间戳副本，请关掉后再跑一次以覆盖主文件。
4. **空来源 = 尚未从 A1/A2 回填，不是「无需求」。** `seq` 只在分册内唯一（02 的 97 ≠ 05 的 97）。
5. **禁止**整文件读 `cfg_metric-*-seed.yaml` / `metric-readiness-matrix-*.yaml` / `metric-srs-map.yaml` 来回答单条口径。
6. 未点名 `commit` / `push` 不要提交。xlsx 只覆写 `registry/export/`，不回写 YAML。
