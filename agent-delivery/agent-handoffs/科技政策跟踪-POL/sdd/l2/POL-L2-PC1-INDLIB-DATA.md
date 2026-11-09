# POL-L2-PC1-INDLIB-DATA · 规划指标库搭建 · 后台数据架构设计

- 任务：`POL-L2-PC1-INDLIB-DATA` · 2026-11-08 · `agent:data-agent` · 监管：`human:淮政玮`
- SRS：**605** · 上游：INDLIB-ARCH

## 1. 表

仅 `gkxlumenx_gapfill.gapfill_policy_indicator_lib`。全部行 mock（四维在源上无结构化真值）。维度闭集：扶持力度、适用范围、实施时效、申请条件。

列要点：政策 id、维度、口径说明、条目值/描述、`gap_item`、`fill_method=manual`、`gapfill_batch_id`、`generated_at`；`metric_id` 留空。DDL+灌数：`POL-L2-PC1-INDLIB-GAPFILL-L01`。

## 2. 边界

不写 ODS/DWD/ADS；不把 `policy_support` 字面 null 抬升为真值；不与注册指标表合并。查询不灌数。D4 保持 mock。
