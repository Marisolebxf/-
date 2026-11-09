# POL-L2-PC1-CLEAN · 系统引用政策源数据清洗 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 政策数据治理
- 需规序号：602
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-08
- 调度核对：见文末

查库：`demo_gkxlumenx_dwd.policy_base_info`、`script_state`（2026-11-09 起 19 行清洗作业行，批次 `pc1-clean-20261109`）。展示读面 `GET /display/v1/policy/governance/results`（含 `policyOptions`）。不重开 GDF。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 602 系统引用政策源数据清洗 | 政策数据治理 · 清洗 | 政策选择（候选来自 `results.policyOptions`，非强制） | 打开清洗 Tab；可选定政策看其清洗明细 | `GET /display/v1/policy/governance/results` | 不带参数，或 `policyId=18319069` | HTTP 成功非 501。`totalPolicyCount>0`；`qualityAgg` 13 组非空（7 个清洗阶段 job × success/failed/skipped）；`qualityDetails` 可按 `policyId`/`status` 过滤（灌数批 `pc1-clean-20261109`，3 政策 × 7 job）；`policyOptions` 为后端候选列表 | 可演 |

## 一条主路径

1. 打开智能政策库构建 · 清洗 Tab。
2. 请求 `GET …/governance/results`。页眉库内政策数取自 `totalPolicyCount`；批次卡显示 7 个清洗阶段作业（状态成功/失败/部分）；口径文案「待追加 → 入仓 → 重算 10 步汇总」与算法中台一致，页面只读。
3. 政策选择器选定政策（如 `18319069`）后，质量明细按该政策过滤。

## 调度核对

可演 1 行。可建演示样本循环。数据已灌（2026-11-09 `POL-PC1-CASE-FILL-DATA`，demo 库 `script_state` 19 行）；前端已支持清洗 Tab 选政策与批次表（`POL-PC1-CASE-FILL-FE`，待人工确认推送）。
