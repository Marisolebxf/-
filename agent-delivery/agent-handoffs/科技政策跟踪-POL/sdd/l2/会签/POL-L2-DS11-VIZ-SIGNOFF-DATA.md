# POL-L2-DS11-VIZ-SIGNOFF-DATA · 政策分析评价 · 政策分析报告可视化呈现 · 数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-03
- 对象：`sdd/l2/POL-L2-DS11-VIZ-ARCH.md`
- 监管：`human:淮政玮`
- 对照：该稿第 5、9 节；`POL-L2-DS11-READ-ARCH` 第 8 节；`POL-L2-DS11-READ-SIGNOFF-DATA`
- 范围：SRS 219–222
- 结论：**同意**

本页只核对数据落点。不改架构正文，不改任务状态，不建表，不灌数，不定字段级 DDL。

## 表、读取方、灌数方

| 序号 | 表 | 读取方 | 灌数方 |
|---|---|---|---|
| 219 | 新建 `gkxlumenx_gapfill.gapfill_policy_eval_trend`。不写 ODS、DWD、ADS | `gkxlumen-element` 经 `POST /display/v1/policy/evaluation/jobs` 的趋势段只读。无行则图空 | `POL-L2-DS11-VIZ-GAPFILL-L01`（`data-agent`）。查询不灌数 |
| 220 | 新建 `gkxlumenx_gapfill.gapfill_policy_eval_partition`。不写 ODS、DWD、ADS。不另建第三张可视化表 | 同一条 `jobs` 的分区段，`gkxlumen-element` 只读。无行则图空 | 同一张灌数单 |
| 221 | 不建表。只消费第 7 项已有政策子图 | 展示只读该子图。无子图则空。Java 不写 nGQL | 无。不灌弦线矩阵、演示路径 |
| 222 | 已有 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。本叶不建 | `gkxlumen-element` 经 `GET /display/v1/policy/evaluation/shells` 只读模板选用行。无选用行则模板区空 | 无。`POL-L2-DS11-READ-GAPFILL-L01` 只灌 224、225 的解读条目和多媒体条目，不灌模板选用。本叶不把模板选用加进该灌数单 |

不新造 `metric_id`。不改 D4。导出的 PDF、Excel 不入库，操作日志不灌。

`POL-L2-DS11-VIZ-GAPFILL-L01` 本页不执行。字段级 DDL 留给 `POL-L2-DS11-VIZ-DATA`。签收仍由 human:淮政玮 做。
