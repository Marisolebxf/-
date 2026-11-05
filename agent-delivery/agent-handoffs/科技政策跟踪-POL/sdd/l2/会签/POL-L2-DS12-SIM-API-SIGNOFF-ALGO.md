# POL-L2-DS12-SIM-API-SIGNOFF-ALGO · 政策效果推演 · 科技政策推演 · 后台接口 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-API.md`（2026-11-05。本页不改它）
- 对照：`sdd/l2/POL-L2-DS12-SIM-ARCH.md`（含 2026-11-05 第 7、9 节）；`sdd/l2/POL-L2-DS12-SIM-METRIC.md`；`lumen-algo-py/vendor/entan-py` 的 `polan/text/parse.py`、`polan/text/simulate.py`、`polan/job.py`、`conf/cfg_model_registry.yaml` 的 `POLICY_TEXT_PARSE`、`POLICY_SIMULATE`；`PolicyAnalysisTypes.java` 白名单。判定引自 `sdd/指标与501.md` §3
- 监管：`human:淮政玮`
- 强度：ponytail off
- 范围：SRS 237–242。只读核对。不改分册，不改 Python 或 Java，不改模型注册表，不动 task-registry

## 结论

同意会签。

## 核对

2026-11-05 指标身份只取 `指标与501.md` §3。不读 seed YAML，不编 D1–D3。注册表与函数不一致只记观察，不要求本页改注册表。

`polan.text.parse.run` 从 `dwd.policy_base_info` 取 `is_deleted=0` 的政策，用规则写出摘要、结构化要素和自动标签，然后 `truncate` 整张 `ads.policy_text_parse` 再插入。摘要取 abstract，空则取 content，并截断。结构化要素写入政策类型、级别、区域、发布年、要点；源对象里已有的适用对象、支持方式、申报条件会抄进同一结构。自动标签来自关键词、政策类型、主题。每一行的 `metric_id` 固定为字面量 `M_POLICY_TEXT_PARSE`。函数不写重点项、影响对象、路径环节、解读段落，插入行里也没有 `M_POLICY_SIMULATE`。一次展示请求若调用 `run()`，会清空整表，条款行一并被清掉。

`polan.text.simulate.run` 只读 `ads.policy_intensity` 中 `scope_type=province` 且力度指数非空的行，取力度前 12 省。三条情景按 `simulated = baseline * (1 + boost * elasticity)` 写出基线、推演值、变化率和逐年曲线，`truncate` 后写入 `ads.policy_simulate`。行上 `metric_id` 固定为 `M_POLICY_SIMULATE`。函数不写重点、影响范围、路径环节、解读段落，也不写 `M_POLICY_DS_11_POLICY_EVAL_015`。

`PolicyAnalysisTypes` 的规范键是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`、`policy_intensity`、`policy_focus_ads`、`policy_text_parse`、`policy_region_diff`。没有 `policy_simulate`，也没有重点可视化、影响范围、路径预测、解读报告键。`policy_text_parse` 的注释是展示智能摘要（226）。`polan.job.JOB_SUB_TYPES` 另含内部 `policy_shard`，Java 白名单不注册它。`JOB_SUB_TYPES` 含 `policy_text_parse`；`execute` 在该键上只读 `summary`，不调用 `parse.run`。白名单里没有 `policy_simulate`。

`POLICY_TEXT_PARSE` 的 `status` 为 active，`metric_ids` 同时列 `M_POLICY_TEXT_PARSE` 与 `M_POLICY_DS_11_POLICY_EVAL_012`，`handler_module` 为 `polan.text.parse`，`invoke_path` 为 `/internal/analysis/policy/text-parse`，`ext.ads_table` 为 `ads.policy_text_parse`，`ext.is_mock` 为 true。`parse.run` 只写 `M_POLICY_TEXT_PARSE`。`POLICY_SIMULATE` 同时列 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015`，`handler_module` 为 `polan.text.simulate`，`invoke_path` 为 `/internal/analysis/policy/simulate`，`ext.ads_table` 为 `ads.policy_simulate`。`simulate.run` 只写 `M_POLICY_SIMULATE`。

| 序号 | metric_id | 代码 | 接口稿 |
|---|---|---|---|
| 237 | `M_POLICY_TEXT_PARSE`。MODEL。D4=`mock`。判定 501 | `parse.run` 清空整表后写入，行上只有这一条 `metric_id`。已有 `policy_text_parse` 键只读 `summary`，不调用 `parse.run`。该键是评价 226 | 第 1、3 节：种类为文本解析，同步读已有 `ads.policy_text_parse` 的解析行。行上 `metric_id` 保持 `M_POLICY_TEXT_PARSE`。请求路径不调用 `polan.text.parse.run`。不改 226 的 `policy_text_parse` 键。不加新 Job 键。不灌 gapfill。不新造指标 |
| 238 | 未见。判定 501。不挂 `M_POLICY_FOCUS_INDEX`，不挂 `M_POLICY_SIMULATE` | 未见重点可视化函数。`simulate.run` 不写重点项 | 第 4 节：同步读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的重点行。行上 `metric_id` 留空。不新造指标 |
| 239 | 未见。判定 501。不挂 `M_POLICY_SIMULATE` | `simulate.run` 只写省级力度情景，不写影响范围 | 第 5 节：同步读同一张缺项表的影响范围行。行上 `metric_id` 留空。不新建 Python simulate job。不读 `ads.policy_simulate` |
| 240 | `M_POLICY_RELATION_DEGREE`。GRAPH。D4=`mock`。判定跨项索引 | 未见本页查图函数。白名单无关联分析键 | 第 1、6 节：无 HTTP 资源，无种类，不走 `simulation/jobs`。沿用已有号，不新造独立 `metric_id`，不为此加资源。Java 不写 nGQL |
| 241 | 未见。判定 501。不挂 `M_POLICY_LAYOUT_REC_COUNT`，不挂 `M_POLICY_DS_11_POLICY_EVAL_015`，不挂 `M_POLICY_SIMULATE` | `simulate.run` 不写路径环节，也不写 015。未见路径预测函数 | 第 7 节：同步读同一张缺项表的路径环节行。行上 `metric_id` 留空。不把 `M_POLICY_SIMULATE` 写进这些行 |
| 242 | 未见。判定 501。不挂 `M_POLICY_SIMULATE` | 未见解读报告函数，也未见产文件函数 | 第 8 节：同步读同一张缺项表的解读段落行。页面呈现正文。不产生 PDF，不产生 Word。不写对象存储。行上 `metric_id` 留空 |

六条核与接口稿、架构稿、指标稿一致：

- 不新建指标。237 保持已有 `M_POLICY_TEXT_PARSE`。240 沿用已有 `M_POLICY_RELATION_DEGREE`，不另造独立号。238、239、241、242 行上 `metric_id` 留空。第 10 节写明不新造 `metric_id`，不把 `M_POLICY_SIMULATE`、`M_POLICY_FOCUS_INDEX`、`M_POLICY_DS_11_POLICY_EVAL_015`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1` 挂到本六叶的缺项行。012 不挂 237。
- 237 的请求不调用 `polan.text.parse.run`。第 1、2、3、10 节写明同步读，不进 `gkxlumen-topic-async-service`，不进 `POST /internal/policy/jobs/execute`，不把 237–242 写入 `PolicyAnalysisTypes` 或 `JOB_SUB_TYPES`。
- 240 不设资源。
- 不新建 Python simulate job。第 1、10 节写明不调用 `polan.text.simulate`，不读 `ads.policy_simulate`，不加 `policy_simulate`。
- D4 仍是 mock。237 与 240 只转述 `指标与501` 已有的 mock。解析行已落在 ADS，不因此升 live。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。238、239、241、242 没有专属 `metric_id`，没有可改的 D4。缺项行仍是 mock。
- 242 不产生文件。第 8、9、10 节写明不产生 PDF、Word，不灌文件，不灌自定义格式，不把 `report/jobs` 或 `gkxlumenx_gapfill.gapfill_policy_report_body` 写成这条资源。

`指标与501` §3.2 仍把 237、238、239、241、242 记为 501，把 240 记为跨项索引。§8 把 237–239、241、242 的真路径写成「501，页面空态」，并写明解析行 237 同此。接口稿不改 `指标与501.md`，不把 501 改成可接统计读面，不把 240 改出跨项索引。读面沿架构：237 读已有解析表，238、239、241、242 读缺项表，有行则读表，无行则该区空。

观察（不构成不同意，也不要求改注册表）：

- `POLICY_TEXT_PARSE` 已是 active，并有 `invoke_path`。`ext.is_mock` 为 true。这不是 metric MCP 的 D4。接口第 1 节写明当前五次读取保持同步读，不加 Job 键；`M_POLICY_TEXT_PARSE` 日后若作为可调用解析服务接通，237 才可切异步真算，注册动作不在本分册。226 的 `policy_text_parse` 键保持原状。本页不把 active 写成 237 已在请求里调用 `parse.run`。
- `POLICY_TEXT_PARSE` 把 012 与 `M_POLICY_TEXT_PARSE` 并列。`parse.run` 只写后者。接口不挂 012。
- `POLICY_SIMULATE` 把 015 与 `M_POLICY_SIMULATE` 并列。`simulate.run` 只写后者，且只写省级力度情景。接口不新建 simulate job，不调用该函数，不把 015 或 `M_POLICY_SIMULATE` 挂到 237–242。
- 接口第 3 节沿架构 §1.4：`structured_elements` 含 `"clauses"` 键的行不返回，判别写法交给数据分册。这不改变「请求不调用 `parse.run`」和「行上号保持 `M_POLICY_TEXT_PARSE`」。

未发现接口稿新造 `metric_id`，未发现 237 改号或在请求路径调用 `parse.run`，未发现 240 设资源，未发现新建 Python simulate job，未发现改 D4，未发现 242 产生文件。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。不改接口稿，不改架构稿，不改指标稿，不改算法代码，不改模型注册表。
