# POL-L2-DS12-SIM-METRIC-SIGNOFF-DATA · 政策效果推演 · 科技政策推演 · 后台指标设计数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-METRIC`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS12-SIM-METRIC` 第 1、5、6、7 节；`POL-L2-DS12-SIM-DATA` 第 1、2、9、10、11 节；`POL-L2-DS12-SIM-ARCH` 第 5、9 节
- 范围：SRS 237–242
- 结论：**同意会签**

本页只核对指标分册的读表与行上 `metric_id` 是否与数据分册、架构第 5、9 节一致。不改三份分册，不改任务状态，不建库，不灌数，不新造 `metric_id`。

## 库表核对

| 口径 | 指标分册 | 判定 |
|---|---|---|
| 237 读已有解析表，行上保持 `M_POLICY_TEXT_PARSE` | 第 1、5 节：展示读 `ads.policy_text_parse` 的解析行，行上已有号不改、不新造。DATA 第 9 节：`gkxlumenx_ads.policy_text_parse` 就是这一张，行上 `metric_id` 仍是该号。ARCH 第 5.1 节同句 | 一致 |
| 238、239、241、242 读 `gapfill_policy_sim_result`，行上 `metric_id` 留空 | 第 1、6 节：四叶读同一张缺项表，行上留空，不挂 `M_POLICY_SIMULATE`，不把 237 的号指进来。DATA 第 2 节：这四种行的 `metric_id` 写 NULL，不写空字符串。ARCH 第 5.2–5.5、9 节同句 | 一致 |
| 240 无表 | 第 1、7 节：不设种类，不设 HTTP 资源，不灌关联表。纸面号 `M_POLICY_RELATION_DEGREE` 留在第 7 项，不写进本叶资源。DATA 第 10 节：不设表、不设列。ARCH 第 5.6 节：不设种类、不设资源 | 一致 |
| 不灌文本解析 | 第 1、5、10 节：不灌缺项文本解析行，请求不调用 `polan.text.parse.run`。`POL-L2-DS12-SIM-GAPFILL-L01` 的「文本解析」按架构第 9 节不灌。DATA 第 9、11 节：不写解析表，不在两张 gapfill 表加文本解析行。ARCH 第 9 节同句 | 一致 |
| D4 仍是 mock | 第 1、4 节：`M_POLICY_TEXT_PARSE`、`M_POLICY_RELATION_DEGREE` 转述为 mock，不升 live。238、239、241、242 无专属号，缺项行仍是 mock。DATA 第 2 节：结果行 `is_mock=1`，D4 仍是 mock。ARCH 第 5、9 节：D4 保持 mock | 一致 |

条款键怎么从返回里拿掉，指标分册写明由 `POL-L2-DS12-SIM-DATA` 定。DATA 第 9 节仍读这张已有解析表，行上号不改。

## 不灌清单

| 种类 | 不灌 |
|---|---|
| 237 文本解析 | 不灌缺项行。不跑 `polan.text.parse.run`。不把解析行写入 `gapfill_policy_sim_result` |
| 238 重点 | 不挂 `M_POLICY_FOCUS_INDEX`。不把解析标签改挂成重点项 |
| 239 影响范围 | 不挂 `M_POLICY_SIMULATE`。不造全国通用兜底行 |
| 241 路径环节 | 不挂 `M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DS_11_POLICY_EVAL_015` |
| 242 解读段落 | 不产生文件。不灌 PDF、Word |
| 240 | 不建表。不把 `M_POLICY_RELATION_DEGREE` 写入 gapfill |

`POL-L2-DS12-SIM-GAPFILL-L01` 未执行。本页不执行。查询请求不灌数。

## 签收边界

本页不把任务标 done，不改 `task-registry.yaml`，不改三份分册，不建库，不灌数。D4 保持 mock。签收仍由 human:淮政玮 做。
