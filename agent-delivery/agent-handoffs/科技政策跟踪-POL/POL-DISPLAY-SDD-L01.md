# POL-DISPLAY-SDD-L01 · 科技政策跟踪系统详细设计说明书

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 详设三叶 handoff 齐后合成。不等签收 |

## Ponytail

ponytail: off

## 范围

合成调用链、指标与 501、契约输入清单。不写 OpenAPI 字段表，不改三叶正文，不改业务仓。

## 产物

`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md`

三叶：

- `POL-DISPLAY-SDD-CHAIN-L01`：同步读 ADS，Job 未注册则 501。`E-E7-POLICY-M1-L06` 不是展示实现路径。
- `POL-DISPLAY-SDD-METRIC-L01`：七页三档沿用调研。评价页 5 行交互壳并入 501。推演与布局推荐分键。
- `POL-DISPLAY-SDD-INPUT-L01`：25 条资源。全景 13、评价 3、推演 1、治理 3、拆解 2、对比 2、研报 1。

## 会签

架构、算法、数据、产品均未签。本单停在会签，不标 done。

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | green |

## 下游

契约单 `BE-POL-CONTRACT-01` 可读本说明书与契约输入清单。本单不替它写字段表，也不开工实现单。
