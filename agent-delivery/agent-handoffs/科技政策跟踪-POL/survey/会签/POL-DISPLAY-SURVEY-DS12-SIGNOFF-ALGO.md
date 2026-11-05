# POL-DISPLAY-SURVEY-DS12-SIGNOFF-ALGO · 政策效果推演调研 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-05
- 对象：`POL-DISPLAY-SURVEY-DS12-L01`（`survey/DS-12.md`，2026-11-03。本页不改它）
- 对照：`POL-DISPLAY-SURVEY-DS12-L01.md`；`lumen-algo-py/vendor/entan-py` 的 `polan/text/simulate.py`、`polan/text/parse.py`、`polan/job.py`、`polan/eval/layout.py`、`api/policy_routes.py`、`conf/cfg_model_registry.yaml` 的 `POLICY_SIMULATE`、`POLICY_TEXT_PARSE`、`POLICY_LAYOUT`；`lumen-svc-platform` 的 `gkxlumen-topic-async-service` 内 `PolicyAnalysisTypes.java`。指标身份取 `sdd/指标与501.md` 第 3 节
- 监管：`human:淮政玮`
- ponytail：`off`
- 范围：SRS 232–242，另加布局推荐分键。只读核对。不改调研，不改 Python 或 Java，不改模型注册表，不动 task-registry

## 结论

同意会签。

2026-11-05 动态工具目录里没有 `metric-registry`，本页未走 MCP `metric-get`。指标身份改对照 `sdd/指标与501.md` 第 3 节。不读 seed YAML，不编 D1–D3。MODEL 且 D4=`mock` 仍记 501，不写成已上线。可接统计读面仍为 0。

## 核对

可接统计读面只认 STAT 或 COMPUTE。第 3 节本页没有 COMPUTE。唯一的 STAT 是 `M_POLICY_LAYOUT_REC_COUNT`，留在布局推荐分键，不进入 232–242。三档仍是可接统计读面 0、501 共 10、跨项索引 2。分键里的推演行与 232–234 是同一条指标，不另计入。合计 12 条。

| 序号 | metric_id | algorithm_type | D4 | 代码观察 | 调研判定 |
|---|---|---|---|---|---|
| 分键·推演 | `M_POLICY_SIMULATE` | MODEL | mock | `simulate.run` 只读 `ads.policy_intensity` 中 `scope_type=province` 且力度指数非空的行，取力度前 12 省。三条情景按 `simulated = baseline * (1 + boost * elasticity)` 写出基线、推演值、变化率和逐年曲线，`TRUNCATE` 后写入 `ads.policy_simulate`。行上 `metric_id` 固定为 `M_POLICY_SIMULATE`。`JOB_SUB_TYPES` 与 `PolicyAnalysisTypes` 均无 `policy_simulate`。注册表 `POLICY_SIMULATE` 的 `status` 为 `active`，`ext.is_mock` 为 true。`GET /v1/policy/simulate` 只按 `scope_code` / `scenario_id` 读 `ads.policy_simulate` | 501。未以可调用 Job 注册。232–234 共用这一条 |
| 分键·布局推荐 | `M_POLICY_DEEP_171_1`；`M_POLICY_LAYOUT_REC_COUNT` | MODEL；STAT | mock；mock | `POLICY_LAYOUT` 的 `metric_ids` 只有 `M_POLICY_LAYOUT_REC_COUNT`，`handler_module` 为 `polan.eval.layout`，`ads_table` 为 `ads.policy_effect`，`is_mock` 为 true。`layout.run` 写入 `scope_type=region_layout`，行上 `metric_id` 为 `M_POLICY_LAYOUT_REC_COUNT`。`JOB_SUB_TYPES` 与 `PolicyAnalysisTypes` 均无 `policy_layout`。注册表未见 `M_POLICY_DEEP_171_1`。`polan/metrics/metrics.py` 的 `TABLE_MAP` 把该号映到表名 `policy_layout`。本轮未见 `layout.run` 写出该号 | 跨项索引。计数虽是 STAT，仍是布局建议条数，不能当推演页可接统计读面，不顶替 241 |
| 232 未出台政策仿真模拟 | `M_POLICY_SIMULATE` | MODEL | mock | 见分键·推演。未见未出台仿真函数。`simulate.run` 不收需规里的未出台参数 | 501 |
| 233 新出台政策效果预测 | `M_POLICY_SIMULATE` | MODEL | mock | 见分键·推演。与 232 共用同一函数，没有独立指标、独立情景 | 501 |
| 234 区域经济发展空间模拟 | `M_POLICY_SIMULATE` | MODEL | mock | 见分键·推演。空间模拟未见独立函数。产出范围是省级力度情景 | 501 |
| 235 多维度效果评估 | 未见 | 未见 | 未见 | `POLICY_EFFECT` 的 `metric_ids` 是 `M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT`，`handler_module` 为 `polan.eval.effect`。注册表未见 `M_POLICY_DEEP_168_1`。`TABLE_MAP` 把该号映到表名 `policy_effect`。本叶不挂该号 | 501。不借用 `M_POLICY_DEEP_168_1` |
| 236 利益攸关方参与评估 | 未见 | 未见 | 未见 | `simulate.py`、`parse.py`、`job.py`、`PolicyAnalysisTypes` 未见利益攸关方采集或参与评估函数 | 501 |
| 237 政策文本智能解析 | `M_POLICY_TEXT_PARSE` | MODEL | mock | `parse.run` 读 `dwd.policy_base_info`，`TRUNCATE` 后写入 `ads.policy_text_parse`，行上 `metric_id` 固定为 `M_POLICY_TEXT_PARSE`。注册表 `POLICY_TEXT_PARSE` 另列 `M_POLICY_DS_11_POLICY_EVAL_012`，`run()` 不写 012。`job.py` 的 `policy_text_parse` 只 `SELECT summary`，请求里不跑 `parse.run`。`PolicyAnalysisTypes.TEXT_PARSE` 的注释指向展示智能摘要 226。类型是 MODEL | 501。不是统计读面 |
| 238 政策重点可视化展示 | 未见 | 未见 | 未见 | `POLICY_FOCUS` 挂 `M_POLICY_FOCUS_INDEX` 与 `M_POLICY_RELATION_DEGREE`。`polan/eval/focus.py` 的 `run()` 写入 `ads.policy_focus`，行上 `metric_id` 为拼接串 `M_POLICY_FOCUS_INDEX/M_POLICY_RELATION_DEGREE`。白名单有 `policy_focus`、`policy_focus_ads`。本叶不挂焦点指数 | 501。不挂 `M_POLICY_FOCUS_INDEX` |
| 239 政策影响范围分析 | 未见 | 未见 | 未见 | 未见独立影响范围函数。`simulate.run` 只写省级力度情景 | 501。不把 `M_POLICY_SIMULATE` 改挂成统计读面 |
| 240 政策关联分析 | `M_POLICY_RELATION_DEGREE` | GRAPH | mock | 注册表 `POLICY_RE`（`handler_module` 为 `polan.graph.entity`）与 `POLICY_FOCUS` 都列了该号。`focus.run` 用 `ads.policy_graph_edge` 的边权做加权度，写入 `relation_degree`。`polan.graph.entity` 的函数体本轮未展开。白名单无关联分析键 | 跨项索引 |
| 241 政策实施路径预测 | 未见 | 未见 | 未见 | 未见路径预测函数。`layout.run` 只写布局建议条数。`simulate.run` 不写 `M_POLICY_DS_11_POLICY_EVAL_015`。注册表把 015 列在 `POLICY_SIMULATE` 下。本轮未见 `layout.run` 写出 `M_POLICY_DEEP_171_1` | 501。015 与 171 都不顶替。布局建议条数也不顶替 |
| 242 政策解读报告生成 | 未见 | 未见 | 未见 | `JOB_SUB_TYPES` 与 `PolicyAnalysisTypes` 未见解读报告键。`parse.run` 只写解析行 | 501 |

注册表与函数不一致，只记观察，本页不改注册表。`POLICY_SIMULATE` 多列了 `M_POLICY_DS_11_POLICY_EVAL_015`，`simulate.run` 只写 `M_POLICY_SIMULATE`。`POLICY_TEXT_PARSE` 多列了 `M_POLICY_DS_11_POLICY_EVAL_012`，`parse.run` 只写 `M_POLICY_TEXT_PARSE`。`focus.run` 把焦点指数和关联度拼进同一个 `metric_id`。238 仍不挂焦点指数，240 仍是跨项索引。

后续架构稿的读表退路不改变调研当时的 501，本页不因此不同意。`POL-L2-DS12-EST-ARCH` 让 232–234 读 `gapfill_policy_sim_forecast`，235 读 `gapfill_policy_sim_result`，236 读 `gapfill_policy_sim_stakeholder`，且不调用 `simulate.run`。`POL-L2-DS12-SIM-ARCH` 让 237 只读已有 `ads.policy_text_parse`，238、239、241、242 读 `gapfill_policy_sim_result`，240 消费第 7 项读图，并写明调研文件里这些叶仍是 501。读表是后续可实现退路。本页不把 501 改成可接统计读面。

232–242 没有漏挂 STAT 或 COMPUTE，也没有把布局建议条数、焦点指数、168、015、171 错挂成可接统计读面。

## 签收边界

本页不把 `POL-DISPLAY-SURVEY-DS12-L01` 标 done。签收只由 human:淮政玮 做。不改模型注册表。不改调研，不改算法代码，不动 task-registry。
