# POL-L2-DS11-PLAN-SIGNOFF-ALGO · 政策分析评价 · 推荐方案报告交互展示 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-PLAN-ARCH.md`（2026-11-03。本页不改它）
- 对照：`lumen-algo-py/vendor/entan-py` 的 `polan/text/simulate.py`、`polan/eval/layout.py`、`polan/eval/effect.py`、`polan/text/parse.py`、`polan/job.py`、`conf/cfg_model_registry.yaml` 的 `POLICY_SIMULATE`、`POLICY_LAYOUT`、`POLICY_EFFECT`、`POLICY_TEXT_PARSE`、`POLICY_FOCUS`；`PolicyAnalysisTypes.java` 白名单。判定引自 `sdd/指标与501.md` 227–231。边界对照 `POL-L2-DS11-READ-ARCH.md`、`sdd/调用链与边界.md` 与说明书第 11.2 节
- 监管：`human:淮政玮`
- 范围：SRS 227–231。只读核对。不改已有文件，不改 Python 或 Java，不改模型注册表，不动 task-registry

## 结论

同意会签。

## 核对

2026-11-03 指标身份只取 `指标与501.md`。不读 seed YAML，不编 D1–D3。注册表与函数不一致只记观察，不要求本页改注册表。

`polan.text.simulate.run` 只读 `ads.policy_intensity` 中 `scope_type=province` 且力度指数非空的行，取力度前 12 省。三条情景用 `simulated = baseline * (1 + boost * elasticity)` 写出基线、推演值、变化率和逐年曲线，`TRUNCATE` 后写入 `ads.policy_simulate`。行上 `metric_id` 固定为 `M_POLICY_SIMULATE`。函数不写方案、参数档、路径节点、风险、专家意见，也不写 `M_POLICY_DS_11_POLICY_EVAL_015`。

`PolicyAnalysisTypes` 的规范键是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`。没有 `policy_scheme`，也没有推演键。`polan.job.JOB_SUB_TYPES` 另含内部 `policy_shard`，Java 白名单不注册它。

| 序号 | metric_id | 代码 | 架构稿 |
|---|---|---|---|
| 227 | 未见。判定 501。不把布局建议条数写入本页 | `layout.run` 把 `M_POLICY_LAYOUT_REC_COUNT` 写入 `ads.policy_effect`（`scope_type=region_layout`）。注册表 `POLICY_LAYOUT` 只挂这一条。仓库里没有按评估模型生成多个改进方案再出雷达和 KPI 的函数 | 不挂 `M_POLICY_LAYOUT_REC_COUNT`，也不挂 `M_POLICY_DEEP_171_1`。读 `gapfill_policy_eval_scheme` 的方案对照行。少于两行则对比空。不调用 `layout.run` |
| 228 | 未见。判定 501。不挂 `M_POLICY_SIMULATE` | 见上。`simulate.run` 只写省级力度情景 | 不迁 `polan.text.simulate.run`、`M_POLICY_SIMULATE`、`ads.policy_simulate`。按方案和参数档读同一张缺项表。请求内不按弹性公式现算，不把 `simulate.run` 加进白名单 |
| 229 | `M_POLICY_DS_11_POLICY_EVAL_015`。GRAPH。D4=`mock`。口径是路径与风险生成，不是第 7 项在线读图 | 注册表把该号列在 `POLICY_SIMULATE` 的 `metric_ids` 下，`handler_module` 为 `polan.text.simulate`，`ads_table` 为 `ads.policy_simulate`。`run()` 不产出这条指标，也不产出路径与风险 | 不改注册表，不调用 `simulate.run`，不读政策子图，不写 nGQL。缺项表的路径与风险行沿用该 `metric_id`。D4 仍是 `mock`。无行则路径和风险都空，不用推演曲线顶替。序号 241 不顶替本叶 |
| 230 | 未见。判定 501 | 无意见采集函数，无意见指标 | 只读已灌意见行。请求不插入。不把序号 210 的 `gapfill_policy_audience_feedback` 当成方案意见 |
| 231 | 未见。判定 501。无导出 Job | 无方案报告模型。白名单无导出键 | 从当次读到的方案对照行和意见行生成。不灌文件。不是 `report/jobs`，也不是序号 222 |

第 11.2 节「评价 · 方案 227–231」只有一张 `gapfill_policy_eval_scheme`，灌数单 `POL-L2-DS11-PLAN-GAPFILL-L01`。架构稿五叶共用这一张表，种类为方案对照、参数模拟、路径与风险、互动意见。231 不另占种类。227、228、230 没有已挂指标，行上 `metric_id` 留空。不新造 `metric_id`。

观察：`M_POLICY_DS_11_POLICY_EVAL_015` 挂在 `POLICY_SIMULATE` 下，`simulate.run` 只写 `M_POLICY_SIMULATE`。架构稿不调用该函数，本页不要求改注册表。`POLICY_TEXT_PARSE` 下的 `M_POLICY_DS_11_POLICY_EVAL_012` 属于序号 226，`parse.run` 写入的行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。本叶不挂 012。`M_POLICY_EFFECT_SCORE` 由 `effect.run` 写入 `scope_type=region_effect`，留在页上效能，不挂 227–231。

未发现架构稿把布局建议条数改挂到 227，也未发现把省级力度推演迁到 228 或 229。缺项表是灌入的 mock，不用 501 充当这五叶的画面。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。

## 第二轮（2026-11-03 返工后）

### 结论

同意会签。

227 不挂布局建议条数。228 不迁 `polan.text.simulate.run`、`M_POLICY_SIMULATE`、`ads.policy_simulate`。229 沿用 `M_POLICY_DS_11_POLICY_EVAL_015`，不调用 `simulate.run`，不改注册表。

### 核对

`polan/text/simulate.py` 的 `run()` 只读 `ads.policy_intensity` 中 `scope_type=province` 且力度指数非空的行，取力度前 12 省。三条情景按 `simulated = baseline * (1 + boost * elasticity)` 写出基线、推演值、变化率和逐年曲线，`TRUNCATE` 后写入 `ads.policy_simulate`。行上 `metric_id` 固定为 `M_POLICY_SIMULATE`。函数不写方案、参数档、路径节点、风险、专家意见，也不写 `M_POLICY_DS_11_POLICY_EVAL_015`。

`PolicyAnalysisTypes` 仍在 `lumen-svc-platform` 的 `gkxlumen-topic-async-service`。规范键是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`、`policy_focus_ads`、`policy_text_parse`。没有 `policy_scheme`，也没有推演键。不注册内部 `policy_shard`。

| 序号 | 架构稿 | 代码 | 判定 |
|---|---|---|---|
| 227 | 第 5.1 节、第 6 节、第 9 节：不挂 `M_POLICY_LAYOUT_REC_COUNT`，也不挂 `M_POLICY_DEEP_171_1`。读 `gapfill_policy_eval_scheme` 的方案对照行。不调用 `layout.run` | 本叶不要求调用布局函数 | 同意 |
| 228 | 第 5.2 节、第 6 节、第 7 节、第 8 节：不迁 `simulate.run`、`M_POLICY_SIMULATE`、`ads.policy_simulate`。按方案和参数档读同一张缺项表。请求内不按弹性公式现算，不把 `simulate.run` 加进白名单 | `simulate.run` 只写省级力度情景 | 同意 |
| 229 | 第 5.3 节、第 9 节：路径与风险行沿用 `M_POLICY_DS_11_POLICY_EVAL_015`。不改注册表，不调用 `simulate.run`，不读政策子图，不写 nGQL。无行则路径和风险都空。序号 241 不顶替 | `run()` 不产出这条指标，也不产出路径与风险 | 同意 |
| 230 | 只读已灌意见行。请求不插入。不把序号 210 的 `gapfill_policy_audience_feedback` 当成方案意见 | 无意见采集函数 | 同意 |
| 231 | 从当次读到的方案对照行和意见行生成。不灌文件。不是 `report/jobs`，也不是序号 222 | 白名单无导出键 | 同意 |

观察（不构成不同意，也不要求改注册表）：架构稿第 3.1 节写明，模型注册表把 `M_POLICY_DS_11_POLICY_EVAL_015` 列在 `POLICY_SIMULATE` 下，`simulate.run` 只写 `M_POLICY_SIMULATE`。本叶不调用该函数，不改注册表。

未发现把布局建议条数改挂到 227，也未发现把省级力度推演迁到 228 或 229。

### 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。不改架构稿，不改算法代码，不改模型注册表。
