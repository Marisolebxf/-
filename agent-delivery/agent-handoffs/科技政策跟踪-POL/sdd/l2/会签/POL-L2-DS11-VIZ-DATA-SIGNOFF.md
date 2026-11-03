# POL-L2-DS11-VIZ-DATA-SIGNOFF · 政策分析评价 · 政策分析报告可视化呈现 · 数据分册会签

- 角色：`agent:data-agent`
- 日期：2026-11-03
- 对象：`sdd/l2/POL-L2-DS11-VIZ-DATA.md`，交接 `POL-L2-DS11-VIZ-DATA.md`
- 监管：`human:淮政玮`
- 对照：已签收的 `sdd/l2/POL-L2-DS11-VIZ-ARCH.md` 第 9 节
- 本页不改分册正文，不建表，不灌数

## 结论

同意

## 核对

| 项 | 分册 | 判定 |
|---|---|---|
| 新建 | 只新建 `gkxlumenx_gapfill.gapfill_policy_eval_trend` 与 `gapfill_policy_eval_partition`。灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01` | 一致 |
| 219 | 拣行键 `switch_dim` + `metric_name`。读取方 `gkxlumen-element`。无行则空 | 一致 |
| 220 | 拣行键 `object_kind`。投向有值时再按 `resource_direction`。无行则空 | 一致 |
| 221 | 不建表。只消费第 7 项已有子图。不写 nGQL | 一致 |
| 222 | 不建表。不把模板选用加进 `POL-L2-DS11-READ-GAPFILL-L01`。无选用行则空 | 一致 |

不写 ODS、DWD、ADS。不改 D4，不新造 `metric_id`。

阻断句：无。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。
