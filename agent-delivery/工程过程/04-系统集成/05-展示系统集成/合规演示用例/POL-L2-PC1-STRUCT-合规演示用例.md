# POL-L2-PC1-STRUCT · 政策库结构化 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 政策数据治理
- 需规序号：603
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-08
- 调度核对：见文末

查库：`demo_gkxlumenx_ads.policy_text_parse`、`demo_gkxlumenx_dwd.policy_base_info`。同资源 `GET /display/v1/policy/governance/results`。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 603 政策库结构化 | 政策数据治理 · 结构化 | 政策 `18319069` | 选定政策后读 results | `GET /display/v1/policy/governance/results` | `policyId=18319069` | `structure.structuredPolicyCount=1290`；`structure.coverageRate=0.0624`（1290/20666）；`structure.policySummary.policyId=18319069` 且 `hasClauses=true` | 可演 |

## 一条主路径

1. 打开结构化 Tab，选 `18319069`。
2. 请求带 `policyId`。摘要应显示已结构化；覆盖率来自 ADS/DWD 计数，不是写死百分比。

## 调度核对

可演 1 行。可建演示样本循环。
