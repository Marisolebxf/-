# POL-L2-DS12-SIM-SIGNOFF-ALGO · 政策效果推演 · 科技政策推演 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-ARCH.md`（2026-11-04。本页不改它）
- 对照：`lumen-algo-py/vendor/entan-py` 的 `polan/text/parse.py`、`polan/text/simulate.py`、`polan/job.py`、`conf/cfg_model_registry.yaml` 的 `POLICY_TEXT_PARSE`、`POLICY_SIMULATE`、`POLICY_LAYOUT`、`POLICY_FOCUS`；`PolicyAnalysisTypes.java` 白名单。评价只读先例对照 `sdd/l2/POL-L2-DS11-READ-ARCH.md` 序号 226。判定引自 `sdd/指标与501.md` §3
- 监管：`human:淮政玮`
- 强度：ponytail off
- 范围：SRS 237–242。只读核对。不改已有文件，不改 Python 或 Java，不改模型注册表，不动 task-registry

## 结论

同意会签。

## 核对

2026-11-05 调用 `metric-get` 时，MCP 命名空间 `metric-registry` 未加载。指标身份只取 `指标与501.md`。不读 seed YAML，不读就绪度矩阵，不编 D1–D3，也不补 501 表上没有的口径、公式、源表、源系统、更新频率和版本。注册表与函数不一致只记观察，不要求本页改注册表。

`polan.text.parse.run` 从 `dwd.policy_base_info` 做规则截取，写出标题、摘要、结构化要素和自动标签，行上 `metric_id` 固定为 `M_POLICY_TEXT_PARSE`。插入前 `conn.truncate` 清空整张 `ads.policy_text_parse`。`polan/clause_job.py` 把 `clauses` 写进同一张表的 `structured_elements`；条款写入本身不 TRUNCATE，文件注明灌数重灌仍会清空该表。

`polan.job._policy_text_parse_rows` 只执行 `SELECT summary FROM ads.policy_text_parse`。`execute_policy_job` 在 `sub_type=policy_text_parse` 时走这条查询，不调用 `parse.run`。这是评价页 226 的已有先例：`POL-L2-DS11-READ-ARCH` 写明 226 只读 `ads.policy_text_parse.summary`，请求不调用 `parse.run`。Java `PolicyAnalysisTypes.TEXT_PARSE` 已是 `policy_text_parse`，注释为展示智能摘要（226）。

`polan.text.simulate.run` 只读 `ads.policy_intensity` 中 `scope_type=province` 且力度指数非空的行，取力度前 12 省。三条情景按 `simulated = baseline * (1 + boost * elasticity)` 写出基线、推演值、变化率和逐年曲线，`TRUNCATE` 后写入 `ads.policy_simulate`。行上 `metric_id` 固定为 `M_POLICY_SIMULATE`。函数不写重点、影响范围、路径环节、解读段落，也不写 `M_POLICY_DS_11_POLICY_EVAL_015`。

`PolicyAnalysisTypes` 的规范键是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`、`policy_intensity`、`policy_focus_ads`、`policy_text_parse`、`policy_region_diff`。没有推演键，也没有重点可视化、影响范围、路径预测、解读报告键。`polan.job.JOB_SUB_TYPES` 另含内部 `policy_shard`，Java 白名单不注册它。本叶不把 `parse.run` 加进该白名单。

`polan` 下已有 `run` 为解析、推演、焦点、布局、力度、效果、匹配、图谱实体等。未见重点可视化、影响范围、路径预测、解读报告的独立模型函数。这四叶读 `gapfill_policy_sim_result` 是缺项退路。退路不写成模型已上线。`POLICY_TEXT_PARSE` 的 `ext.is_mock` 为 true，501 的 D4 仍是 `mock`。

| 序号 | metric_id | 代码 | 架构稿 |
|---|---|---|---|
| 237 | `M_POLICY_TEXT_PARSE`。MODEL。D4=`mock`。判定 501 | `parse.run` 清空整表后写入，行上只有这一条 `metric_id`。请求路径上的 `policy_text_parse` 只读 `summary`，不调用 `parse.run`。白名单里的该键是评价 226，不是 `parse.run` | element 只读已落库解析行，取 `title / summary / auto_tags / structured_elements`，排除 `structured_elements` 含 `"clauses"` 的条款行。请求不调用 `parse.run`，不把该函数加进展示白名单，不加新 Job 键。既有 `policy_text_parse` 保持 226 原状。无行则报告空 |
| 238 | 未见。判定 501。不挂 `M_POLICY_FOCUS_INDEX` | 未见重点可视化函数。`POLICY_FOCUS` 挂焦点指数，`focus.run` 写入 `ads.policy_focus` | 读 `gapfill_policy_sim_result` 的重点行。行上 `metric_id` 留空。不挂焦点指数 |
| 239 | 未见。判定 501。不挂 `M_POLICY_SIMULATE` | `simulate.run` 只写省级力度情景，不写影响范围 | 读同一张缺项表的影响范围行。行上 `metric_id` 留空。不挂 `M_POLICY_SIMULATE` |
| 240 | `M_POLICY_RELATION_DEGREE`。GRAPH。D4=`mock`。判定跨项索引。展示只消费读图 | 本叶未见新建查图函数。`focus.run` 从 `ads.policy_graph_edge` 算关联度写入 `ads.policy_focus`，不发 nGQL。`PolicyAnalysisTypes` 无关联分析键，也无 nGQL | 不设种类、不设资源。页面消费第 7 项已有读图。不新建查图算法任务。Java 不写 nGQL。不改打 `E-E7-POLICY-M1-L06` |
| 241 | 未见。判定 501。不挂 `M_POLICY_LAYOUT_REC_COUNT`，不挂 `M_POLICY_DS_11_POLICY_EVAL_015`，不挂 `M_POLICY_DEEP_171_1` | `layout.run` 把 `M_POLICY_LAYOUT_REC_COUNT` 写入 `ads.policy_effect`（`scope_type=region_layout`）。`POLICY_LAYOUT` 只挂这一条。未见路径预测函数。`simulate.run` 不写 015，也不写路径环节 | 读同一张缺项表的路径环节行。行上 `metric_id` 留空。不把布局建议条数、015、171 填进本叶 |
| 242 | 未见。判定 501。不挂 `M_POLICY_SIMULATE` | 未见解读报告函数，无导出模型 | 读同一张缺项表的解读段落行。行上 `metric_id` 留空。页面呈现正文，不灌文件 |

501 §3.2 仍把 237、238、239、241、242 记为 501，把 240 记为跨项索引。架构稿写明会签前不改写 `指标与501.md`。本页可实现链路是读已有解析行和缺项行，以及 240 消费已有读图。501 的判定保留，不把读表退路改写成模型已上线。

`M_POLICY_FOCUS_INDEX` 在 501 序号 223 为 MODEL、D4=`mock`、判定 501。`M_POLICY_DS_11_POLICY_EVAL_015` 在序号 229 为 GRAPH、D4=`mock`、判定 501，口径是路径与风险生成。`M_POLICY_SIMULATE` 在 §3.1 为 MODEL、D4=`mock`、判定 501，只挂 232–234。`M_POLICY_DEEP_171_1` 为 MODEL、D4=`mock`、跨项索引；`M_POLICY_LAYOUT_REC_COUNT` 为 STAT、D4=`mock`、跨项索引。这五条都不挂 238、239、241、242。

观察（不构成不同意，也不要求改注册表）：

- `POLICY_TEXT_PARSE` 的 `metric_ids` 同时列 `M_POLICY_TEXT_PARSE` 与 `M_POLICY_DS_11_POLICY_EVAL_012`，`handler_module` 为 `polan.text.parse`。`parse.run` 只写 `M_POLICY_TEXT_PARSE`。012 属于评价 226。237 不调用 `parse.run`，不挂 012。
- `POLICY_SIMULATE` 的 `metric_ids` 同时列 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015`，`handler_module` 为 `polan.text.simulate`。`simulate.run` 只写 `M_POLICY_SIMULATE`。本叶不调用该函数，不把 015 挂到 241。
- `POLICY_FOCUS` 同时列 `M_POLICY_FOCUS_INDEX` 与 `M_POLICY_RELATION_DEGREE`，`ads_table` 为 `ads.policy_focus`。`focus.run` 把两条号拼成一个 `metric_id` 字符串写入该表。`POLICY_RE` 也列 `M_POLICY_RELATION_DEGREE`，`handler_module` 为 `polan.graph.entity`，`graph_space` 为 `gkx_policy`。501 把关联度标成 GRAPH、跨项索引。240 只消费第 7 项读图，不调用 `focus.run`。
- `POLICY_LAYOUT` 只挂 `M_POLICY_LAYOUT_REC_COUNT`。`M_POLICY_DEEP_171_1` 不在 `POLICY_TEXT_PARSE`、`POLICY_SIMULATE`、`POLICY_LAYOUT`、`POLICY_FOCUS` 的 `metric_ids` 里。

未发现架构稿把 `parse.run` 放进 237 的请求路径或展示白名单。未发现把焦点指数、015、布局推荐计数、`M_POLICY_SIMULATE`、`M_POLICY_DEEP_171_1` 挂到 238、239、241、242 的缺项行。未发现为本叶新建查图算法任务。未发现把缺项表读法写成重点可视化、影响范围、路径预测或解读报告的模型已上线。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。不改架构稿，不改算法代码，不改模型注册表。
