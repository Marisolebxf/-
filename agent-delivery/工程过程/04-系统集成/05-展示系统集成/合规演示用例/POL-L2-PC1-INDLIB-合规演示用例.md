# POL-L2-PC1-INDLIB · 规划指标库搭建 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 政策数据治理
- 需规序号：605
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-08
- 调度核对：见文末

查库：`gkxlumenx_gapfill.gapfill_policy_indicator_lib`（12 行，四维×3 政策，全 `is_mock=1`）。

展示读面：`GET /display/v1/policy/governance/indicator-library`。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 605 规划指标库搭建 | 政策数据治理 · 规划指标库搭建 | 政策 `18319069`；维度可不选（四闭集） | 打开指标库 Tab 并选定该政策 | `GET /display/v1/policy/governance/indicator-library` | `policyId=18319069` | records 4 行，维度恰为扶持力度/适用范围/实施时效/申请条件各 1；`metric_id` 空；`is_mock=1` | 可演 |

## 一条主路径

1. 打开规划指标库搭建 Tab。
2. 选政策 `18319069`。
3. 应看到该政策四维各一条；全部 Mock。

## 调度核对

可演 1 行。可建本二级演示样本循环。
