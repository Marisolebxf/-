# POL-L2-DS12-SIM-METRIC-SIGNOFF-ARCH · 政策效果推演 · 科技政策推演 · 指标分册架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-METRIC`（2026-11-05）
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS12-SIM-ARCH`（2026-11-04 稿；2026-11-05 改正 §1.4：同一 `policy_id` 仍读，返回时去掉 `clauses` 与 `clause_meta`）。本页只核指标分册是否落在该架构内。不改分册，不改架构稿，不改任务状态
- 范围：SRS 序号 237–242 的指标挂接。只写本会签。强度 ponytail off

## 结论

同意会签

分册不新建 `metric_id`。`M_POLICY_SIMULATE` 只认不挂，归 232–234。237 保持 `M_POLICY_TEXT_PARSE`。240 的 `M_POLICY_RELATION_DEGREE` 留在第 7 项，无 HTTP。238、239、241、242 行上留空。D4 仍是 mock。不调用 `polan.text.parse.run`。237 的条款读法以改正后的 §1.4 为准：同一 `policy_id` 仍读，返回时去掉 `clauses` 与 `clause_meta`。旧的整行丢弃不作为否决。未见 metric MCP、改读 `sdd/指标与501.md`，不构成不同意。

## 核对

| 项 | 分册 | 对架构判定 |
|---|---|---|
| 不新建 `metric_id` | 第 1、2、10 节：不新注册。挂接表只有 237 已有的 `M_POLICY_TEXT_PARSE`。这一条之外不新造号 | 一致。与架构第 7 节「不新造 `metric_id`」一致 |
| `M_POLICY_SIMULATE` 只认不挂，归 232–234 | 第 1、2、8、9 节：推演页只认这一条。只挂 232–234，归 `POL-L2-DS12-EST-METRIC`。237–242 的行不写这个号。不读 `ads.policy_simulate`，不调用 `polan.text.simulate.run` | 一致。与架构第 1.3 节、第 6 节「推演键只挂 232–234」一致 |
| 237 保持 `M_POLICY_TEXT_PARSE` | 第 1、2、5 节：行上已有号不改、不新造。类型 MODEL。不把摘要升成第二指标。不把 `M_POLICY_DS_11_POLICY_EVAL_012` 改挂到 237 | 一致。与架构第 5.1 节「行上 `metric_id` 仍是已有的 `M_POLICY_TEXT_PARSE`」一致 |
| 240 的 `M_POLICY_RELATION_DEGREE` 留在第 7 项，无 HTTP | 第 1、7 节：不另造独立号，不设种类，没有 HTTP 资源。纸面号留在第 7 项。页面消费政策子图。Java 不写 nGQL，不建查图任务 | 一致。与架构第 2、5.6 节「不设种类、不设资源」一致 |
| 238、239、241、242 行上留空 | 第 1、6 节：不新注册，不挂 `M_POLICY_SIMULATE`，不把 237 的号指进这四叶。重点、影响范围、路径环节、解读段落四行的 `metric_id` 留空 | 一致。与架构第 5.2–5.5 节、第 9 节「行上 `metric_id` 留空」一致 |
| D4 仍是 mock | 第 4 节：`M_POLICY_TEXT_PARSE`、`M_POLICY_RELATION_DEGREE`、`M_POLICY_SIMULATE` 只转述 mock，不升 live。四叶无专属号，缺项行仍是 mock。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开 | 一致。与架构第 7、9 节「不改 D4，D4 保持 mock」一致 |
| 不调用 `parse.run` | 第 3、5、10 节：展示请求不调用 `polan.text.parse.run`。不把截取规则收成公式。不改 `parse.py`，不改 `cfg_model_registry.yaml`，不加 Job 键 | 一致。与架构第 1.4、第 6 节「展示请求不调用 `run()`」一致 |
| 237 条款读法 | 第 5 节：读 `ads.policy_text_parse` 的该政策解析行，返回标题、摘要、自动标签、结构化要素。条款判别写法交给 `POL-L2-DS12-SIM-DATA`。不用条款行顶替解析报告 | 一致。以架构 2026-11-05 改正后的 §1.4、第 2 节、第 5.1 节为准：同一 `policy_id` 仍读，返回时去掉 `clauses` 与 `clause_meta`，不因这两个键整行丢弃。旧的整行丢弃不作为否决 |
| 读表与调用链 | 237 读 `ads.policy_text_parse`，不灌缺项文本解析。238、239、241、242 读 `gkxlumenx_gapfill.gapfill_policy_sim_result`。240 不走 `simulation/jobs`。链路是浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element`。不进异步。判定列仍是 501 与跨项索引，分册不改那一列。无行则该区空，不用 501 充当功能 | 一致。与架构第 2、5、9 节同一分组 |
| 指标 MCP 回退 | 抬头写明未见 metric MCP，未调用 `metric-get` / `metric-query`，回退 `sdd/指标与501.md` §3。未填注册中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1、D2、D3 | 不构成不同意。分册没有把未查到的字段写成已查到 |

## 路径、表、sub_type

| 序号 | 公开路径 | 表 | sub_type |
|---|---|---|---|
| 237 | `POST /display/v1/policy/simulation/jobs` | `ads.policy_text_parse` 的该政策解析行。同一 `policy_id` 仍读，返回时去掉 `clauses` 与 `clause_meta`。`metric_id` 保持已有 `M_POLICY_TEXT_PARSE`。不灌缺项文本解析 | 无。不进 `PolicyAnalysisTypes`，不进 `JOB_SUB_TYPES`。请求种类：文本解析。同步读，不建任务。不调用 `polan.text.parse.run` |
| 238 | 同上 | `gkxlumenx_gapfill.gapfill_policy_sim_result` 的重点行。`metric_id` 留空 | 无。请求种类：重点可视化。同步读，不建任务 |
| 239 | 同上 | 同表的影响范围行。`metric_id` 留空 | 无。请求种类：影响范围。同步读，不建任务 |
| 240 | 无 | 不建表。`M_POLICY_RELATION_DEGREE` 留在第 7 项政策子图 | 无。不设 HTTP，不进 `simulation/jobs`，不新建查图任务 |
| 241 | `POST /display/v1/policy/simulation/jobs` | 同表的路径环节行。`metric_id` 留空 | 无。请求种类：路径预测。同步读，不建任务 |
| 242 | 同上 | 同表的解读段落行。`metric_id` 留空。不产生文件 | 无。请求种类：解读报告。同步读，不建任务 |

237、238、239、241、242 的结果跳是：浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element` → 上表对应的表。不进入 `gkxlumen-topic-async-service`，不进入 Python `/internal/*`，不调用 `polan.text.parse.run`。240 由页面消费第 7 项读图，不走这条资源。

`POL-L2-DS12-SIM-GAPFILL-L01` 不灌文本解析。238、239、241、242 的缺项行 `metric_id` 留空。分册不执行灌数。D4 保持 mock。

## 铁律

1. 算法只在 Python。本六叶没有新模型。不调用 `polan.text.parse.run`。Java 不写 nGQL，不生成重点、影响范围、路径或解读正文。
2. 调用链是浏览器 → `/display/v1/policy/simulation/jobs` → `gkxlumen-display` → `gkxlumen-element` 只读。展示不直连 Python，不直连库，不调用 `demo-*`。240 不设 HTTP。
3. 237 读 `ads.policy_text_parse`。同一 `policy_id` 仍读，返回时去掉 `clauses` 与 `clause_meta`。238、239、241、242 读 `gkxlumenx_gapfill.gapfill_policy_sim_result`。接口不直接返回写死的报告、重点、范围、路径或全文。
4. 五类读面共用已有 `simulation/jobs`，一次一种类。不进 `PolicyAnalysisTypes`，不进异步管道。
5. 不新建 `metric_id`。237 保持 `M_POLICY_TEXT_PARSE`。238、239、241、242 留空。D4 保持 mock。
6. `M_POLICY_SIMULATE` 只认不挂，归 232–234。`M_POLICY_RELATION_DEGREE` 留在第 7 项。
7. 未见 metric MCP 时改读 `指标与501.md`。这不构成不同意。判定列仍是 501 与跨项索引，分册不改那一列。

## 签收边界

本页不把任务标 done。签收仍由 human:淮政玮 做。同意会签不是签收。
