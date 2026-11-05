# POL-L2-DS12-SIM-DATA-SIGNOFF-DATA · 政策效果推演 · 科技政策推演 · 数据落点数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-DATA`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS12-SIM-ARCH` 第 7、9 节（行内容对照第 5.2–5.5 节；235、236 行内容对照 `POL-L2-DS12-EST-ARCH` §5.4、§5.5）；`POL-L2-DS11-PLAN-DATA` 的 `is_mock`；条款写入对照 `polan/clause_job.py` 的 `_write_default`（已有行是 `UPDATE` 同一行）
- 范围：两张缺项表的列是否盖住架构要的行内容；表张数；文本解析不灌；预测列；242；空态；库边界；条款判别
- 结论：**同意会签**

本页只核对 DATA 分册。不改 DATA 分册，不改架构稿，不改任务状态，不建库，不灌数，不写可执行 SQL。

## 库表核对

| 口径 | DATA 分册 | 判定 |
|---|---|---|
| 缺项表两张，都在 `gkxlumenx_gapfill`，表名 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder`。不并成一张，不加第三张 | 第 1、2、8、13 节。235、238、239、241、242 在第一张。236 只在第二张。240 不设表 | 一致。架构第 7、9 节同这两张，并写明不收成一张、不另建第三张 |
| 不写 ODS、DWD、ADS、供应方库 | 第 1、9、12、13 节。237 对 `gkxlumenx_ads.policy_text_parse` 只读，不加列，不灌 | 一致。缺项行只进上述两张 gapfill 表 |
| 不写 `gapfill_policy_sim_forecast` 的列，不把预测行抄进这两张表 | 第 1、3、12、13 节。235 不挂参数档、区域、政策类型 | 一致。232–234 的列留在 EST 数据分册 |
| 不灌文本解析 | 第 9、11、13 节。不建文本解析 gapfill 表，不把解析行写入两张缺项表，请求不调用 `polan.text.parse.run` | 一致。架构第 9 节：该灌数单 DoD 的「文本解析」开工时不灌 |
| 242 不设文件路径 | 第 2、7 节。`body_text` 是解读段落唯一内容列。不设文件路径、对象键、文件名、文件字节 | 一致。架构第 9 节不灌 PDF / Word、自定义格式、核增研报正文 |
| 空态是空 | 第 1、3–10、11 节。空表、无行、条件对不上返回空。不返回 501，不写示例行，不造兜底行 | 一致。查询不灌数 |
| 240 不建表 | 第 10 节。不把 `M_POLICY_RELATION_DEGREE` 写入两张缺项表 | 一致。架构第 7 节不建查图任务 |

## 列覆盖

架构要的行内容都能落在已有列上。列清单不是可执行 SQL。

| 种类 | 架构要的行内容 | DATA 分册列 | 判定 |
|---|---|---|---|
| 多维评估（235） | EST §5.4：一个维度的得分与说明。维度是经济、社会、环境、创新。进第一张。不改行内容 | `dimension_name`、`score_value`、`score_text`。`policy_id` 写 NULL。不设预测列 | 一致 |
| 重点（238） | 所属政策、组别（政策目标 / 支持领域 / 实施路径 / 资金安排）、标题、一句明细 | `policy_id`、`group_name`、`item_title`、`detail_text` | 一致 |
| 影响范围（239） | 所属政策、类别（受益对象 / 影响区域 / 影响行业）、名称、一句说明、时间变化、区域维度数据 | `policy_id`、`impact_kind`、`impact_name`、`impact_text`、`time_change_text`、`region_text`。`region_text` 是展示原文，不存地图文件 | 一致。按 `policy_id` 拣行，推演上下文落在所属政策上 |
| 路径环节（241） | 所属政策、五环节、时间安排、责任主体、一句说明 | `policy_id`、`stage_name`、`schedule_text`、`owner_name`、`stage_text` | 一致 |
| 解读段落（242） | 所属政策、四段（政策背景 / 主要内容 / 预期效果 / 实施建议）、正文 | `policy_id`、`section_name`、`body_text` | 一致 |
| 参与意见（236） | EST §5.5：主体（决策者、评估者、利益攸关方）、渠道（在线问卷、意见征集、专家评审）、意见正文、时间。进第二张。不加预测列 | `actor_role`、`channel_name`、`opinion_text`、`opinion_at`。不设 `policy_id`，不设汇总列 | 一致。`opinion_at` 与 `generated_at` 分列 |

`row_kind` 在结果表是五个值：`多维评估`、`重点`、`影响范围`、`路径环节`、`解读段落`。意见表只有 `参与意见`。`参与意见` 不写入结果表。

第 9 节「行要能按所属政策拣」落在重点、影响范围、路径环节、解读段落。这四类 `policy_id` 必填。235 按 EST §5.4 不挂到某一条政策，`policy_id` 留空。236 的行内容没有政策，意见表不设 `policy_id`。

## 条款判别

架构第 1.4 节：237 只取解析行，语义是 `structured_elements` 不含 `"clauses"` 键的行，判别写法由本分册定。第 5.1 节同时要求一次读取返回标题、摘要、自动标签、结构化要素，条款树不进解析报告。

`_write_default` 在该政策已有解析行时执行 `UPDATE`：把 `clauses` 和 `clause_meta` 写进同一行的 `structured_elements`，不另插一行。更新之后，这一行同时带着解析要素和条款键。

分册第 9 节按这个事实写判别：按 `policy_id` 读取该行，返回 `title`、`summary`、`auto_tags`，以及去掉 `clauses`、`clause_meta` 之后的 `structured_elements`。含有这两个键的行仍返回标题、摘要、标签和其余要素。没有该政策的行，报告空。不返回条款树顶替解析报告。

判定：一致。去键发生在返回的要素上。整行按「不含 `clauses`」丢掉，会把同一行上的标题、摘要、标签和其余要素一起丢掉，第 5.1 节要返回的内容就没了。分册保住这些字段，条款树不进入解析报告。不另建表，不写 `gkxlumenx_ads.policy_text_parse`，不灌文本解析缺项行。

## D16 与 `is_mock`

| 项 | DATA 分册 | 判定 |
|---|---|---|
| `metric_id` | 两张缺项表五种结果行和参与意见行都写 NULL，不写空字符串。237 不改已有 `M_POLICY_TEXT_PARSE`。不新造 `metric_id` | 一致。架构第 9 节：238 / 239 / 241 / 242 留空。235、236 沿 EST 留空 |
| `gap_item` | 序号加叶子名，按 `row_kind` 固定。242 无单独文件行，`gap_item` 在解读段落行上 | 一致。架构第 9 节写「序号和叶子名」 |
| `fill_method` | 固定 `manual`，不设 `fill_model` | 一致 |
| `gapfill_batch_id`、`generated_at` | NOT NULL，由灌数单填写 | 一致 |
| `is_mock` | 两张表都是 NOT NULL，每行必须为 1。D4 仍是 mock | 一致。与 `POL-L2-DS11-PLAN-DATA` 第 2 节同一句。架构第 9 节未单列此列。本页不因多了 `is_mock=1` 否决 |

D4 保持 mock。`GDF-POLICY-MOCK-GATE-L01` 在分册里仍是 blocked。本页不把它写成已解开。

## 不灌清单

| 种类 | 不灌 |
|---|---|
| 多维评估 | 参数档、GDP、就业率、预测曲线、推演键 |
| 参与意见 | 页面当场提交的新意见、受众问卷、方案意见 |
| 重点 | 焦点指数、预渲染图片、解析标签 |
| 影响范围 | 全国兜底行、地图文件、234 的空间预测行 |
| 路径环节 | 布局推荐条数、流程执行记录、评价页 229 的方案路径 |
| 解读段落 | PDF、Word、文件路径、自定义格式、核增研报正文 |
| 文本解析 | 不灌。不写 `gkxlumenx_ads.policy_text_parse`，不在两张 gapfill 表里加文本解析行 |
| 240 | 不灌。不建表 |

`POL-L2-DS12-SIM-GAPFILL-L01` 分册记为 backlog。本页不执行。查询请求不灌数。

## 观察（不构成不同意）

条款任务在库里还没有该政策的解析行时会插入一行，插入行的 `structured_elements` 只有条款两键。分册对「有行」一律去键后返回，这支会带回标题和截短摘要，要素为空。主路径仍是更新已有解析行。分册没有为这支另建表，也没有把文本解析灌进 gapfill。本页不把这支写成阻塞。

## 签收边界

本页不把任务标 done，不改任务状态，不改 `task-registry.yaml`，不改 DATA 分册，不改架构稿，不建库，不灌数，不补可执行 SQL。D4 保持 mock。签收仍由 human:淮政玮 做。
