# POL-DISPLAY-SURVEY-PC-L01 · 科技政策跟踪调研 · 核增四页

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权。本叶只写分册与本 handoff，不改注册表 |

## 范围

核增四页合为一叶：政策数据治理（PC-1，`FE-POL-04A`，`US-DS-POL-07`，SRS 602–605）、智能政策拆解（PC-2，`FE-POL-05A`，`US-DS-POL-08`，SRS 606–609）、多维政策对比（PC-3，`FE-POL-06A`，`US-DS-POL-09`，SRS 610–613）、智能研报生成（PC-4，`FE-POL-07A`，`US-DS-POL-10`，SRS 614–618）。

查询走 task-registry 与 metric-registry。政策域 35 条。GDF 政策派单包只索引，不写成展示系统新任务。未写 API-POL，未改 WBS，未改业务仓，未把任务标 done。`E-E7-POLICY-M1-L06` 不作为实现路径。

## 产物路径

`agent-delivery/agent-handoffs/科技政策跟踪-POL/survey/PC.md`

## 四页三档计数

表内 17 行。治理页眉「库内政策数」可挂 `M_POLICY_TOTAL_COUNT`（STAT，D4=mock），不计入下表。

| 页 | 可接统计读面 | 501 | 跨项索引 |
|---|---|---|---|
| PC-1 政策数据治理 | 0 | 2 | 2 |
| PC-2 智能政策拆解 | 0 | 1 | 3 |
| PC-3 多维政策对比 | 0 | 4 | 0 |
| PC-4 智能研报生成 | 0 | 5 | 0 |
| 合计 | 0 | 12 | 5 |

## Ponytail

ponytail: off

定义调研，不缩文档。

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | green |

## 架构合规

- 调用链：本叶不写实现。展示对外仍只走 `/display/v1/policy/**`。
- D12：未改 `lumen-*` / `demo-*`。
- D9：可接统计读面在本四页表内为 0。已点名的误挂指标均 D4=mock，未写成已上线。
- 研报 Job 未注册，PC-4 五叶均为 501。
- 本叶不改图。`diagram_id`：无。

## CI/CD

文档叶。无 commit，无 pipeline，无部署。
