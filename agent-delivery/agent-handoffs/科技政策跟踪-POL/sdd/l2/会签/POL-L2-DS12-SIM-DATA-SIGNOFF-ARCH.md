# POL-L2-DS12-SIM-DATA-SIGNOFF-ARCH · 政策效果推演 · 科技政策推演 · 数据分册架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-DATA`
- 监管：`human:淮政玮`
- 强度：ponytail off
- 对照：`POL-L2-DS12-SIM-ARCH`（2026-11-05）§1.4 与第 5、7、9 节；`POL-L2-DS12-EST-ARCH` §5.4、§5.5。本页不重新设计，不改数据分册，不改那份架构，不改任务状态，不改代码
- 范围：SRS 序号 235–242 的数据落点

## 结论

不同意会签

两张缺项表都在库 `gkxlumenx_gapfill`，不并成一张，不加第三张。`gapfill_policy_sim_result` 覆盖 235 多维评估、238 重点、239 影响范围、241 路径环节、242 解读段落。`gapfill_policy_sim_stakeholder` 只放 236 参与意见。分册不写 `gapfill_policy_sim_forecast` 的列。237 不建 gapfill。240 无表。242 的内容列只有 `body_text`。`is_mock` 与已会签的 DS11 缺项表同款，不因此否决。235、236 的行内容仍是 EST §5.4、§5.5 已写的粒度。

阻塞：`lumen-algo-py/vendor/entan-py/polan/clause_job.py` 的 `_write_default` 在已有 `policy_id` 上执行 `UPDATE`，把 `clauses` 与 `clause_meta` 写进同一条 `structured_elements`。架构 §1.4 的语义是只读不含 `"clauses"` 键的行，判别写法才交给数据分册。分册第 9 节改成含该键的行仍读，返回时去掉这两个键。这改了语义。在 `POL-L2-DS12-SIM-ARCH` §1.4 改成这一读法并完成架构再会签之前，本数据分册不能会签。

## 核对

| 项 | 分册 | 判定 |
|---|---|---|
| 只两张缺项表，库 `gkxlumenx_gapfill` | 第 1 节：新定列的表只有 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder`。两张不并，不加第三张。不写 ODS、DWD、ADS，不写供应方库。237 对 `gkxlumenx_ads.policy_text_parse` 只读 | 一致。与架构第 7、9 节两张表、不收成一张一致 |
| result 覆盖 235、238、239、241、242 | 第 2 节 `row_kind` 只有 `多维评估`、`重点`、`影响范围`、`路径环节`、`解读段落`。236 的 `参与意见` 不进这张表 | 一致。与架构第 9 节「本叶四种进第一张，235 也进第一张」一致 |
| stakeholder 只放 236 | 第 8 节：`row_kind` 只有 `参与意见`。不放 235、237、238、239、240、241、242 | 一致。与架构第 9 节、EST §5.5 一致 |
| 不写 forecast 列 | 第 1、12 节：232–234 的列归 `POL-L2-DS12-EST-DATA`，不把预测行抄进这两张表。第 3 节多维评估不挂参数档、区域、政策类型。第 8 节意见表不加预测列 | 一致。预测列仍在 `gapfill_policy_sim_forecast` |
| 235 行内容沿 EST §5.4 | 第 3 节：一行一个维度，维度只用经济、社会、环境、创新。得分在 `score_value`，一句说明在 `score_text`。`metric_id` 留空。不挂 `M_POLICY_SIMULATE`，不挂 `M_POLICY_DEEP_168_1` | 一致 |
| 236 行内容沿 EST §5.5 | 第 8 节：一行一条意见。主体、渠道、意见正文、时间。请求不插入、不更新、不删除。页面新提交留在浏览器。`metric_id` 留空。不加 `policy_id` | 一致 |
| 237 不建 gapfill | 第 9、11 节：不另建表，不加列，不灌 `policy_text_parse`，不在两张 gapfill 表里加文本解析行。请求不调用 `polan.text.parse.run` | 一致。与架构第 9 节「文本解析不灌」一致 |
| 237 的条款读法 | 第 9 节：条款批次更新同一条解析行，返回时从 `structured_elements` 去掉 `clauses`、`clause_meta`。含 `clauses` 的行仍然读取标题、摘要、标签和其余要素 | 阻塞。架构 §1.4、§5.1 的语义是只取不含 `"clauses"` 键的行。判别写法由数据分册定，语义不由数据分册改。`_write_default` 对已有 `policy_id` 是 `UPDATE` 同一行。去键返回让含该键的行进入 237，与「不含该键的行才读」不同 |
| 240 无表 | 第 10 节：不设种类，不设表，不设列，不建 gapfill，不写 nGQL。消费第 7 项读图，指标仍是已有 `M_POLICY_RELATION_DEGREE` | 一致 |
| 242 只有正文列 | 第 7 节：`body_text` 是解读段落唯一的内容列。不设文件路径、对象键、文件名、文件字节。四个段落名在 `section_name` | 一致。与架构 §5.5「页面呈现正文，不灌文件」一致 |
| `is_mock` | 两张表都有 `is_mock` tinyint，每行必须为 1。D16 五列仍是 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。`fill_method` 固定 `manual`。六种业务行 `metric_id` 留空 | 一致。与 `POL-L2-DS11-PLAN-DATA` 缺项表同款。多这一列用来避免把缺项行读成已上线，不构成否决 |
| 读链与空态 | 235、236、237、238、239、241、242 走 `POST /display/v1/policy/simulation/jobs`。240 不走这条资源。`gkxlumen-display` 不直连库。element 按种类只读。无行返回空，不返回 501。查询不灌数 | 一致 |
| 不新造 `metric_id`，不改 D4 | 237 行上仍是 `M_POLICY_TEXT_PARSE`。240 仍是 `M_POLICY_RELATION_DEGREE`。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。D4 保持 mock | 一致 |

## 路径、表、种类

| 序号 | 表 | 种类 |
|---|---|---|
| 235 | `gkxlumenx_gapfill.gapfill_policy_sim_result` | `多维评估`。不按政策拣。`metric_id` 留空 |
| 236 | `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` | `参与意见`。不设 `policy_id`，不设预测列 |
| 237 | 已有 `gkxlumenx_ads.policy_text_parse`。不建 gapfill | 读法见上表阻塞行。分册写成返回时去掉 `clauses`、`clause_meta` |
| 238 | `gkxlumenx_gapfill.gapfill_policy_sim_result` | `重点`。按 `policy_id` 拣 |
| 239 | 同上 | `影响范围`。按 `policy_id` 拣 |
| 240 | 无 | 无。不走 `simulation/jobs` |
| 241 | `gkxlumenx_gapfill.gapfill_policy_sim_result` | `路径环节`。按 `policy_id` 拣 |
| 242 | 同上 | `解读段落`。内容列只有 `body_text` |

235–239、241、242 的内部跳是：浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element` 只读。不进入 `gkxlumen-topic-async-service`，不进入 Python `/internal/*`。237 读已有解析表，其余五行读上表对应的 gapfill 行。240 不走这条跳。

`POL-L2-DS12-SIM-GAPFILL-L01` 的执行人是 `data-agent`，监管 `human:淮政玮`。本页不执行灌数。文本解析不灌，这一条与架构第 9 节一致。查询请求不灌数。D4 保持 mock。

## 铁律

1. 算法只在 Python。本分册不让 Java 生成得分、意见、重点、影响、路径、解读正文，不跑 `polan.text.parse.run`，不写 nGQL。
2. 调用链是浏览器 → `/display/v1/policy/**` → Java → `gkxlumen-element` 只读。240 不走 `simulation/jobs`。
3. 缺项行只在 `gkxlumenx_gapfill` 的两张表。237 不建 gapfill。240 无表。242 不设文件路径列。
4. 235、236 的行内容沿 EST §5.4、§5.5。不把预测列写进这两张表。
5. `is_mock=1` 与 DS11 缺项表同款，D4 仍是 mock。不新造 `metric_id`。
6. 237 的条款隔离仍以架构 §1.4 为准：只读 `structured_elements` 不含 `"clauses"` 键的行。返回时去键改了这条语义，本页不同意。

## 签收边界

本页不把任务标 done。签收仍由 human:淮政玮 做。不同意会签。

## 第二轮（2026-11-05 架构改读法后）

- 角色：`agent:arch-agent`
- 日期：2026-11-05
- 监管：`human:淮政玮`
- 对象：`POL-L2-DS12-SIM-DATA` 第 9 节。对照同日已改的 `POL-L2-DS12-SIM-ARCH` 状态行、§1.4 条款隔离、第 2 节 237 行、§5.1 第一条。本页不改数据分册，不改架构稿，不改任务状态，不改代码
- 强度：ponytail off

### 结论

同意会签

### 核对

| 项 | 现行原文 | 判定 |
|---|---|---|
| 架构状态行 | 同一 `policy_id` 仍读，返回时去掉 `clauses` 与 `clause_meta` | 一致 |
| §1.4 条款隔离 | 条款批次更新同一条解析行，不另插条款行。展示 237 仍读该行的标题、摘要、标签和其余要素。返回 `structured_elements` 时去掉 `clauses` 与 `clause_meta`，条款树不进入解析报告。不因行内有这两个键整行丢弃 | 一致 |
| 第 2 节 237 行 | element 只读 `ads.policy_text_parse` 的该政策解析行。返回时去掉 `clauses`、`clause_meta`，不整行丢弃 | 一致 |
| §5.1 第一条 | 按 `policy_id` 读已有解析行。返回时去掉 `structured_elements` 里的 `clauses`、`clause_meta`。不整行丢弃 | 一致 |
| 数据分册第 9 节 | 按 `policy_id` 读取。返回 `structured_elements` 里除 `clauses`、`clause_meta` 以外的内容。含有 `clauses` 的行仍然读取标题、摘要、标签和其余要素。返回时去掉这两个键，条款树不进入解析报告 | 与上四句同向 |

### 签收边界

本页不把任务标 done。签收仍由 human:淮政玮 做。同意会签不是签收。第一轮原文保留。
