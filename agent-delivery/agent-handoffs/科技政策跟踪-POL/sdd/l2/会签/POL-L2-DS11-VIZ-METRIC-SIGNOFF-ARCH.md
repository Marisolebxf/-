# POL-L2-DS11-VIZ-METRIC-SIGNOFF-ARCH · 政策分析评价 · 政策分析报告可视化呈现 · 指标分册架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-VIZ-METRIC`
- 监管：`human:淮政玮`
- 对照：已签收 `POL-L2-DS11-VIZ-ARCH`（2026-11-03 返工后第二轮四角色同意，注册表已签收）第 5、6 节挂接与点名排除；`sdd/指标与501.md` 219–222 行只作对照。本页只核分册是否落在架构基准内，不重新设计，不改分册，不改架构稿，不改 `指标与501.md`，不改指标 seed 与矩阵，不改 task-registry，不改代码
- 范围：SRS 序号 219–222

## 结论

同意会签

分册零注册、零改 D4、零手抄公式：219、220、222 维持无专属 `metric_id` 的 501 调研判定不改字，221 维持跨项索引不改档；读面全部落在架构定的两张缺项表加模板表与第 7 项已有子图上；不把 501 充当画面，有行读表无行则空。

## 核对

| 项 | 分册写法 | 对架构判定 |
|---|---|---|
| 不新注册指标 | 第 1 节表四行均「不新注册」；「本二级挂接 0 条已有 `metric_id`」；「这 4 叶之外，本二级不新造 `metric_id`」 | 一致。与架构「不新造 `metric_id`」逐句对上 |
| 不改 D4、不写假公式 | 第 3 节：不列八件套全表，「不手抄公式，也不另写一条能算出趋势、分区对照、关联或导出文件的式子」。第 4 节：不写 D1、D2、D3，不补 `aligned`/`partial`/`full`。第 8 节重申不把 mock 写成已上线 | 一致。未被查到的字段一律留空不补，符合注册表只读规约。头部声明未见 metric MCP、未读 seed 与矩阵 YAML，未改注册表 |
| 219/220/222 无专属 `metric_id` | 第 2 节表三行 `metric_id` 均为「（无）」「无专属指标，不改 D4」「不挂」。行上名称三条写明不是注册号：219 指标名、220 对象与投向、222 模板名都「不是 `metric_id`」「不登记成指标」 | 一致。与架构「不新造 `metric_id`，不改 D4，不改指标分册判定」一致，且与数据分册三张表 `metric_id` 留空互相咬合 |
| 221 跨项索引 | 「判定列跨项索引，本叶不改成 501，也不改成可接统计读面」「跨项只消费第 7 项已有子图。不建表」；不挂 `M_POLICY_GRAPH_107_1`（留全景 208）、`M_POLICY_RELATION_DEGREE`（留推演 240），两号 D4 都不改 | 一致。与架构 5.3 节一致，不新开资源、不建缺项表、不新造图指标 |
| 不把 501 充当画面 | 第 1 节三行均「无行则图空/模板空。不用 501 充当画面」；第 8 节「不把 501 当成四叶的画面。有行读表，无行则空。221 无子图则空」。501 判定留在 `指标与501.md` 不改字 | 一致。调研判定与迁移后读面分开表述，正是架构头部定下的口径 |
| 读面与架构一致 | 第 5 节：219 读 `gapfill_policy_eval_trend`、220 读 `gapfill_policy_eval_partition`、222 读 `gapfill_policy_eval_template`；219、220 走 `jobs` 一次一种类不建任务不进异步，222 走 `shells` 模板选用；浏览器只打 `/display/v1/policy/**` | 一致。参数名留给 API 分册，本叶不越界展开 |
| 点名排除与代码核对 | 第 7 节点名不挂：`M_POLICY_TIMESERIES`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT`、全景分布三号、`M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`、`M_POLICY_SIMULATE`、`policy_effect` 等白名单键、`counts`、223–231、`compare/report/benchmark`。第 5.4、5.5、5.6 节只读核对 `effect.py` 写 `ads.policy_effect` 与 `ads.policy_metric_timeseries`、`simulate.py` 写 `ads.policy_simulate`、`PolicyAnalysisTypes` 九键白名单无趋势/分区/导出键 | 一致。排除表与架构第 6 节逐行对应；代码核对只读不改，支撑「不挂、不改 D4、不加白名单键」的判定。`policy_timeseries`、`policy_regional` 不借给 219、220，`policy_focus_ads`、`policy_text_parse` 留给解读二级 |
| 不改上游、不越界 | 第 8 节：不改 `指标与501.md`、架构稿、`POL-L2-DS11-READ-METRIC.md`、说明书、PLAN、WBS、seed 与矩阵；不改 `effect.py`、`simulate.py`、`PolicyAnalysisTypes.java`；不写 OpenAPI；不执行灌数单 | 一致。身份字段未查到的均标明出处限制，不冒充 `metric-get` 返回 |

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。同意会签不是签收。
