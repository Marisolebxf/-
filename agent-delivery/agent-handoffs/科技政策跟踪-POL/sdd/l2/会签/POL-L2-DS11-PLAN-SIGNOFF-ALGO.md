# POL-L2-DS11-PLAN-SIGNOFF-ALGO · 政策分析评价 · 推荐方案报告交互展示 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-PLAN-ARCH.md`（2026-11-03。本页不改它）
- 对照：`sdd/指标与501.md` 第 2 节序号 227–231。代码只读 `lumen-algo-py/vendor/entan-py/polan/text/simulate.py`、`api/policy_routes.py` 的 `_MODEL_TABLE`、`conf/cfg_model_registry.yaml` 的 `POLICY_SIMULATE`，以及 `lumen-svc-platform` 的 `PolicyAnalysisTypes`
- 监管：`human:淮政玮`
- 范围：SRS 227–231。只读核对。不改架构正文，不改 Python 或 Java，不动 task-registry，不新造 `metric_id`，不改 D4

## 结论

同意

## 核对

2026-11-03 指标身份只取 `指标与501.md`。不读 seed YAML，不编 D1–D3。

227、228、230、231 在分册里未见专属 `metric_id`，判定 501。229 已有 `M_POLICY_DS_11_POLICY_EVAL_015`，类型 GRAPH，D4=`mock`，判定仍是 501。口径是路径与风险的生成结果，不是第 7 项在线读图。分册写明 228 不挂 `M_POLICY_SIMULATE`。

`_MODEL_TABLE` 没有方案、参数模拟、路径、意见、导出。`polan/text/simulate.py` 的 `run()` 只按省取 `ads.policy_intensity` 的力度指数，用 `baseline * (1 + boost * elasticity)` 写基线、推演值、变化率和逐年曲线，落入 `ads.policy_simulate`，行上 `metric_id` 固定为 `M_POLICY_SIMULATE`。它不写方案、参数档、路径节点、风险和专家意见，也不产出 `M_POLICY_DS_11_POLICY_EVAL_015`。

`cfg_model_registry.yaml` 的 `POLICY_SIMULATE` 把 `M_POLICY_SIMULATE` 和 `M_POLICY_DS_11_POLICY_EVAL_015` 列在同一模型下，`handler_module` 是 `polan.text.simulate`。函数本身不产出 015。架构稿不改注册表，也不把这次 `run()` 迁到评价页。

| 序号 | 架构稿 | 代码 |
|---|---|---|
| 227 | 没有方案生成模型。读 `gapfill_policy_eval_scheme` 的方案对照行。少于两行则对比空。不挂 `M_POLICY_LAYOUT_REC_COUNT` | 仓库里没有按评估模型写出多个改进方案的函数 |
| 228 | 没有方案模拟模型。按方案和参数档读同一张表。对不上则空。请求内不重算，不套弹性公式 | `simulate.run` 只写省级力度情景。架构不调用它 |
| 229 | 读路径与风险行。行上 `metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015`。不读图，不用推演曲线顶替 | 现有 `run()` 不产出这条指标。架构不为此新写公式 |
| 230 | 没有采集服务。只读已灌意见行。请求不插入 | 无意见模型 |
| 231 | 没有方案报告模型。导出从当次读到的方案行和意见行生成。不灌文件 | 不是 `report/jobs`，也不是 `simulate.run` |

`PolicyAnalysisTypes` 的规范键是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`，另放行 `policy_intensity` 只做转发。没有 `policy_scheme`。架构稿不加这个键，也不把 227–231 塞进其中任何一项。展示链不打 `/internal/analysis/policy/simulate`。Java 不写 nGQL，不把 `simulate.run` 抄进请求处理。

五叶共用 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。查询只读。无行则该块空。路径与风险行沿用已有 `metric_id`。其余三种没有已挂指标，`metric_id` 留空。D4 保持 mock。缺项表的行是灌入的 mock，不是方案生成模型。

未发现架构稿把未注册的方案生成写成可算公式，也未发现把 `polan.text.simulate.run` 抄进 Java。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。
