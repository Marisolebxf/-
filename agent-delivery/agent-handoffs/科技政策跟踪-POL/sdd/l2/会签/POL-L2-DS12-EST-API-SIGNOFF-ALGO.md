# POL-L2-DS12-EST-API-SIGNOFF-ALGO · 政策效果推演 · 效果预估 · 后台接口设计 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-EST-API.md`（2026-11-05。本页不改它）
- 对照：`POL-L2-DS12-EST-ARCH.md`（2026-11-04。2026-11-05 只改第 5.4、5.5 节的库.表写法，读法未改）、`POL-L2-DS12-EST-METRIC.md`（2026-11-05）。代码只读 `lumen-algo-py/vendor/entan-py` 的 `polan/text/simulate.py`、`polan/job.py`、`conf/cfg_model_registry.yaml` 的 `POLICY_SIMULATE`，以及 `lumen-svc-platform` 的 `PolicyAnalysisTypes.java`。指标身份取 `sdd/指标与501.md` §3.1 与 §3.2 的 232–236 行
- 监管：`human:淮政玮`
- 强度：ponytail off
- 范围：SRS 232–236。只读核对。不改分册，不改 Python 或 Java，不改模型注册表，不动 task-registry，不 commit

## 结论

同意会签。

## 核对

2026-11-05 本会话未调用指标 MCP。指标身份只取 `sdd/指标与501.md` §3。不读 seed YAML，不编 D1–D3。指标 MCP 不可用，不构成不同意。注册表与函数不一致只记观察，不要求本页改注册表。`指标与501.md` §3.2 仍把 232–236 的判定列写成 501、页面空态。接口分册的空态是无行则空、HTTP 成功。调研判定列仍写 501，不构成不同意。

`polan.text.simulate.run` 无参数。它只读 `ads.policy_intensity` 中 `scope_type=province` 且力度指数非空的行，取力度前 12 省。三条情景是扶持力度 +20%、扶持力度 +40%、覆盖面扩展。公式为 `simulated = baseline * (1 + boost * elasticity)`。写出基线、推演值、变化率、逐年曲线和一句解释，`TRUNCATE` 后写入 `ads.policy_simulate`。行上 `metric_id` 固定字面量 `M_POLICY_SIMULATE`。函数不收政策类型、覆盖范围、支持力度、实施时间，不写未出台仿真、新出台短长期效果、区域 GDP / 产业结构 / 就业率，不写 235 的维度得分，不写 236 的意见。

`PolicyAnalysisTypes.CANONICAL` 是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`、`policy_intensity`、`policy_focus_ads`、`policy_text_parse`、`policy_region_diff`。没有 `policy_simulate`。`polan.job.JOB_SUB_TYPES` 另含内部 `policy_shard`，同样没有 `policy_simulate`。`job.py` 不调用 `simulate.run`。

`指标与501.md` §3.2：232、233、234 都是已有 `M_POLICY_SIMULATE`，`algorithm_type`=`MODEL`，D4=`mock`，判定 501。233 写明与 232 共用，没有独立指标。234 写明空间模拟没有独立指标。235、236 的 `metric_id` 为未见，判定 501。235 写明不借用 `M_POLICY_DEEP_168_1`。§3.1：`M_POLICY_DEEP_171_1` 为 `MODEL`、D4=`mock`，跨项索引；`M_POLICY_LAYOUT_REC_COUNT` 为 `STAT`、D4=`mock`，跨项索引。二者是布局推荐键，不能当作推演结果。

| 序号 | 接口分册 | 架构稿 / 指标分册 | 判定 |
|---|---|---|---|
| 232 | 第 1、2、3、8 节：`simulation/jobs` 同步读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast` 未出台仿真行。行上 `metric_id` 用已有 `M_POLICY_SIMULATE`。不调用 `polan.text.simulate`，不读 `ads.policy_simulate`，不按弹性现算。不挂 `M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT`。无行则该次模拟空，HTTP 成功，不返回 501 | ARCH §5.1、§9 与 METRIC §5.1 同此。D4 仍是 mock | 同意 |
| 233 | 第 4 节：同一条 `jobs`，种类为新出台预测，同一张表。行上仍是 `M_POLICY_SIMULATE`，不新注册。不调 `parse/jobs`，不用解析结果顶替。无行则该区空，不返回 501 | ARCH §5.2 与 METRIC §5.2 同此 | 同意 |
| 234 | 第 5 节：种类为区域空间，同一张表。行上仍是 `M_POLICY_SIMULATE`。区域或类型对不上则空间结果空，不造全国通用行。不写 nGQL。不返回 501 | ARCH §5.3 与 METRIC §5.3 同此 | 同意 |
| 235 | 第 6 节：种类为多维评估。只读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的多维评估行。行上 `metric_id` 留空。不挂 `M_POLICY_SIMULATE`，不借用 `M_POLICY_DEEP_168_1`。无行则雷达和柱状空，不返回 501 | ARCH §5.4 与 METRIC §6.1 同此 | 同意 |
| 236 | 第 7 节：种类为利益攸关方。只读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` 的参与意见行。行上 `metric_id` 留空，不挂 `M_POLICY_SIMULATE`。请求不插入。无行则列表空，不返回 501 | ARCH §5.5 与 METRIC §6.2 同此 | 同意 |

五叶都不新造 `metric_id`。232–234 只挂已有 `M_POLICY_SIMULATE`。235–236 不挂该号。D4 保持 mock，不把 mock 写成已上线。接口分册第 9 节写明不调用 `polan.text.simulate`，不读 `ads.policy_simulate`，不把布局推荐键顶替推演，不用 501 充当这五叶的功能。第 8 节把架构第 2 节真推演未注册种类的 501 排除在这五叶之外。五叶不进 `PolicyAnalysisTypes`，不加 `policy_simulate`，不进 `POST /internal/policy/jobs/execute`。与代码事实相容：`run()` 只服务中台省级力度情景，填不出这五叶。

## 观察

不构成不同意，也不要求改注册表，也不要求改接口分册。

`POLICY_SIMULATE` 的 `metric_ids` 列了 `M_POLICY_SIMULATE` 和 `M_POLICY_DS_11_POLICY_EVAL_015`，`handler_module` 为 `polan.text.simulate`，`ads_table` 为 `ads.policy_simulate`，`ext.is_mock` 为 true。`run()` 只写 `M_POLICY_SIMULATE`。接口分册不调用该函数，不读这张表，不改注册表。指标分册第 3 节已记下同一事实。

架构第 5.5 节写表内种类为参与意见。接口分册第 1 节写明公开 kind 取「利益攸关方」，参与意见是行内容。读的仍是 `gapfill_policy_sim_stakeholder`，行上 `metric_id` 仍留空。算法路径不变。

236 对已灌行的计数，接口分册与指标分册都没有把它写成新 `metric_id`，也没有改挂成可接统计读面。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。不改接口分册，不改架构稿，不改指标分册，不改算法代码，不改模型注册表。
