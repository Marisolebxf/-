# POL-L2-DS12-EST-SIGNOFF-ALGO · 政策效果推演 · 效果预估 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-EST-ARCH.md`（2026-11-04。本页不改它）
- 对照：`lumen-algo-py/vendor/entan-py` 的 `polan/text/simulate.py`、`polan/text/parse.py`、`polan/eval/layout.py`、`polan/eval/effect.py`、`polan/job.py`、`api/policy_routes.py`、`conf/cfg_model_registry.yaml` 的 `POLICY_SIMULATE`、`POLICY_TEXT_PARSE`、`POLICY_LAYOUT`、`POLICY_EFFECT`；`lumen-svc-platform` 的 `PolicyAnalysisTypes.java` 白名单。指标身份取 `sdd/指标与501.md` §3。中台签对照 `demo-ui-system-test` 的 `TextAnalysis.vue` 与 `src/api/policy/index.ts`
- 监管：`human:淮政玮`
- 强度：ponytail off
- 范围：SRS 232–236。只读核对。不改架构稿，不改 Python 或 Java，不改模型注册表，不动 task-registry

## 结论

同意会签。

## 核对

2026-11-05 本会话没有挂上 `metric-registry`。`GetDynamicTools` 未见该命名空间，`metric-get` 未调用。指标身份只取 `sdd/指标与501.md` §3。不读 seed YAML，不读就绪度矩阵，不编 D1–D3。注册表与函数不一致只记观察，不要求本页改注册表。`指标与501.md` §3.2 与 §8 仍把 232–236 写成 501、页面空态；按本会签口径，调研仍写 501 不构成不同意。

`polan.text.simulate.run` 只读 `ads.policy_intensity` 中 `scope_type=province` 且力度指数非空的行，取力度前 12 省。三条情景是扶持力度 +20%、扶持力度 +40%、覆盖面扩展。公式为 `simulated = baseline * (1 + boost * elasticity)`。写出基线、推演值、变化率、逐年曲线和一句解释，`TRUNCATE` 后写入 `ads.policy_simulate`。行上 `metric_id` 固定为 `M_POLICY_SIMULATE`。函数不收需规四类参数，不写未出台仿真、新出台短长期效果、区域 GDP / 产业结构 / 就业率，也不写 `M_POLICY_DS_11_POLICY_EVAL_015`。

`GET /v1/policy/simulate` 在 `policy_routes.py`，按 `scope_code` / `scenario_id` 读 `ads.policy_simulate`。`demo-ui-system-test` 的 `fetchSimulate` 打 `/policy/simulate`，`TextAnalysis.vue` 用返回行画曲线。`lumen-svc-platform` 内未见 `policy_simulate`、`simulation/jobs`、`M_POLICY_SIMULATE`。

`PolicyAnalysisTypes` 的规范键是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`、`policy_intensity`、`policy_focus_ads`、`policy_text_parse`、`policy_region_diff`。没有 `policy_simulate`。`polan.job.JOB_SUB_TYPES` 另含内部 `policy_shard`，同样没有 `policy_simulate`。`job.py` 不调用 `simulate.run`。

`parse.run` 把 `M_POLICY_TEXT_PARSE` 写入 `ads.policy_text_parse`。`layout.run` 把 `M_POLICY_LAYOUT_REC_COUNT` 写入 `ads.policy_effect`（`scope_type=region_layout`）。`effect.run` 把 `M_POLICY_EFFECT_SCORE` 写入 `scope_type=region_effect`，把 `M_POLICY_IMPLEMENTATION_EFFECT` 写入时序行。`effect.run` 不写 `M_POLICY_DEEP_168_1`。

| 序号 | metric_id | 代码 | 架构稿 |
|---|---|---|---|
| 232 | `M_POLICY_SIMULATE`。`algorithm_type`=`MODEL`。D4=`mock`。判定 501 | `simulate.run` 只写省级力度情景。没有未出台四类参数仿真函数 | 第 5.1 节、第 9 节：行上沿用 `M_POLICY_SIMULATE`。读 `gapfill_policy_sim_forecast` 未出台仿真行。不新造指标，不改 D4。不调用 `simulate.run`，不按弹性公式现算，不加进 `PolicyAnalysisTypes` |
| 233 | 同上，与 232 共用，没有独立指标。判定 501 | `parse.run` 只写解析行，不写短长期效果。`policy_text_parse` 已在白名单，本叶不走它 | 第 4 节、第 5.2 节、第 6 节：同一张表的新出台预测行，行上仍是 `M_POLICY_SIMULATE`。不调 `parse/jobs`，不调 `policy_text_parse`，不用解析结果顶替 |
| 234 | 同上。空间模拟没有独立指标。判定 501 | 无区域经济空间模拟函数。`simulate.run` 的范围只有省 | 第 5.3 节：同一张表的区域空间行，行上仍是 `M_POLICY_SIMULATE`。服务端回行。不造全国通用行 |
| 235 | 未见。判定 501。写明不借用 `M_POLICY_DEEP_168_1` | `effect.run` 写的是 `M_POLICY_EFFECT_SCORE`，不是 168，也不是经济 / 社会 / 环境 / 创新四维评估行 | 第 5.4 节：读 `gapfill_policy_sim_result` 多维评估行。`metric_id` 留空。不借 168，不借 `M_POLICY_SIMULATE` |
| 236 | 未见。判定 501。关键词「利益」为 0 条 | 无意见采集函数，无意见指标 | 第 5.5 节、第 6 节：读 `gapfill_policy_sim_stakeholder` 参与意见行。`metric_id` 留空，不新造。不挂 `M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT`。请求不插入 |

`指标与501.md` §3.1：`M_POLICY_DEEP_171_1` 为 `MODEL`、D4=`mock`，跨项索引；`M_POLICY_LAYOUT_REC_COUNT` 为 `STAT`、D4=`mock`，跨项索引。二者是布局推荐键。§3.2 的 237 才挂 `M_POLICY_TEXT_PARSE`（`MODEL`，D4=`mock`，判定 501）。233 不借用该号。

架构稿第 1.4 节、第 2 节、第 6 节、第 7 节、第 8 节把 `polan.text.simulate.run`、`ads.policy_simulate`、`/v1/policy/simulate` 留在算法中台。展示预估走 `gkxlumen-display` 的 `simulation/jobs`，由 `gkxlumen-element` 只读缺项表。本叶不进 `PolicyAnalysisTypes`，不进 `JOB_SUB_TYPES`，不进 async-service。缺项行可以沿用基线、推演值、变化率、曲线、一句解释这种内容形态，字段归 DATA 单；这不是把 `run()` 迁进展示请求。弹性系数和中台三条固定情景不迁。

## 观察

不构成不同意，也不要求改注册表。

`POLICY_SIMULATE` 的 `metric_ids` 列了 `M_POLICY_SIMULATE` 和 `M_POLICY_DS_11_POLICY_EVAL_015`，`handler_module` 为 `polan.text.simulate`，`ads_table` 为 `ads.policy_simulate`，`invoke_path` 写着 `/internal/analysis/policy/simulate`。`run()` 只写 `M_POLICY_SIMULATE`。本次在 `lumen-algo-py` 的 Python 路由里未见该 `invoke_path` 的处理函数。架构稿第 1.1 节已记下 015 与函数不符，第 7 节写明不改模型注册表，本叶也不调用该函数。

`POLICY_TEXT_PARSE` 另列 `M_POLICY_DS_11_POLICY_EVAL_012`，`parse.run` 写入的行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。本叶不走这条通道。

`POLICY_LAYOUT` 只挂 `M_POLICY_LAYOUT_REC_COUNT`。`M_POLICY_DEEP_171_1` 在 `polan/metrics/catalog.py` 中有条目，中文名是政策布局推荐模型，不在 `POLICY_LAYOUT` 的 `metric_ids` 里。`POLICY_EFFECT` 挂 `M_POLICY_EFFECT_SCORE` 与 `M_POLICY_IMPLEMENTATION_EFFECT`。`M_POLICY_DEEP_168_1` 在同一目录的代码目录里中文名是政策效果评估模型，`effect.run` 不写这个号。架构稿不把这两条改挂到 235 或 236。

第 5.4 节、第 5.5 节把库名和表名连写成 `gkxlumenx_gapfill_policy_sim_result`、`gkxlumenx_gapfill_policy_sim_stakeholder`。第 0 节、第 2 节、第 9 节写的是库 `gkxlumenx_gapfill` 下的 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder`。读法仍是 element 只读 SIM 组表，不改算法路径。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。不改架构稿，不改算法代码，不改模型注册表。
