# POL-L2-DS11-VIZ-SIGNOFF-ALGO · 政策分析评价 · 政策分析报告可视化呈现 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-VIZ-ARCH.md`（2026-11-03。本页不改它）
- 对照：`sdd/指标与501.md` 第 2 节序号 219–222。代码只读 `lumen-algo-py/vendor/entan-py/api/policy_routes.py` 的 `_MODEL_TABLE`，以及 `polan/eval/`
- 监管：`human:淮政玮`
- 范围：SRS 219–222。只读核对。不改已有文件，不改 Python 或 Java，不动 task-registry

## 结论

同意会签。

## 核对

2026-11-03 指标身份只取 `指标与501.md`。不读 seed YAML，不编 D1–D3。

`_MODEL_TABLE` 的键是 `focus`、`opportunity`、`intensity`、`effect`、`gap`、`layout`、`guide`、`guard`。没有趋势、分区、导出。`polan/eval/` 下是 `effect.py`、`gap.py`、`focus.py`、`opportunity.py`、`intensity.py`、`layout.py`、`focus_one.py`、`ds_composite.py`。没有趋势图模块，没有分区对比模块。

| 序号 | 指标分册 | 架构稿 | 代码 |
|---|---|---|---|
| 219 | 未见。判定 501。不借用 `M_POLICY_TIMESERIES` | 不改挂时序。不把 `M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT` 当成趋势图。读 `gapfill_policy_eval_trend`，无行则空 | 无趋势模型。`effect` 在表内，写的是效果分和落地实效 |
| 220 | 未见。判定 501。不挂全景分布类 STAT | 不挂。读 `gapfill_policy_eval_partition`，无行则空 | 无分区模型 |
| 221 | 未见。判定跨项索引。不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` | 只消费第 7 项已有子图。不把共词网络写成新算法，不新造图指标 | `eval` 无共词模块。关联度在 `focus.py`，架构不挂 |
| 222 | 未见。判定 501。无指标，无导出模型，与核增研报无关 | 读 `gapfill_policy_eval_shell` 的模板选用。不走 `report/jobs`，不走全景 `benchmark-report` | `_MODEL_TABLE` 无导出 |

效果评估的落点，用来和 219 分开，本页不改挂：

- `polan.eval.effect.run` 把 `M_POLICY_EFFECT_SCORE` 写在 `ads.policy_effect`，`scope_type=region_effect`。
- 同一函数把 `M_POLICY_IMPLEMENTATION_EFFECT` 写在 `ads.policy_metric_timeseries`。每个区域一行，`stat_date` 是运行当天。这是落地实效的快照，不是多维指标趋势图。
- 分册里 `M_POLICY_IMPLEMENTATION_EFFECT` 在全景序号 209，类型 MODEL，D4=`mock`。`M_POLICY_EFFECT_SCORE` 在评价页 KPI，需求来源在推演。`M_POLICY_TIMESERIES` 在全景序号 198、205、206，类型 STAT，D4=`mock`。三处都不在 219。
- 架构稿第 5.1 节把这两条都写成写入 `ads.policy_effect`。落地实效的行在 `policy_metric_timeseries`。两处都不挂 219，这个差别不改变会签结论。

全景分布类 STAT（件数、类型、级别、全国、深圳）在分册第 1 节。架构稿不挂到 220。

221 与全景序号 208 共用「只消费第 7 项子图」的索引：`E-E7-POLICY-M1-L02` 已完成，`GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog。208 挂 `M_POLICY_GRAPH_107_1`。221 不挂这条，也不挂 `M_POLICY_RELATION_DEGREE`。`focus.run` 把关联度留在焦点行上。共词网络没有已注册模型，架构稿不新写一个。

222 与全景序号 217 的对标报告、研报序号 614–618 分开。架构稿不把这两条改成评价页的导出。

缺项表与「无模型」并存：分册对 219、220、222 的 501 和无模型判定留在分册，架构稿不改字。迁移后查缺项表，无行则空，不在接口里写死曲线、矩阵或 PDF。缺项表的行是灌入的 mock，不是已注册算法。不新造 `metric_id`，不改 D4。221 仍是跨项索引。

未发现架构稿把上述模型改挂到 219–222，也未发现把缺项表写成真算法。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。
