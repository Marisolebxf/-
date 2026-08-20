# 派单包 · TOPIC-METRIC-CLASSIFY-L01

> **状态**：backlog（等 `TOPIC-METRIC-INVENTORY-L01` done/签收后 unlock → ready）  
> **Agent**：`algorithm-agent` · **supervised_by**：`human:唐绍祖`  
> **依赖**：`TOPIC-METRIC-INVENTORY-L01`

## 1. 目标

对 L01 `inventory.yaml` 逐条分类，并给出：可直接统计的默认口径、需查文献的任务清单、我方/三方 owner 分割。

## 2. 分类枚举（只准一类）

`STAT` | `COMPUTE` | `MODEL` | `LITERATURE` | `THIRD_PARTY` | `NO_SOURCE`

## 3. 必读

- L01 产出目录 `metrics/indicator-inventory/2026-08-20/`
- `data/third-party-source/gkx-mysql-raw/SUPPLIER-WORK-CONSTRAINTS.md`（只消费 `dwd_*`）
- 对照勿伪闭合：`metric-spec-POLICY.yaml`、`metric-readiness-matrix-SVC/SYNTH.yaml`

## 4. 产出

同目录：`classify.yaml` · `stat-defaults.md` · `literature-tasks.md` · `owner-split.md`  
handoff：`TOPIC-METRIC-CLASSIFY-L01.md`

## 5. 禁止

COMPUTE 伪装 STAT；文献指数写成已有公式；改 seed 的 `mapping_status` 为 aligned；写生产代码。

## 6. `/goal`（unlock 后粘贴）

```text
/goal
task: TOPIC-METRIC-CLASSIFY-L01
agent: algorithm-agent
supervised_by: human:唐绍祖
强度：definition/spike，禁止砍文档完整性；不写代码。

先读本派单包 + metrics/indicator-inventory/2026-08-20/inventory.yaml + SUPPLIER-WORK-CONSTRAINTS.md
认领后：逐条分类 → classify.yaml / stat-defaults.md / literature-tasks.md / owner-split.md → handoff → review
```
