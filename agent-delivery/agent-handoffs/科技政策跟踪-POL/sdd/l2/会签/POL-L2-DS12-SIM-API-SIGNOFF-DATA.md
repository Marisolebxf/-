# POL-L2-DS12-SIM-API-SIGNOFF-DATA · 政策效果推演 · 科技政策推演 · 数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-API`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS12-SIM-API` 第 1、3–8 节；`POL-L2-DS12-SIM-DATA` 第 2、4–7、9、10 节；`POL-L2-DS12-SIM-ARCH` §1.4；`lumen-algo-py` `vendor/entan-py/polan/clause_job.py` 的 `_write_default`
- 范围：SRS 237–242
- 结论：**不同意会签**

本页只核对接口读表是否与数据分册一致。不改接口分册，不改数据分册，不改架构稿，不改任务状态，不建库，不灌数。

## 库表核对

| 口径 | 接口分册 | 数据分册 | 判定 |
|---|---|---|---|
| 237 只读已有解析表。不灌 gapfill。查询不写这张表 | `ads.policy_text_parse` | `gkxlumenx_ads.policy_text_parse`。不加列。架构稿里的 `ads.policy_text_parse` 就是这一张 | 表一致 |
| 238 读结果表重点行 | `gkxlumenx_gapfill.gapfill_policy_sim_result` 的重点行 | `row_kind=重点`，再按 `policy_id` | 一致 |
| 239 读结果表影响范围行 | 同一张表的影响范围行，按政策拣 | `row_kind=影响范围`，再按 `policy_id` | 一致 |
| 241 读结果表路径环节行 | 同一张表的路径环节行 | `row_kind=路径环节`，再按 `policy_id` | 一致 |
| 242 读结果表解读段落行。不读文件 | 同一张表的解读段落行。页面呈现正文。不产生 PDF、Word。不写对象存储 | `row_kind=解读段落`。内容只在 `body_text`。不设文件路径、对象键、文件字节 | 一致 |
| 240 无表 | 无 HTTP 资源，无种类 | 不设表，不设列 | 一致 |
| 238、239、241、242 的 `metric_id` 留空。`fill_method=manual`。D4 保持 mock。237 行上仍是已有 `M_POLICY_TEXT_PARSE` | 第 2 节。不新造 `metric_id`。不改 D4 | 第 2、9 节。五种结果行 `metric_id` 留空。237 不改已有值 | 一致 |
| 237 读哪些行、返回的要素里留哪些键 | 第 3 节：`structured_elements` 含 `"clauses"` 键的行不返回。判别写法由数据分册定，本分册只定这个语义。返回整份 `structured_elements` | 第 9 节：含有 `clauses` 的行仍然读取。返回时去掉 `clauses` 与 `clause_meta` | 阻塞 |

## 条款行

架构 §1.4 定的语义是：237 只取 `structured_elements` 不含 `"clauses"` 键的行。判别写法交给数据分册，架构只定语义。

`_write_default` 先按 `policy_id` 读已有 `policy_text_parse`。行已存在时执行 `UPDATE`，把 `clauses` 和 `clause_meta` 写进同一条 `structured_elements`，不另插一行。条款批次跑完后，这条解析行含 `"clauses"` 键。

数据分册第 9 节写成：返回 `structured_elements` 里除 `clauses`、`clause_meta` 以外的内容；含有 `clauses` 的行仍然读取标题、摘要、标签和其余要素。这改的是读哪些行、返回什么，不是把「不含键才读」落成判别条件。

接口第 3 节仍按架构语义写「含 `"clauses"` 键的行不返回」，并称语义已定、判别写法交给数据分册。按这句，条款批次之后该政策的解析行整行不返回，标题、摘要、标签和其余要素一起空掉。数据分册第 9 节则仍返回这些要素。两册对不上。

### 阻塞

接口第 3 节「含 `"clauses"` 键的行不返回」与数据分册第 9 节「含有 `clauses` 的行仍然读取，返回时去掉 `clauses` 与 `clause_meta`」是两套读法。数据分册改了语义。对齐之前不同意会签。

## 签收边界

本页不把任务标 done，不改 `task-registry.yaml`，不建库，不灌数，不改分册。D4 保持 mock。签收仍由 human:淮政玮 做。第 3 节与数据分册第 9 节的条款读法对齐之前，本页维持不同意会签。

## 第二轮（2026-11-05 返工后）

- 角色：`agent:data-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-API` 第 3 节；第 9 节空态表 237 行
- 对照：`POL-L2-DS12-SIM-DATA` 第 9 节
- 监管：`human:淮政玮`
- 本轮只核第一轮的条款读法。第一轮原文保留。不改分册，不改任务状态。

### 结论

同意会签。

第一轮阻塞已消掉。同一 `policy_id` 仍读取，返回时去掉 `clauses` 与 `clause_meta`，不整行丢弃。与数据分册第 9 节一致。

### 逐条

| 原阻塞 | 返工后 | 判定 |
|---|---|---|
| 接口第 3 节写含 `"clauses"` 键的行不返回，整行丢弃 | 第 3 节：条款批次更新同一条 `policy_id`，把 `clauses`、`clause_meta` 写进同一份 `structured_elements`，不另插一行。含这两个键的行仍然读取。返回 `structured_elements` 时去掉这两个键。不因含 `clauses` 整行丢弃。空态句同样写不因行内有条款键整行丢弃 | 已消掉 |
| 空态表 237 行未写去掉键 | 第 9 节空态表 237 行：返回时去掉 `clauses` 与 `clause_meta`，不整行丢弃。当前稿第 8 节是 242，不改这条读法 | 已消掉 |
| 与数据分册第 9 节两套读法 | 数据分册第 9 节：按 `policy_id` 读取；返回 `structured_elements` 里除 `clauses`、`clause_meta` 以外的内容；含有 `clauses` 的行仍然读取标题、摘要、标签和其余要素 | 已消掉 |

### 签收边界

本页不把任务标 done，不改 `task-registry.yaml`，不建库，不灌数，不改分册。D4 保持 mock。签收仍由 human:淮政玮 做。
