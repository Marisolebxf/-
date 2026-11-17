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

仍只读已有 `gkxlumenx_gapfill.gapfill_policy_lineage_index`。只被 `governance/lineage-index` 读这一行已返回的列。不与 `gapfill_policy_report_trace`（617）合并，不读该表。查询不灌数。D4 保持 mock。不新增列。

界面格对照该行已有列（会签 `604-LINEAGE-FDE-C-异议闭合`「同一收法」，D-C1、D-C2 已采纳）：

| 界面格 | 已有列 | 空的时候 |
|---|---|---|
| 政策原文 | `policy_title` | 行上有标题就写标题 |
| 条款内容 | `clause_no`、`clause_excerpt` | 两列按已签收表都有值 |
| 分析结论 | `conclusion_title`、`conclusion_text` | 空就留空，不造句 |
| 查证标识 | `conclusion_key` | 空则界面写「这条还没有洞察标识」，不写 0 |

`link_kind=原文条款` 的 `conclusion_title`、`conclusion_text`、`conclusion_key` 为空就留空。不从邻行拼，不从 `gapfill_policy_report_trace` 拼。路径「原文 → 条款 → 结论」用上面三格拼接，不另设列。

溯源、查证、复核三个按钮不是表列，仍在每一行，含 `link_kind=原文条款` 的行。

## 变更记录

2026-11-16 · `POL-L2-PC1-LINEAGE-FDE-L01` 波次 C：按会签「同一收法」与 D-C1、D-C2 回写 §2。仍只读已有索引表；界面格对照已有六列；原文条款行结论三列空则留空；三个按钮不是表列、仍在每一行。不新增列，不新建表。
