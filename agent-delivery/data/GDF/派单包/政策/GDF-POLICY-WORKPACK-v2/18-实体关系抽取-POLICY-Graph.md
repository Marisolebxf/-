# 18 — POLICY-Graph：实体与关系

> **读者**：GDF。抽取和写入关系在本包。读图、查图归第 07 项，不在这里配。  
> **不复制** `metrics/repro/` 里的图谱脚本。

## 1. 已经在配的

`12` 的 **POLICY-C1**（`scripts/policy_c1_industry.py`）就是产业节点落入 `policy_industry_rel` 的作业。继续按 `12` 和 `15` 跑。不要把 C1 改名为 MDC，也不要把它当成下面两条指标的脚本。

C2（条款结构化）仍按 `12` 跑。它不是 MDC 的全文模型，也不进 `17` 的第一批。

## 2. 还没有脚本、先不配

| 指标 | 要写的结果 | 本版 |
|---|---|---|
| `M_POLICY_GRAPH_106_1` 政策实体识别 | `gkxlumenx_ads.policy_entity`（及图上的实体） | 脚本未进包。任务 `GDF-POLICY-GRAPH-EXT-L01`。未完成前不要建作业 |
| `M_POLICY_GRAPH_107_1` 政策实体关系抽取 | `policy_graph_node` / `policy_graph_edge` | 同上 |

图上的实体和边属性：GDF 只触发图谱引擎 API，不写 nGQL，不直写图库。API 的字段契约未收进本包之前，不要配这条触发。

`M_POLICY_RELATION_DEGREE` 等边落地、并且 QPOL-03 签了之后才由 MDC 计算。不在 ODS 再平行建一张边表。

## 3. 不要做

- 不要把 C1 的产业关联表当成 106 / 107 的输出。
- 不要在 CDC / SeaTunnel 里另写一套实体或关系规则。
- 不要为了关联度去灌假边。灌数见 `20`，确认前不做。
