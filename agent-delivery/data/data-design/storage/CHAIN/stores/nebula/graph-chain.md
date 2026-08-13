# NebulaGraph · 产业链子图

```yaml
---
doc_id: CHAIN-STORE-NEBULA
element: CHAIN
role: store-nebula
status: draft
version: "2026-08-13"
updated: "2026-08-13"
engine: nebula
s3_task: DATA-CHAIN-STORAGE-S3-L01
as_built_source: agent-handoffs/产业链分析-CHAIN/DATA-CHAIN-db-design.md §7
---
```

> **引擎**：仅 NebulaGraph（`192.168.88.43:9669`）；**禁止 Neo4j**；**Java 禁直连 nGQL**。  
> **Schema 指针**：[`DATA-CHAIN-db-design.md`](../../../../../agent-handoffs/产业链分析-CHAIN/DATA-CHAIN-db-design.md) §7（历史稿；落地前按 v5 关系表投影修订）。  
> **关系真源**：DWD `industry_chain_node_rel` / `entity_rel` / `event_entity_rel`（v5）；Python 投影写入 Nebula。  
> ETL：[`../../etl/pipeline-to-nebula.md`](../../etl/pipeline-to-nebula.md)。

## 1. Space（设计目标）

| 属性 | 值 |
|---|---|
| Space（正式目标） | `gkx_chain` |
| Demo | `demo_gkx_chain`（建议） |
| vid_type | `FIXED_STRING(80)`（设计稿）；落地以现网为准 |
| partition / replica | 设计稿 10 / 1 |

## 2. Tag / Edge（摘要 · 设计稿）

**Tag**：`chain` · `segment` · `enterprise` · `institution`  
**Edge**：见 DATA-CHAIN-db-design §7.2（上下游/归属等）

> OPEN：Tag/Edge 与 v5 `node_rel`/`entity_rel` 命名对齐复核后再标 approved。

## 3. 读写

| 写 | 读 |
|---|---|
| Python | Python；Java 经 Feign `/internal` |

## 4. 禁止

Neo4j；Java 直连；ADS/ES 另建永久边真源；细表仅因流图会签标 approved。
