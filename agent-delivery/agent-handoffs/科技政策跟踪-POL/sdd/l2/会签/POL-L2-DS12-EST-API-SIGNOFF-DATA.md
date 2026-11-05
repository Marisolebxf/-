# POL-L2-DS12-EST-API-SIGNOFF-DATA · 政策效果推演 · 效果预估 · 后台接口设计数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-EST-API`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS12-EST-DATA` 第 1、2、6、7、8 节；`POL-L2-DS12-EST-ARCH` 第 5.4、5.5、9 节（只核对读路径）；`POL-L2-DS12-EST-API` 签收口径与第 1、2、4、6、7、8 节
- 范围：SRS 232–236
- 结论：**同意会签**

本页只核对接口分册的读表是否与数据分册一致：库 `gkxlumenx_gapfill` 与表名分开写；不把 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder` 的列写进接口分册当成 DDL；不灌文本解析；空态是空；235、236 的灌数仍归 `POL-L2-DS12-SIM-GAPFILL-L01`。不改接口分册，不改数据分册，不改架构稿，不改任务状态，不建库，不灌数。

## 库表核对

| 口径 | 接口分册 | 判定 |
|---|---|---|
| 232–234 只读库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_forecast`。种类只有未出台仿真、新出台预测、区域空间。不另建表，不拆成三张 | 签收口径与第 1、2、3–5 节。写法是 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`，按种类拣行 | 一致。与 DATA 第 1、2 节同一库、同一张表、三个 `row_kind` |
| 库名与表名分开，不粘成一个标识 | 232–236 的读落点都是库名、点、表名。第 2 节另写「库只允许 `gkxlumenx_gapfill`」。不进 ODS、DWD、ADS，不写供应方库 | 一致。没有把库名和表名粘成 `gkxlumenx_gapfill_policy_sim_*` |
| 235 读 `gapfill_policy_sim_result` 的多维评估行，236 读 `gapfill_policy_sim_stakeholder` 的参与意见行。这两张的列不在接口分册里写成 DDL | 第 6、7 节只写一行里有什么，并写明字段名归 `POL-L2-DS12-SIM-DATA`。第 2 节写明 235、236 的字段级 DDL 由该数据分册定，本分册不写 DDL、不改行内容 | 一致。与 DATA 第 1 节末句、第 7 节：这两张的列归 `POL-L2-DS12-SIM-DATA`，数据分册不展开那两张表的列。接口分册没有列名、类型、空约束 |
| 不灌文本解析。233 不读 `ads.policy_text_parse`，不用解析结果顶替预测行 | 第 4、8、9 节：不调 `parse/jobs`，不调 `policy_text_parse`，无预测行不返回解析结果。237 的解析读法留给 `POL-L2-DS12-SIM-API`，本分册不改写、不灌 | 一致。DATA 第 4、7、8 节：解析行不复制进预估表，也不顶替预测行 |
| 空态是空。无行不写成 501。接口不直接返回写死的预测、得分或意见 | 第 8 节：五叶无行则空，HTTP 成功，不返回 501。查询不灌数。架构第 2 节「真推演」未注册时的 501 不挂这五叶 | 一致。DATA 第 1、6、8 节：空态是空，不写成 501，查询不插入行来凑数 |
| 232–234 灌数归 `POL-L2-DS12-EST-GAPFILL-L01`。235、236 灌数仍归 `POL-L2-DS12-SIM-GAPFILL-L01` | 文首与第 2、6、7 节。本分册不执行灌数 | 一致。DATA 第 1 节末句、第 6 节：235、236 的灌数见 `POL-L2-DS12-SIM-GAPFILL-L01`，本数据分册不执行 |
| 232–234 行上 `metric_id` 用已有 `M_POLICY_SIMULATE`。`fill_method=manual`。D4 保持 mock。不新造 `metric_id`。235、236 行上 `metric_id` 留空 | 第 2、4、5、6、7 节。不借用推演键填评估分。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开 | 一致。DATA 第 2 节三种行固定 `M_POLICY_SIMULATE`、`fill_method=manual`、`is_mock=1`。235、236 的列不在该数据分册 |

## 不灌清单

| 种类 | 不灌 |
|---|---|
| 未出台仿真 | 中台三条情景原文、弹性现算、用户模拟历史、布局推荐条数 |
| 新出台预测 | 文本解析行、顶替用的解析结果、政策正文 |
| 区域空间 | 全国通用兜底行、地图文件 |
| 235 | 不灌进 `gapfill_policy_sim_forecast`。不在接口分册写 `gapfill_policy_sim_result` 的列当 DDL。灌数仍归 `POL-L2-DS12-SIM-GAPFILL-L01` |
| 236 | 不灌进预估表。请求不插入、不更新、不删除。不在接口分册写 `gapfill_policy_sim_stakeholder` 的列当 DDL。灌数仍归 `POL-L2-DS12-SIM-GAPFILL-L01` |

`POL-L2-DS12-EST-GAPFILL-L01` 与 `POL-L2-DS12-SIM-GAPFILL-L01` 均未在本页执行。查询请求不灌数。

## 签收边界

本页不把任务标 done，不改 `task-registry.yaml`，不建库，不灌数，不补 DDL。D4 保持 mock。签收仍由 human:淮政玮 做。
