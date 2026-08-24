---
name: gkx-metric-lookup
description: >
  Look up a GKX metric's 8-piece identity kit and D1–D4 ingestion status.
  Use when the user asks for metric_id, 8件套, 口径, formula, algorithm_type,
  接入状态, D4, 就绪度, or MetricSpecCard fields. Read-only via metric-registry MCP.
---

# GKX 指标查询（8 件套 + 接入状态）

查某条指标的**身份**和**现在算不算得出**时，走 MCP `metric-registry`，不要打开 `metrics/registry/*.yaml`。

权威模型：`agent-delivery/data-lineage-policy.md`（D9）。上手：`agent-delivery/metric-mcp-usage-guide.md`。

## 何时用

用户或任务提到：`metric_id` / `M_ENT_*` / 8 件套 / 口径 / 公式 / `algorithm_type` / D1–D4 / 接入 / Mock / ⓘ 字段 / 「这条数哪来的」/ SRS / 需求来源。

只谈派单 WBS、A1/A2 表、谁做算法 → 去梳理全文，不是本 skill。只谈任务状态 → `gkx-task-registry`。导出整张「指标进度统计」Excel → `gkx-metric-progress`。导出带需求来源的完整 Excel → `gkx-metric-srs-export`。

## 怎么查

1. 已知 ID → `metric-get`（`metric_id`）。
2. 只知道中文名或域 → `metric-query`（`q` / `domain` / `d1` / `d4`），`limit` 默认 20。
3. 只要覆盖计数 → `metric-summary`。
4. MCP 未加载：提示重启 Cursor；可用 `node scripts/metric-mcp-selfcheck.mjs` 自检。仍不要整文件读 YAML。

## 怎么说结果

分三段，不要揉成一套字段：

- **8 件套（身份）** = `kit`：metric_id、中文名、definition、formula、**algorithm_type**、源表、源系统、更新频率、version。未填类型 = `UNKNOWN`。
- **接入状态** = `readiness`：D1 `d1_def_status` / D2 / D3 / D4。`lifecycle_stage` 可附带，但不是 8 件套。
- **需求来源** = `extras.srs_refs`：需规分册 `book`（02/04/05）+ `seq` + `name` + `brief`。空 = 未回填。`seq` 跨分册不可比。

看 `found.seed` / `found.matrix`：缺哪侧就说缺，不要用另一侧脑补。`aligned` 且 `D4=mock` 是合法组合。

## 禁止

- 直接读 registry YAML 当查询结果
- 把 D1–D4、lifecycle 或 `srs_refs` 说成 8 件套
- 用本 skill 改 seed / 矩阵（口径正式化走 data-agent）
- 把 `UNKNOWN` 说成已定类型或已对齐
