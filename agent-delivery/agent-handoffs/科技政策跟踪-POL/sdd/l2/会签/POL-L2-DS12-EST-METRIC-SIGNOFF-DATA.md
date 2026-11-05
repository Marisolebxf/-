# POL-L2-DS12-EST-METRIC-SIGNOFF-DATA · 政策效果推演 · 效果预估 · 后台指标设计数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-EST-METRIC`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS12-EST-ARCH` 第 5.1–5.5、9 节；`POL-L2-DS12-EST-DATA` 第 1、2、4、6、7 节
- 范围：SRS 232–236 的指标挂表
- 结论：**同意会签**

本页只核对指标挂表是否一致：232–234 读哪张表、行上 `metric_id` 是哪一个号；235、236 读哪张表、行上是否留空；解析行有没有被当成预测；D4 是否仍为 mock。不改三份分册，不改任务状态，不建库，不灌数。

## 指标挂表核对

| 口径 | 三册 | 判定 |
|---|---|---|
| 232–234 读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast` | METRIC 第 1、3、5 节：未出台仿真、新出台预测、区域空间三行都读这一张。DATA 第 1、2 节：同一张表，`row_kind` 只有这三种。ARCH 第 5.1–5.3、9 节同表 | 一致 |
| 232–234 行上 `metric_id` 用已有 `M_POLICY_SIMULATE` | METRIC 第 2、5 节：三行都用这个已有号，不另起三条。DATA 第 2 节：三种行固定此号，不写空，不写别的指标。ARCH 第 5.1–5.3、9 节：三种均用推演键 | 一致 |
| 235 读 `gkxlumenx_gapfill.gapfill_policy_sim_result`，行上 `metric_id` 留空 | METRIC 第 1、6.1 节：多维评估行留空，不挂 `M_POLICY_SIMULATE`。DATA 第 1 节末句：列归这张表，预估表不放 235 行。ARCH 第 5.4 节：留空，不借用推演键填评估分 | 一致 |
| 236 读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`，行上 `metric_id` 留空 | METRIC 第 1、6.2 节：参与意见行留空，不挂 `M_POLICY_SIMULATE`。DATA 第 1 节末句：列归这张表。ARCH 第 5.5 节：留空，不新造 | 一致 |
| 不把解析行当预测 | METRIC 第 5.2、7 节：233 不调 `parse/jobs`，无行不返回解析结果顶替，不把 `M_POLICY_TEXT_PARSE` 顶替预测行。DATA 第 1、2、4、6、7 节：`ads.policy_text_parse` 不进预估表，一行不是文本解析记录，`similar_basis_text` 不是解析行，不灌独立文本解析行。ARCH 第 5.2、9 节：不另开解析通道，不灌独立文本解析行 | 一致 |
| D4 仍 mock | METRIC 第 1、4 节：`M_POLICY_SIMULATE` 保持 mock，不升 live；235、236 没有专属号，缺项行仍是 mock。DATA 第 2 节：`is_mock=1`，D4 不改绿。ARCH 第 7、9 节：不改 D4 | 一致 |
| 不新造 `metric_id` | 三册同句。235、236 指不到就留空 | 一致 |

## 不灌清单

| 种类 | 不灌 |
|---|---|
| 未出台仿真 | 解析行。不把 `ads.policy_text_parse` 复制进 `gapfill_policy_sim_forecast` |
| 新出台预测 | 独立文本解析行、顶替用的解析结果。不把 `M_POLICY_TEXT_PARSE` 写入行上。`similar_basis_text` 只是行内说明 |
| 区域空间 | 解析行。不把解析结果写成空间结果 |
| 235 | 不写入预估表。不把 `M_POLICY_SIMULATE` 写入多维评估行 |
| 236 | 不写入预估表。不把 `M_POLICY_SIMULATE` 写入参与意见行 |

查询请求不灌数。本页不执行 `POL-L2-DS12-EST-GAPFILL-L01`，也不执行 `POL-L2-DS12-SIM-GAPFILL-L01`。

## 签收边界

本页不把任务标 done，不改 `task-registry.yaml`，不建库，不灌数，不补 DDL。D4 保持 mock。签收仍由 human:淮政玮 做。
