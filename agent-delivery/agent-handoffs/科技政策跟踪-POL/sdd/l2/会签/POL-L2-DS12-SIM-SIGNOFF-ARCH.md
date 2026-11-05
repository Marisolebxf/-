# POL-L2-DS12-SIM-SIGNOFF-ARCH · 政策效果推演 · 科技政策推演 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-ARCH`（2026-11-04）。本页不重新设计，不改那份架构
- 监管：`human:淮政玮`
- 强度：ponytail off
- 对照：同目录 `POL-L2-DS12-EST-ARCH`（232–236，只读）；说明书第 11 节总规则与第 11.2 节；`sdd/调用链与边界.md`；`sdd/契约输入清单.md` 的 `simulation/jobs`；`survey/DS-12.md`；已签收 `POL-L2-DS11-READ-ARCH` §4.4 与 `POL-L2-DS11-READ-SIGNOFF-ARCH`（`policy_text_parse` 只读先例）。下游 API / METRIC / DATA 尚未以本页代写

## 结论

同意会签

237 读已有 `ads.policy_text_parse`，请求不跑 `polan.text.parse.run`。这符合说明书第 11 节：已有表、已有产出，就不建缺项行。第 11.2 节把「文本解析」写在仿真组灌数清单里，本叶的收窄成立。`POL-L2-DS12-SIM-GAPFILL-L01` 开工时不灌文本解析行。

238、239、241、242 按种类读 `gapfill_policy_sim_result`。240 不设资源，只消费第 7 项子图。与 EST 共用一条 `simulation/jobs`，不重复实现 232–236，不改 `gapfill_policy_sim_stakeholder` 的灌数内容。本叶缺项行 `metric_id` 留空，不进异步白名单。调研仍写 501，稿内已写明会签前不改调研，不构成不同意。

同意会签不是签收。

## 核对

| 项 | 架构稿 | 判定 |
|---|---|---|
| 算法只在 Python。Java 不跑解析、不写 nGQL、不直连库、不直连 Python | 237 由 `gkxlumen-element` 只读已落库解析行，请求不调用 `polan.text.parse.run`。238、239、241、242 只读缺项行，不生成重点、影响范围、路径或解读。240 只消费第 7 项子图，Java 不写 nGQL，不新建查图任务。`gkxlumen-display` 不直连库、不直连 Python，不写算法。真模型未注册的能力保持空态；注册后的 async 不在本叶，本叶不加 Job 键 | 一致 |
| 浏览器只打 `/display/v1/policy/**`。不打 `/v1/policy/text/parse`，不打专题 URL，不调 `demo-*` | 六叶对外只有已有的 `POST /display/v1/policy/simulation/jobs`；240 连这条也不走。`GET /v1/policy/text/parse` 与 demo「文本解析」签留在算法中台，展示不直连、不嵌入。不改打 `/topic/v1/policy`，不把 `E-E7-POLICY-M1-L06` 写成展示路径。契约「`M_POLICY_TEXT_PARSE` 不为推演单开 URL」：本叶不开新 URL，在同一条 `simulation/jobs` 上按种类读已有解析表 | 一致 |
| 237 收窄第 11.2 节「文本解析要灌缺项行」。是否符合第 11 节「已有表与已有产出就不建缺项行」 | 第 11 节：已经有 ADS 表、也有可调用计算的，不新建表，接口读已有表；没有表也没有算法的，才建 `gapfill_` 表。`ads.policy_text_parse` 已在。批产 `polan.text.parse.run` 已向该表写入标题、摘要、自动标签、结构化要素，行上 `metric_id` 仍是已有的 `M_POLICY_TEXT_PARSE`。该函数插入前清空整表，请求调用会连带清掉条款行。已签收的评价 226 已按同一约束只读这张表的 `summary`，且不建 `gapfill_policy_eval_summary`。237 仍只读，取列扩到 `title / summary / auto_tags / structured_elements`，并排除条款行；不另造一套解析，不把缺维改建成文本解析缺项行。第 11.2 节仿真组清单里的「文本解析」因此不灌 | 一致。符合第 11 节。`POL-L2-DS12-SIM-GAPFILL-L01` 开工时不灌文本解析行 |
| 238、239、241、242 读 `gapfill_policy_sim_result`，按种类分开。240 不设资源，只消费第 7 项子图 | 第 2 节：重点、影响范围、路径环节、解读段落四种行同表不同种类。一次 `jobs` 只带一种类。无行则该区空，接口不写死重点、范围、时间表或报告。240 无种类、无资源；页面消费政策子图（`E-E7-POLICY-M1-L02`），不建查图任务，不重画查图时序。调用链 6.4 与契约「240 不设资源」同向 | 一致 |
| 与 EST 共用一条 `simulation/jobs`。不重复实现 232–236。不改 stakeholder 表的灌数内容 | 第 0 节与第 2 节：推演页仍是 `POST /display/v1/policy/simulation/jobs`，不产生第二套资源。232–236 的种类由 `POL-L2-DS12-EST-ARCH` 在同一条资源上分发，本叶不实现、不改挂。235 多维评估行、236 参与意见行不在本叶组。`gapfill_policy_sim_stakeholder` 的灌数内容不改。灌数单对文本解析以外的已定内容仍照灌，其中 235、236 的内容不由本叶改写 | 一致 |
| 本叶缺项行 `metric_id` 留空。不把 `M_POLICY_SIMULATE` 挂到 235–242。不挂布局推荐、焦点指数、015。不新造 `metric_id`，不改 D4。不进异步白名单 | 238、239、241、242 的行上 `metric_id` 留空。第 6 节点名排除：推演键只挂 EST 已裁定的 232–234 预测行；`M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT` 不进本叶；`M_POLICY_FOCUS_INDEX` 不挂 238；`M_POLICY_DS_11_POLICY_EVAL_015` 不挂 241。237 沿用解析行上已有的 `M_POLICY_TEXT_PARSE`，不改、不新造。D4 保持 mock。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。`PolicyAnalysisTypes` 与 `JOB_SUB_TYPES` 不加新键；评价 226 已有的 `policy_text_parse` 保持原状。五类读面不进 `gkxlumen-topic-async-service` | 一致 |
| 调研仍写 501 | `survey/DS-12.md` 对 237–239、241、242 仍判 501，240 仍判跨项索引。说明书第 2 节、调用链第 3 节、契约 `simulation/jobs` 行仍写未注册则空。稿第 7 节写明会签前不改调研、说明书、指标与 501、契约输入清单。本叶可实现链路是读表，无行则该区空，不用 501 充当功能，也不改那些上游文件 | 一致。不构成不同意 |

## 路径、表、sub_type

| 序号 | 公开路径 | 表 | sub_type |
|---|---|---|---|
| 237 | `POST /display/v1/policy/simulation/jobs` | 已有 `ads.policy_text_parse` 的解析行（`structured_elements` 不含 `"clauses"` 的行）。不建、不灌文本解析缺项行 | 无。不进 `PolicyAnalysisTypes`，不进 `JOB_SUB_TYPES`。请求种类：文本解析。同步读，不建任务 |
| 238 | 同上 | `gkxlumenx_gapfill.gapfill_policy_sim_result` 的重点行。`metric_id` 留空 | 无。请求种类：重点可视化。同步读，不建任务 |
| 239 | 同上 | 同表的影响范围行。`metric_id` 留空 | 无。请求种类：影响范围。同步读，不建任务 |
| 240 | 不设资源 | 不建表。消费第 7 项政策子图 | 无。不进 `simulation/jobs`，不新建查图任务 |
| 241 | `POST /display/v1/policy/simulation/jobs` | 同表的路径环节行。`metric_id` 留空 | 无。请求种类：路径预测。同步读，不建任务 |
| 242 | 同上 | 同表的解读段落行。`metric_id` 留空 | 无。请求种类：解读报告。同步读，不建任务 |

237、238、239、241、242 的内部跳是：浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element` 只读。237 读 `ads.policy_text_parse`。238、239、241、242 读 `gkxlumenx_gapfill.gapfill_policy_sim_result`。不进入 `gkxlumen-topic-async-service`，不进入 Python `/internal/*`。

240 不走上述 `jobs`。页面消费已有第 7 项子图，Java 不写 nGQL。

EST 的 232–234 仍读 `gapfill_policy_sim_forecast`，235 仍读本表的多维评估行，236 仍读 `gapfill_policy_sim_stakeholder`。三条都在同一条 `simulation/jobs` 上按种类分发。本叶不改这五条的读法，也不改 236 的灌数内容。

评价 226 的异步键仍是 `policy_text_parse`，只读同表 `summary`，请求不跑 `polan.text.parse.run`。本叶不改那个键，也不把 237 再挂进白名单。

说明书第 11.2 节仿真组要灌的是多维评估、文本解析、重点、影响范围、路径、解读正文，以及参与意见。本叶只拿掉「文本解析」这一行。重点、影响范围、路径、解读仍灌入 `gapfill_policy_sim_result`。235、236 的灌数内容保持 EST 与第 11.2 节已写的范围，本叶不改写。

调用链第 3 节仍写整页推演在 `M_POLICY_SIMULATE` 未注册时 501。本叶读表，无行则空，不用 501 充当功能。本页不改写调用链文件。

`POL-L2-DS12-SIM-GAPFILL-L01` 的执行人是 `data-agent`，监管 `human:淮政玮`。本叶不执行灌数。查询请求不灌数。D4 保持 mock。该单开工时不灌文本解析行。

## 铁律

1. 算法只在 Python。本六叶的请求不跑解析、不生成重点、影响范围、路径或解读。Java 不写 nGQL。`gkxlumen-display` 不直连库，不直连 Python。
2. 调用链是浏览器 → `/display/v1/policy/**` → Java → `gkxlumen-element` 只读。展示不打 `/v1/policy/text/parse`，不打专题 URL，不调用 `demo-*`。
3. 237 只读已有 `ads.policy_text_parse`。请求不调用 `polan.text.parse.run`。不建文本解析缺项行。灌数单开工时不灌文本解析行。
4. 238、239、241、242 只读 `gkxlumenx_gapfill.gapfill_policy_sim_result`，按种类分开。240 不设资源，只消费第 7 项子图。
5. 与 EST 共用一条 `simulation/jobs`。不重复实现 232–236。不改 `gapfill_policy_sim_stakeholder` 的灌数内容。
6. 本叶缺项行 `metric_id` 留空。不把 `M_POLICY_SIMULATE` 挂到 235–242。不挂布局推荐、焦点指数、015。不新造 `metric_id`，不改 D4。不进异步白名单。
7. 接口不直接返回写死的解析、重点、范围、路径或报告。调研、说明书、调用链、契约里仍写的 501，会签前不改，不构成不同意。

## 签收边界

本页不把任务标 done。签收仍由 human:淮政玮 做。同意会签不是签收。

## 第二轮（2026-11-05 返工后）

- 角色：`agent:arch-agent`
- 日期：2026-11-05
- 监管：`human:淮政玮`
- 对象：返工后的 `POL-L2-DS12-SIM-ARCH`。只核第 7、9 节的表张数与 235/236 灌数归属有没有改掉第一轮已同意的读法。本页不改那份架构，不改 `POL-L2-DS12-EST-ARCH`，不改代码，不改 task-registry
- 对照：第一轮已同意的读法；`POL-L2-DS12-EST-ARCH` 第 9 节（235/236 灌数由 SIM 组灌数单负责）
- 强度：ponytail off

### 结论

同意会签

### 核对

| 项 | 返工后的架构稿 | 判定 |
|---|---|---|
| 237 仍读 `ads.policy_text_parse`。请求不跑 `polan.text.parse.run`。文本解析不灌缺项行 | 第 1.4、2、5.1、8 节未改：element 只读已落库解析行，请求不调用 `run()`。第 9 节仍写 237 不灌缺项行，文本解析行不灌，灌数单 DoD 的「文本解析」不灌。第 7、9 节没有把 237 改成读缺项表，也没有把 `run()` 放进请求 | 一致 |
| 238、239、241、242 仍读 `gapfill_policy_sim_result`。240 仍不设资源 | 第 2、5.2–5.5、8 节未改：四种仍只读这张表的对应种类行。第 5.6、2、8 节：240 不设资源，只消费第 7 项子图。第 7、9 节把本叶四种放进第一张 `gapfill_policy_sim_result`，没有改到 `gapfill_policy_sim_stakeholder`，也没有给 240 加表 | 一致 |
| 与 EST 共用 `simulation/jobs`。不重复实现 232–236 的读法 | 第 0、2 节未改：仍是同一条 `POST /display/v1/policy/simulation/jobs`；232–236 由 EST-ARCH 分发，本叶不实现、不改挂。第 6 节仍写不重复实现。第 9 节写 235/236 的读法由 EST-ARCH 定，236 指到 EST-ARCH §5.5，本叶不另写读法 | 一致 |
| 第 7 节与第 9 节都写明两张表：`gapfill_policy_sim_result` 与 `gapfill_policy_sim_stakeholder`。235 进 result，236 进 stakeholder。灌数由 `POL-L2-DS12-SIM-GAPFILL-L01`。行内容口径不在本叶改写 | 第 7 节点名这两张，本叶四种进第一张，235 的多维评估行也进第一张，236 的参与意见行进第二张，并写不把两张收成一张。第 9 节同样两张；235 灌进 `gapfill_policy_sim_result`，236 灌进 `gapfill_policy_sim_stakeholder`；灌数由 `POL-L2-DS12-SIM-GAPFILL-L01`，与 EST 第 9 节「灌数由 SIM 组负责」同向；写明本叶不改行内容口径，不改这两行已经写明的行内容。两节不再一张、两张互报 | 一致 |
| 浏览器仍只打 `/display/v1/policy/**`。不进异步。不新造 `metric_id` | 第 1.3 节仍写浏览器只打该前缀。第 7 节仍写不改打专题 URL 或 `/v1/**`，不进 `PolicyAnalysisTypes`，不进 async-service，不新造 `metric_id`。第 2、6 节：缺项读面不进异步，不加 Job 键。第 9 节：238/239/241/242 的 `metric_id` 留空；237 沿用已有 `M_POLICY_TEXT_PARSE` | 一致 |

### 签收边界

本页不把任务标 done。签收仍由 human:淮政玮 做。同意会签不是签收。第一轮原文保留。

## 第三轮（2026-11-05 条款读法）

- 角色：`agent:arch-agent`
- 日期：2026-11-05
- 监管：`human:淮政玮`
- 对象：当前 `POL-L2-DS12-SIM-ARCH`。只核 237 的条款读法是否已从「不含 `clauses` 键的行才读」改为「同一行仍读，返回时去掉这两个键，条款树不进报告」。本页不改那份架构，不改任务状态，不改代码
- 对照：`lumen-algo-py` `vendor/entan-py/polan/clause_job.py` 的 `_write_default`。已有 `policy_id` 执行 `UPDATE`，把 `clauses` 与 `clause_meta` 写进同一条 `structured_elements`
- 强度：ponytail off

### 结论

同意会签

### 核对

| 项 | 当前架构稿 | 判定 |
|---|---|---|
| 状态行 | 同日按 `clause_job._write_default` 把 §1.4 的条款读法改为：同一 `policy_id` 仍读，返回时去掉 `clauses` 与 `clause_meta` | 已改 |
| §1.4 条款隔离 | 条款批次更新同一条解析行，不另插条款行。展示 237 仍读该行的标题、摘要、标签和其余要素。返回 `structured_elements` 时去掉 `clauses` 与 `clause_meta`，条款树不进入解析报告。不因行内有这两个键整行丢弃 | 已改。不再要求整行丢弃 |
| 第 2 节 237 | element 只读 `ads.policy_text_parse` 的该政策解析行。返回时去掉 `clauses`、`clause_meta`，不整行丢弃 | 已改 |
| §5.1 | 按 `policy_id` 读已有解析行。返回时去掉 `structured_elements` 里的 `clauses`、`clause_meta`（§1.4）。不整行丢弃 | 已改 |
| 与 `_write_default` | 已有 `policy_id` 是 `UPDATE`，两键进同一条 `structured_elements`，不另插一行 | 同向。同一行仍读，返回时去键，条款树不进报告 |

### 签收边界

本页不把任务标 done。签收仍由 human:淮政玮 做。同意会签不是签收。第一轮、第二轮原文保留。
