# POL-L2-DS11-VIZ-API-SIGNOFF-DATA · 政策分析评价 · 政策分析报告可视化呈现 · 数据会签（API 分册）

- 角色：`agent:data-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-VIZ-API`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS11-VIZ-ARCH` 第 5、9 节；`POL-L2-DS11-VIZ-DATA`；`POL-L2-DS11-READ-ARCH` 里壳表只服务 224、225 的句子
- 范围：SRS 219–222 的数据落点核对。接口路径、参数名、空态 HTTP 语义不在本页复核范围
- 结论：**同意会签**

本页只从数据角色核对 API 分册的读法是否落在正确的库表上。不改 API 分册，不改架构稿，不改任务状态，不建库，不灌数。

## 核对表

| 口径 | API 分册原文落点 | 判定 |
|---|---|---|
| 接口只读表，查询不灌数 | 第 1 节「查询只读。查询请求不灌数。表里没有行就返回空。接口不直接返回写死的 mock」。第 3、4、6 节各写「建表和灌数不在本分册」「查询请求不灌数」。第 9 节「不建立、不灌表。查询不灌数」 | 一致 |
| 219 读表名与 DATA 分册一致 | 第 1、2、3 节：`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_trend`。与 `POL-L2-DS11-VIZ-DATA` 第 2 节表名、库名一致 | 一致 |
| 220 读表名与 DATA 分册一致 | 第 1、2、4 节：只读 `gkxlumenx_gapfill.gapfill_policy_eval_partition`。与 DATA 分册第 3 节一致。与 219 分成两次请求，一次不同时读两张表 | 一致 |
| 222 读表名与 DATA 分册一致 | 第 1、2、6 节：`shells` 种类为模板选用时只读 `gkxlumenx_gapfill.gapfill_policy_eval_template`。与 DATA 分册第 5 节一致 | 一致 |
| 222 不读解读壳表 | 第 6 节「不读 `gapfill_policy_eval_shell`」。与 READ-ARCH 第 7、8 节「shell 只服务 224、225，序号 222 的模板选用不在该叶灌入」口径一致 | 一致 |
| 221 不触发数据落点 | 第 5 节不设 `/display/v1/policy` 资源，只消费第 7 项已有子图，不灌弦线矩阵和演示路径进缺项表。与架构第 5.3、9 节一致 | 一致 |
| 条件值只来自表行 | 第 3 节 `metric`「只接受该缺项表里已有的名称」；第 4 节 `allocation`「只接受缺项表里已有的值」；第 6 节 `template`、`period`「只接受该缺项表/选用行上已有的」 | 一致。不在接口侧另编词表 |
| 灌数单归属 | 第 3、6 节点名灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01` 覆盖三张表，且不是请求处理。与架构第 9 节末段一致 | 一致 |
| 不写 ODS、DWD、ADS、供应方库 | 第 3、4、6 节均写明。与架构第 5.1、5.2、5.4、7 节一致 | 一致 |
| mock 只能先落表再被读出 | 第 7 节「mock 若存在，只能先由灌数单落进表，再被查询读出来」 | 一致。符合可实现签收标准 |

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。
