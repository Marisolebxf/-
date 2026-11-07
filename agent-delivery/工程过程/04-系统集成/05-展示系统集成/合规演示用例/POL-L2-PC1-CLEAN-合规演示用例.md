# POL-L2-PC1-CLEAN · 系统引用政策源数据清洗 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 政策数据治理
- 需规序号：602
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-08
- 调度核对：见文末

查库：`demo_gkxlumenx_dwd.policy_base_info`、`script_state`（当前 0 行）。展示读面 `GET /display/v1/policy/governance/results`。不重开 GDF。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 602 系统引用政策源数据清洗 | 政策数据治理 · 清洗 | 打开页（政策选择非强制） | 打开清洗 Tab | `GET /display/v1/policy/governance/results` | （无必选参数） | HTTP 成功非 501。`totalPolicyCount=20666`（`demo_gkxlumenx_dwd.policy_base_info` `is_deleted=0`）。`qualityAgg`/`qualityDetails` 空列表（`script_state` 0 行，诚实空，不造假分数） | 可演 |

## 一条主路径

1. 打开智能政策库构建 · 清洗 Tab。
2. 请求 `GET …/governance/results`。页眉库内政策数取自 `totalPolicyCount`；质量区无行则空，不显示伪分数。

## 调度核对

可演 1 行。可建演示样本循环。不派数据单。
