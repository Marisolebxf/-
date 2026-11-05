# POL-L2-DS12-EST-DATA-SIGNOFF-ALGO · 政策效果推演 · 效果预估 · 数据落点 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-EST-DATA.md`（2026-11-05。本页不改它）
- 对照：`lumen-algo-py/vendor/entan-py` 的 `polan/text/simulate.py`、`polan/text/parse.py`、`polan/job.py`、`conf/cfg_model_registry.yaml` 的 `POLICY_SIMULATE`；`PolicyAnalysisTypes.java` 白名单。读法对照 `POL-L2-DS12-EST-ARCH.md` 第 5.1–5.3 节与第 9 节，指标对照 `POL-L2-DS12-EST-METRIC.md`。判定引自 `sdd/指标与501.md` §3.1 分键与 §3.2 的 232–234
- 监管：`human:淮政玮`
- 强度：ponytail off
- 范围：SRS 232–234。`gapfill_policy_sim_forecast` 行上的指标身份、D4 与读表边界。只读核对。不改分册，不改 Python 或 Java，不改模型注册表，不动 task-registry

## 结论

同意会签。

## 核对

2026-11-05 指标身份只取 `指标与501.md` §3。不读 seed YAML，不编 D1–D3。注册表与函数不一致只记观察，不要求本页改注册表。

`polan.text.simulate.run` 只读 `ads.policy_intensity` 中 `scope_type=province` 且力度指数非空的行，取力度前 12 省。三条情景按 `simulated = baseline * (1 + boost * elasticity)` 写出基线、推演值、变化率和逐年曲线，`TRUNCATE` 后写入 `ads.policy_simulate`。行上 `metric_id` 固定为字面量 `M_POLICY_SIMULATE`。函数不写 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`，不收政策类型、覆盖范围、支持力度、实施时间，不写新出台短长期效果，不写区域 GDP、产业结构、就业率。

`polan.text.parse.run` 从 `dwd.policy_base_info` 做规则截取，写出标题、摘要、结构化要素和自动标签，`TRUNCATE` 后写入 `ads.policy_text_parse`。每一行的 `metric_id` 固定为字面量 `M_POLICY_TEXT_PARSE`。函数不写 `M_POLICY_SIMULATE`，也不写未出台仿真、新出台预测或区域空间行。

`PolicyAnalysisTypes` 的规范键是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`、`policy_intensity`、`policy_focus_ads`、`policy_text_parse`、`policy_region_diff`。没有 `policy_simulate`。`polan.job.JOB_SUB_TYPES` 另含内部 `policy_shard`，同样没有 `policy_simulate`。数据分册不把 `simulate.run` 或 `parse.run` 加进该白名单。

`cfg_model_registry.yaml` 的 `POLICY_SIMULATE` 把 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015` 列在同一 `metric_ids` 下，`handler_module` 为 `polan.text.simulate`，`ads_table` 为 `ads.policy_simulate`，`ext.is_mock` 为 true。`run()` 只写前一个号，且只写入 `ads.policy_simulate`。`指标与501` §3.1 与 232–234 行把 `M_POLICY_SIMULATE` 写成 MODEL、D4=`mock`、判定 501。推演页可接统计读面为 0。

| 序号 | 数据分册 | 代码 | 判定 |
|---|---|---|---|
| 232 | `gapfill_policy_sim_forecast` 的 `row_kind=未出台仿真`。行上 `metric_id` 固定已有 `M_POLICY_SIMULATE`，不写空，不写别的号。不另设 baseline、simulated、delta 数值列。请求内不调用 `polan.text.simulate.run`，不按弹性公式现算。`is_mock=1`。D4 仍是 mock | `simulate.run` 只写 `ads.policy_simulate` 的省级力度情景，不写这张缺项表，也不收四类参数 | 同意 |
| 233 | 同表 `row_kind=新出台预测`。行上 `metric_id` 仍是已有 `M_POLICY_SIMULATE`。不把 `M_POLICY_TEXT_PARSE` 写进行上。`similar_basis_text` 是已灌入的一句依据，不存放解析标题、摘要、标签或条款。不读 `ads.policy_text_parse`，不用解析结果顶替预测行。`is_mock=1` | `parse.run` 只写 `ads.policy_text_parse`，行上只有 `M_POLICY_TEXT_PARSE`。`simulate.run` 不写短长期效果 | 同意 |
| 234 | 同表 `row_kind=区域空间`。行上 `metric_id` 仍是已有 `M_POLICY_SIMULATE`。不把 GDP、产业结构、就业率改挂别的指标。不造全国兜底行。`is_mock=1` | `simulate.run` 不写区域空间 | 同意 |

三种 forecast 行的 `metric_id` 都固定为已有 `M_POLICY_SIMULATE`。不新造第二条、第三条推演指标，也不把 `M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_INTENSITY_SCORE`、`M_POLICY_TEXT_PARSE`、`M_POLICY_DS_11_POLICY_EVAL_015` 写入本表。D4 保持 mock，不升 live。`is_mock=1` 只用来避免把缺项行读成已上线，不把这些行写成已上线，也不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。

第 1、2、7、8 节写明三类预测不读已有 ADS，不读已经落库的推演结果。`ads.policy_simulate` 继续只服务中台读面，行不复制进 `gapfill_policy_sim_forecast`。解析行不进入本表。235、236 的列不在本表展开，本表也不放那两类行。

观察（不构成不同意，也不要求改注册表或改分册）：

- 架构稿第 1.4 节把中台行的 baseline、simulated、delta、曲线和一句解释采纳为缺项行的内容范式，字段名归本数据分册。分册把预测值与变化率、逐年趋势、一句解释写进文字列，不把 `ads.policy_simulate` 的列原样拷进 forecast 行，也不迁三条固定情景和弹性公式。这与不读 `ads.policy_simulate` 一致。
- 模型注册表把 `M_POLICY_DS_11_POLICY_EVAL_015` 与 `M_POLICY_SIMULATE` 并列。`simulate.run` 只写后者。015 留在评价页 229。本数据分册不把 015 写进 forecast 行，不改注册表。
- `parse.run` 的标题、摘要、结构化要素和自动标签只落在 `ads.policy_text_parse`。本数据分册的 `similar_basis_text` 不是这些字段的拷贝。

未发现 forecast 行改用新 `metric_id`。未发现把 D4 改出 mock。未发现把 `is_mock=1` 的行写成已上线。未发现读 `ads.policy_simulate` 或把解析结果拷进预测行。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。不改数据分册，不改架构稿，不改指标分册，不改算法代码，不改模型注册表。
