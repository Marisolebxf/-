# POL-L2-DS12-EST-METRIC-SIGNOFF-ALGO · 政策效果推演 · 效果预估 · 后台指标设计 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-EST-METRIC.md`（2026-11-05。本页不改它）
- 对照：`POL-L2-DS12-EST-ARCH.md`（2026-11-04，2026-11-05 只改第 5.4、5.5 节库.表写法）；`lumen-algo-py/vendor/entan-py` 的 `polan/text/simulate.py`、`polan/job.py`、`conf/cfg_model_registry.yaml` 的 `POLICY_SIMULATE`；`PolicyAnalysisTypes.java` 白名单。判定引自 `sdd/指标与501.md` §3.1 分键与 §3.2 的 232–236。本次会签动态工具目录无 metric 命名空间，与分册写明的回退相同，不另查 seed
- 监管：`human:淮政玮`
- 范围：SRS 232–236。只读核对。不改已有文件，不改 Python 或 Java，不改模型注册表，不动 task-registry

## 结论

同意会签。

## 核对

2026-11-05 指标身份只取 `指标与501.md` §3。分册写明动态工具目录无 metric 命名空间，未调用 `metric-get` / `metric-query`，改读该节与说明书第 2 节已有号、类型、D4 和三档。本次会签目录同样没有 metric 命名空间。未填中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1–D3，不构成不同意。不读 seed YAML，不编 D1–D3。注册表与函数不一致只记观察，不要求本页改注册表。

`polan.text.simulate.run` 只读 `ads.policy_intensity` 中 `scope_type=province` 且力度指数非空的行，按指数从高到低取前 12 省。三条情景用 `simulated = baseline * (1 + boost * elasticity)` 写出基线、推演值、变化率和逐年曲线，`TRUNCATE` 后写入 `ads.policy_simulate`。行上 `metric_id` 固定为字面量 `M_POLICY_SIMULATE`。函数不收需规四类参数，不写新出台短长期效果，不写区域 GDP、产业结构、就业率，不写维度得分，不写参与意见，插入行里也没有 `M_POLICY_DS_11_POLICY_EVAL_015`。

`PolicyAnalysisTypes` 的规范键是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`、`policy_intensity`、`policy_focus_ads`、`policy_text_parse`、`policy_region_diff`。没有 `policy_simulate`。`polan.job.JOB_SUB_TYPES` 另含内部 `policy_shard`，同样没有 `policy_simulate`。Java 白名单不注册它。

`cfg_model_registry.yaml` 的 `POLICY_SIMULATE` 把 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015` 列在同一 `metric_ids` 下，`handler_module` 为 `polan.text.simulate`，`ads_table` 为 `ads.policy_simulate`。`run()` 只写前一个号。

| 序号 | metric_id | 代码 | 指标分册 |
|---|---|---|---|
| 232 | `M_POLICY_SIMULATE`。MODEL。D4=`mock`。判定 501。真路径写无 STAT/COMPUTE 可挂 | `simulate.run` 只写省级力度情景，不收政策类型、覆盖范围、支持力度、实施时间 | 沿用这一条。D4 仍是 mock。未出台仿真行上的 `metric_id` 用这个已有号。读 `gapfill_policy_sim_forecast`。不把情景弹性收成公式，不调用 `run()`，不读 `ads.policy_simulate`。Java 不按弹性现算 |
| 233 | 同上。与 232 共用同一推演模型，没有独立指标 | 同上。函数不写短长期效果，也不写 `M_POLICY_TEXT_PARSE` | 沿用同一条。不另起指标。不调 `parse/jobs`，不把解析结果顶替预测行 |
| 234 | 同上。空间模拟没有独立指标 | 同上。函数不写区域 GDP、产业结构、就业率 | 沿用同一条。不另起指标。区域空间行仍用这个已有号。不把弹性收成空间公式 |
| 235 | 未见。判定 501。真路径写不借用 `M_POLICY_DEEP_168_1` | 无多维评分函数。`run()` 不写维度得分 | 不新注册。不挂 `M_POLICY_SIMULATE`。不挂 `M_POLICY_DEEP_168_1`、`M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT`。行上 `metric_id` 留空。读 `gapfill_policy_sim_result`。无行则空，不造得分 |
| 236 | 未见。判定 501。真路径写关键词「利益」为 0 条 | 无意见采集函数。`run()` 不写意见 | 不新注册。不挂 `M_POLICY_SIMULATE`。不挂两条布局推荐键。行上 `metric_id` 留空。读 `gapfill_policy_sim_stakeholder`。请求不插入。已灌行计数不新注册，不改成可接统计读面 |

232–234 只挂已有 `M_POLICY_SIMULATE`，不新造第二条、第三条推演指标，D4 保持 `mock`，不升 live。235、236 没有专属 `metric_id`，没有可改的 D4。分册不列八件套全表，不手抄公式，也不另写一条能算出经济效益、社会影响、创新促进、短长期效果、GDP、产业结构、就业率、维度得分或意见汇总的式子。

`指标与501` §3.2 把推演页可接统计读面写成 0。`M_POLICY_LAYOUT_REC_COUNT` 在 §3.1 是布局推荐键，类型 STAT，D4=`mock`，判定跨项索引。`M_POLICY_DEEP_171_1` 同键，类型 MODEL，D4=`mock`，判定跨项索引。分册不把这两条改挂进 232–236，也不把 STAT 计数写成推演页的可接统计读面。架构稿第 6 节同样不让这两条进入推演页任何区。

观察（不构成不同意，也不要求改注册表）：`M_POLICY_DS_11_POLICY_EVAL_015` 挂在 `POLICY_SIMULATE` 下，`simulate.run` 只写 `M_POLICY_SIMULATE`。分册不调用该函数，不改注册表，不把 015 写进 232–234 的预估行。`M_POLICY_EFFECT_SCORE` 留在评价页，不改挂 232、233。

未发现把布局建议条数或 `M_POLICY_DEEP_171_1` 改挂到 232–236，也未发现把省级力度弹性收成 232、233 或 234 的公式，也未发现把 `M_POLICY_SIMULATE` 填进 235 或 236。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。不改指标分册，不改架构稿，不改算法代码，不改模型注册表。
