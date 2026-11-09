# POL-L2-PC1-LINEAGE · 溯源索引构建 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 政策数据治理
- 需规序号：604
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-08
- 调度核对：见文末

查库时间：2026-11-08（`gkxlumenx_gapfill.gapfill_policy_lineage_index` apply 后）。主机 `10.50.11.76`。口令未写入本文件。

展示读面：`GET /display/v1/policy/governance/lineage-index` → element 只读 gapfill 表。原文条款行 `is_mock=0`（ADS 快照）；条款结论行 `is_mock=1`。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 604 溯源索引构建 | 政策数据治理 · 溯源索引构建 | 政策 `18319069`（科技部财政部关于调整国家科学技术奖奖金标准的通知） | 打开溯源 Tab 并选定该政策 | `GET /display/v1/policy/governance/lineage-index` | `policyId=18319069` | records **4** 行：原文条款 2（`二、`/`三、`，`is_mock=0`）+ 条款结论 2（`conc-award-raise`/`conc-award-start`，`is_mock=1`） | 可演 |

## 一条主路径

1. 打开智能政策库构建 → 溯源索引构建。
2. 政策选择器选 `18319069`。
3. 请求带 `policyId=18319069`。应看到原文条款与结论各至少两行；结论带 Mock 标记。

## 调度核对

可演 1 行。可建本二级演示样本循环。不派数据单（表已灌）。
