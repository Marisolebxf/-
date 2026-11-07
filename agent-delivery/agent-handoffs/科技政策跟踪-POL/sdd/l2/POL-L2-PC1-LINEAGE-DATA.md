# POL-L2-PC1-LINEAGE-DATA · 溯源索引构建 · 后台数据架构设计

- 任务：`POL-L2-PC1-LINEAGE-DATA` · 2026-11-08 · `agent:data-agent` · 监管：`human:淮政玮`
- SRS：**604** · 上游：LINEAGE-ARCH §5/§9

## 1. 表

仅 `gkxlumenx_gapfill.gapfill_policy_lineage_index`。不进 ODS/DWD/ADS/供应方库。

行两类：

| 类型 | 内容 | mock |
|---|---|---|
| 原文↔条款 | 从 `ads.policy_text_parse` 生成真实 policy_id/条款/摘录 | 否 |
| 条款↔结论 | 假想结论挂真实条款 | 是（`fill_method=manual`，UI 🧪） |

公共列：`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`；`metric_id` 留空。字段级 DDL 与灌数由 `POL-L2-PC1-LINEAGE-GAPFILL-L01` 执行（依赖本 DATA + ARCH）。

## 2. 消费边界

只被 `governance/lineage-index` 读。不与 `gapfill_policy_report_trace`（617）合并。查询不灌数。D4 保持 mock。
