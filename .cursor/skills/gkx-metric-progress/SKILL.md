---
name: gkx-metric-progress
description: >
  Regenerates the Feishu-format 指标与数据开发进度 Excel from metrics/registry.
  Use when the user says 指标进度统计, 重新执行一下指标进度统计,
  重新执行一下"指标进度统计", 导出指标进度, 同步指标进度表,
  or metric-progress-export. Calls MCP metric-registry tool metric-progress-export;
  does not write seed/matrix YAML. Not for single-metric 8件套 lookup (use gkx-metric-lookup)
  and not for Feishu API sync (quota-bound).
---

# 指标进度统计（离线看板）

把当前 `metrics/registry/` 投影成飞书「指标与数据开发进度」同列 Excel。飞书开放平台配额不够时用这张表。上手：`agent-delivery/metric-mcp-usage-guide.md` §3.4。Codex 指针：`.codex/skills/gkx-metric-progress/`。

## 何时用

用户说 **指标进度统计** / **重新执行一下「指标进度统计」** / 导出指标进度表。

不要用本 skill：查单条 8 件套 → `gkx-metric-lookup`；导出带需求来源的完整 Excel → `gkx-metric-srs-export`；改 seed/矩阵 → data-agent；推飞书 Bitable → `sync-feishu-metric-board.mjs`（本月配额可能已满）。

## 怎么跑

1. 调 MCP `metric-registry` → **`metric-progress-export`**（无参数）。
2. 面板若仍只有 3 个工具：提示 Reload Window 后再调。MCP 未加载时才用后备：

```powershell
python agent-delivery/metrics/registry/export/export_feishu_metric_board.py --json
```

3. 对人只报：`xlsx` 路径、`rows` / `assessed`、`domain` / `algorithm_type` / `contract_set` / `a2_verdict` / `overall`，以及 **源缺口** `source_gap_indexed` / `source_gap_fallback` / `source_gap_empty`（可按 `source_gap_by_domain` / `source_gap_by_algorithm_type` 分桶）。若 `xlsx_locked=true`：主文件正被 Excel 打开，已写时间戳副本，请关掉后再跑一次以覆盖主文件。
4. 表列：`指标名` 后有 **决策清单中的编号**（`客户决策清单跟踪表.md` 的 Q 号；空=未点名；GAP-* 不进本列），再后是 **域**（中文枚举）。**模块** 列名不改（矩阵代码）；其后 **模块说明** 为中文（`scripts/lib/metric-module-enum.json`）。`lifecycle_stage` 离线列名 **语义层开发阶段**（飞书仍叫「填齐阶段」，已有列不改名）。**合同集合** 后有 **差集判定**（A2 原文分档按 metric_id 聚合；飞书进度表不加）。**源缺口** 优先 sidecar `question/source-gap-index.yaml`（单元格 `[{as_of}] {summary}`）；无 sidecar 回落矩阵 `d3_gap`。表头批注写明 sidecar 优先。域 / 模块说明 / 语义层开发阶段 / 差集判定 / 决策清单编号 / 源缺口概要都不是 8 件套。
5. **合同集合**：A2 `mapped`→F∩L；A2 `missing`（已有正式 `M_*`）→F−L；注册表有、A2 未挂→**L−F**；`other_system` / `n/a_ops` / `third_party`→未分拣。细档看「差集判定」。禁止把 L−F 再标成未分拣。
6. **禁止**整文件读 `cfg_metric-*-seed.yaml` / `metric-readiness-matrix-*.yaml`。
7. 未点名 `commit` / `push` 不要提交。xlsx 只覆写 `registry/export/`，不回写 YAML。飞书 Bitable **不加**「模块说明」列（配额）。
