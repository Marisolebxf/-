# POL-L2-DS12-SIM-SIGNOFF-DATA · 政策效果推演 · 科技政策推演 · 数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-ARCH`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS12-SIM-ARCH` 第 7、9 节；`POL-L2-DS12-EST-ARCH` 第 0 节与第 9 节；`科技政策跟踪-系统详细设计说明书.md` 第 11 节与第 11.2 节「推演 · 仿真 235–242」；灌数单 `POL-L2-DS12-SIM-GAPFILL-L01`（任务注册表 `task-get`，状态 backlog）
- 范围：SRS 237–242
- 结论：**不同意会签**

本页只核对架构第 9 节的数据落点能否让灌数单确定该灌哪些行，以及 237 是否按说明书第 11 节收窄。下游 DATA 分册还没有，本页不定字段级 DDL。不改架构稿，不改任务状态，不建库，不灌数。

## 库表核对

| 口径 | 架构 | 判定 |
|---|---|---|
| 缺项库只有 `gkxlumenx_gapfill`。本叶组自用一张 `gapfill_policy_sim_result`。不拆多张。不写 ODS、DWD、ADS、供应方库 | 第 9 节写一张、不拆、不进 ODS / DWD / ADS、不写供应方库。第 7 节写「缺项行只进已定名的两张 SIM 组表」。灌数单 DoD 仍写建 `gapfill_policy_sim_result` 与 `gapfill_policy_sim_stakeholder` 两张 | 阻塞 |
| 237 不灌缺项行，读已有 `ads.policy_text_parse` | 第 5.1、9 节。请求不调用 `polan.text.parse.run`。行上已有 `metric_id=M_POLICY_TEXT_PARSE`，不改、不新造 | 符合。见下节 |
| 灌入种类只有重点、影响范围、路径环节、解读段落。242 不灌 PDF / Word。240 不建表 | 第 9 节表内四种与此相同。242 不灌 PDF / Word、不灌自定义格式。240 不设种类、不建表，只消费第 7 项子图。同节又写灌数单 DoD「文本解析」不灌、「其余照灌」 | 阻塞 |
| 235 多维评估行、236 参与意见行归 EST 半区，本叶不改它们的灌数内容 | 第 9 节把这两行划出本叶组，称归 EST 半区裁定的两张表，并写不改灌数内容。EST 第 9 节把 235 放进 `gapfill_policy_sim_result`、236 放进 `gapfill_policy_sim_stakeholder`，灌数与字段由 SIM 组两单负责 | 阻塞。与 EST 第 9 节冲突 |
| 缺项行 `metric_id` 留空。`fill_method=manual`。D4 保持 mock。不新造 `metric_id` | 第 9 节。238 / 239 / 241 / 242 行上 `metric_id` 留空。237 沿用已有 `M_POLICY_TEXT_PARSE`，不新造 | 一致 |
| 字段级 DDL 留给 `POL-L2-DS12-SIM-DATA`。灌数单未执行。本页不建库、不灌数。查询不灌数 | 第 9 节。灌数单状态 backlog，依赖本架构与 `POL-L2-DS12-SIM-DATA`。本叶不认领、不执行 | 一致 |

### 237 与说明书第 11 节

说明书第 11 节：已经有 ADS 表、也有可调用计算的，不新建表，接口再读；没有表、也没有算法的，才在 `gkxlumenx_gapfill` 建 `gapfill_` 表。第 11.1 节对已有 ADS 写「不另建表」。评价 READ-ARCH 已按这条总规则，对已落在 `ads.policy_text_parse` 的摘要不建 `gapfill_policy_eval_summary`。

237 的解析行已经由 `polan.text.parse.run` 落在 `ads.policy_text_parse`（标题、摘要、自动标签、结构化要素）。评价 226 只读同表。真查做得到，不启用缺项行退路。解析服务未注册为推演 Job，展示请求也不跑 `run()`（`run()` 会清空整表）。这与 226 的只读先例相同。第 11.2 节仿真组仍把「文本解析」写在要灌清单里，本叶按第 11 节总规则收窄，符合「已有产出不建缺项行」。

灌数单 `POL-L2-DS12-SIM-GAPFILL-L01` 的 DoD 写「独立脚本灌入多维评估、文本解析、重点、影响范围、路径、解读正文，以及参与意见」。其中「文本解析」一项，开工时不灌。这一项符合，不构成同意整单的理由。

### 阻塞

1. 第 7 节写缺项行进入已定名的两张 SIM 组表；第 9 节写本叶组只有一张 `gapfill_policy_sim_result`、不拆。灌数单 DoD 仍要建第二张 `gapfill_policy_sim_stakeholder`。一张与两张并存，灌数单无法确定建几张表。
2. EST 第 0 节与第 9 节：235 多维评估行进 `gapfill_policy_sim_result`，236 参与意见行进 `gapfill_policy_sim_stakeholder`，灌数与字段由 `POL-L2-DS12-SIM-DATA` 与 `POL-L2-DS12-SIM-GAPFILL-L01` 负责。本叶第 9 节把这两行划出本叶组、归 EST 半区，并写本叶不改灌数内容。与 EST 第 9 节冲突。
3. 第 9 节写该灌数单 DoD 的「文本解析」不灌、「其余照灌」。DoD 其余项含多维评估与参与意见。其余照灌会让本单改灌 235、236，超出本叶允许的四种：重点、影响范围、路径环节、解读段落。

须先对齐的句子（本页不代改）：

1. 第 7 节：「缺项行只进 `gkxlumenx_gapfill` 已定名的两张 SIM 组表。」
2. 第 9 节：「`gapfill_policy_sim_stakeholder`（236）归 EST 半区裁定，本叶不改它的灌数内容。」
3. 第 9 节：「该单 DoD 的「文本解析」一行不灌，其余照灌。」
4. 第 9 节：「235 多维评估行、236 参与意见行不在本叶组：归 EST 半区裁定的两张表。」

这四句与 EST 第 9 节不能同时成立。对齐之前，灌数单不能确定 235、236 由谁灌、灌进哪张表。242 不灌 PDF / Word、240 不建表，可以保留。237 不灌缺项行，可以保留。

## 不灌清单

| 种类 | 不灌 |
|---|---|
| 237 文本解析 | 不灌缺项行。不跑 `polan.text.parse.run`。不写 ODS、DWD、ADS 新表、供应方库。开工时不灌 DoD 里的「文本解析」 |
| 重点 | 焦点指数分、预渲染图片、解析标签改挂 |
| 影响范围 | 全国通用兜底行、地图文件、真推演结果 |
| 路径环节 | 布局推荐条数、流程执行记录、评价页 015 的方案路径 |
| 解读段落 | PDF / Word、自定义格式配置、核增研报正文 |
| 240 | 不建表。不灌子图，不建查图任务 |
| 235、236 | 本叶不改这两行的灌数内容。归属与 EST 第 9 节冲突，见上节阻塞，本页不代灌 |

`POL-L2-DS12-SIM-GAPFILL-L01` 未执行。本页不执行。查询请求不灌数。

## 签收边界

本页不把任务标 done，不改 `task-registry.yaml`，不建库，不灌数，不补 DDL。D4 保持 mock。签收仍由 human:淮政玮 做。第 7 节与第 9 节的表张数，以及 235、236 与 EST 第 9 节的灌数归属，改清之前，本页维持不同意会签。

## 第二轮（2026-11-05 返工后）

- 角色：`agent:data-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-ARCH` 第 7、9 节
- 对照：`POL-L2-DS12-EST-ARCH` 第 0 节与第 9 节；`科技政策跟踪-系统详细设计说明书.md` 第 11.2 节「推演 · 仿真 235–242」；灌数单 `POL-L2-DS12-SIM-GAPFILL-L01`（`task-get`，状态仍 backlog，本轮不改）
- 监管：`human:淮政玮`
- 本轮只核第一轮三条阻塞。第一轮原文保留。不定 DDL。不建库，不灌数。

### 结论

同意会签。

第一轮三条阻塞都已消掉。灌数单可以确定建两张表，235、236 由本单灌进哪张，要灌清单不再扩出这六项。

### 逐条

| 原阻塞 | 返工后 | 判定 |
|---|---|---|
| 第 7 节写两张，第 9 节写一张，灌数单定不下建几张 | 第 7 节：缺项行只进 `gkxlumenx_gapfill` 的 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder`，不收成一张，不另建第三张。第 9 节：SIM 组就是这两张，都在库 `gkxlumenx_gapfill`。灌数单 DoD 仍是建这两张 | 已消掉。能确定建 `gkxlumenx_gapfill.gapfill_policy_sim_result` 与 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` |
| 235、236 被划出本叶、归 EST 灌数，与 EST 第 9 节冲突 | 第 7 节：235 多维评估行进第一张，236 参与意见行进第二张。第 9 节：235 灌进 `gapfill_policy_sim_result`，236 灌进 `gapfill_policy_sim_stakeholder`；读法由 EST-ARCH 定（235 为 §5.4，236 为 §5.5），灌数由 `POL-L2-DS12-SIM-GAPFILL-L01` 执行，与 EST §9 一致。EST 第 0 节与第 9 节：这两行不在预估表，灌数由 SIM 灌数单负责 | 已消掉 |
| 「其余照灌」会灌出四种以外的行 | 第 9 节已删「其余照灌」。要灌的只有多维评估（235）、参与意见（236）、重点、影响范围、路径、解读正文。文本解析不灌。242 不灌 PDF / Word 等文件。第 7 节不另建第三张；240 不在要灌清单里，不建表。灌数单 DoD 仍写「文本解析」，第 9 节裁定开工时这一项不灌 | 已消掉。不构成再灌文本解析或文件 |

说明书第 11.2 节仿真组清单仍含「文本解析」，并写 240 只消费已有子图、不灌报告文件。本叶按第 11 节总规则收窄文本解析，与第一轮对这一项的判定相同。本页不改说明书，不改灌数单。

### 签收边界

本页不把任务标 done，不改任务状态，不建库，不灌数，不补 DDL。D4 保持 mock。签收只由 human:淮政玮 做。
