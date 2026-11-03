# POL-L2-DS11-VIZ-METRIC 会签 · algorithm-agent

- 任务：`POL-L2-DS11-VIZ-METRIC`
- 角色：agent:algorithm-agent（监管 human:淮政玮）
- 日期：2026-11-03
- 结论：**同意会签**

## 核对表（算法角色重点）

| # | 核对项 | 结果 | 证据 |
|---|---|---|---|
| 1 | 219/220/222 不新造 metric_id | ✅ | 第 1、2 节：本二级挂接 0 条已有 `metric_id`；第 8 节「不新注册指标」。与 `指标与501.md` 评价表 219–222 行「未见 metric_id」一致 |
| 2 | 不改挂 `M_POLICY_TIMESERIES` | ✅ | 第 5.1、7 节：全景时序不改挂到 219。该号在 `policy_routes.py` 的 `_STAT_ORDER` 中是正式 STAT 读法（`ORDER BY period_key`），分册未把它借进缺项表 |
| 3 | 不改挂 `M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT` | ✅ | 第 5.4 节只读核对 `polan/eval/effect.py` 的 `run()`：前者删插 `ads.policy_effect`（`scope_type='region_effect'`），后者删插 `ads.policy_metric_timeseries`。分册写明两处写入都不挂本叶、不调用 `effect.run`、不改删除范围。代码事实与分册转述逐点一致 |
| 4 | 不改挂全景分布（`M_POLICY_NATIONAL_DIST` / `M_POLICY_TYPE_DIST` / `M_POLICY_LEVEL_DIST`） | ✅ | 第 5.2、7 节：留在全景，不改挂 220，不改它们的 D4。三号在 `policy_routes.py` `_STAT_ORDER` 中确为已有 STAT 读法 |
| 5 | 不改挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` | ✅ | 第 6 节：221 跨项只消费第 7 项已有子图，两号 D4（mock）只转述不改；不为此新读图、不调 `focus.run` 取关联度 |
| 6 | 行上名称（指标名/投向/模板名）不是 metric_id | ✅ | 第 2 节明确三条：219 的评估指标名只来自 `gapfill_policy_eval_trend` 行；220 的对象和投向只来自 `gapfill_policy_eval_partition` 行；222 的模板名只来自 `gapfill_policy_eval_template` 选用行。均「不是新的 metric_id」，不登记成指标 |
| 7 | 不改 D4 | ✅ | 第 4 节：无专属 `metric_id` 即无可改的 D4；被排除号的 D4 只转述 `指标与501` 已有行（`M_POLICY_EFFECT_SCORE` MODEL/mock、`M_POLICY_IMPLEMENTATION_EFFECT` MODEL/mock、`M_POLICY_GRAPH_107_1` GRAPH/mock、`M_POLICY_RELATION_DEGREE` GRAPH/mock 等），不升 live |
| 8 | 未经 metric MCP 不补身份字段 | ✅ | 第 2–4 节：头部声明未见 metric MCP、未读 seed/矩阵；不填中文名、口径、公式、源表、D1–D3、`srs_refs` |
| 9 | `simulate.run` 不调用；白名单不动 | ✅ | 第 5.5、5.6 节：`M_POLICY_SIMULATE` 留在推演 232/233；`PolicyAnalysisTypes` 九键 + 别名核对无误，趋势/分区/导出不进白名单，不增删任何键 |

## 算法侧补充说明

- `effect.py` 的 `ext` 上 `is_mock: True`、`pending: QPOL-02` 原样保留在代码里，分册明确「本叶不闭合 QPOL-02，不把 is_mock 改成已上线」，与 D17/D16 口径一致。
- 219/220/222 判定列保持 501、221 保持跨项索引，分册只改读法（查缺项表）不改判定文字，未把「无模型」虚构成已有模型——对照 `_MODEL_TABLE` 八键与 `polan/eval/` 目录（focus/effect/gap/intensity/layout/opportunity/ds_composite/focus_one）确无趋势、分区、导出模型，转述属实。

本页不把任务标 done，签收仍由 human:淮政玮 做。
