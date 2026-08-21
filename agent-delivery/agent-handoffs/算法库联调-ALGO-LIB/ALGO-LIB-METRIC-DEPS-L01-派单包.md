# 派单包 · ALGO-LIB-METRIC-DEPS-L01

> **状态**：ready · **Agent**：`algorithm-agent` · **supervised_by**：`human:唐绍祖`  
> **仓**：`gkx-orchestration` · **结果目录**：`agent-delivery/metrics/algo-results/`（handoff + 表；不要写 agent-handoffs）  
> **生产派单说明（贴 /goal）**：[`给人说明-ALGO-LIB-METRIC-DEPS-L01-2026-08-21.md`](./给人说明-ALGO-LIB-METRIC-DEPS-L01-2026-08-21.md)  
> **派单备注（监管人必达）**：**必须使用 loop 工程**，禁止一个提示词做整体任务。按八维/层拆会话或分块推进，每块有独立产出再汇总。本备注不要求派单人现在检查 loop 执行。

## 目标

**8/25 前**交出三方 ODS **不满足**缺口清单。手段：双表 + 投影 `*-ods-gaps.yaml/.md`。`pending_ods` 不得混入「不满足」。Schema：`metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-schema.md`。

## 必读

1. `bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/README.md` 及八维目录  
2. `metrics/indicator-inventory/2026-08-20/` **只读**（5/8 维草稿）  
3. `metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-schema.md`  
4. `data-lineage-policy.md` §2.3 D3（ODS 枚举；本叶不改 seed）

## 禁止

- 改 seed、写代码、交混表 `*-deps.yaml`、凭 DWD 把 ODS 标 full  
- 把 `pending_ods` 写进「不满足」清单  
- 人才/科研机构/技术实现伪展开公式（表1 `third_party`，表2 仍列 inputs）  
- 派废作四叶

## `/goal`

```text
/goal
task: ALGO-LIB-METRIC-DEPS-L01
agent: algorithm-agent
supervised_by: human:唐绍祖
claim_type: pull
本叶为 definition/spike 文档分析，禁止用 ponytail 砍文档完整性；不写代码。

截止 2026-08-25：三方 ODS 不满足清单（confirmed none/partial）。
备注：必须使用 loop 工程，禁止一个提示词来做整体任务。
先读给人说明 + schema。交付双表 + ods-gaps.yaml/.md + summary + handoff。
```
