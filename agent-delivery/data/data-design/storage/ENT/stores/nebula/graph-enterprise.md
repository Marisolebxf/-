# NebulaGraph · 企业相关子图

```yaml
---
doc_id: ENT-STORE-NEBULA-ENT
element: ENT
role: store-nebula
status: draft
version: "2026-08-17"
updated: "2026-08-17"
engine: nebula
as_built_source: repos/demo-algo-ent-analysis/docs/nebula-space-schema.md
s3_task: DATA-ENT-STORAGE-S3-L01
---
```

> **引擎**：仅 NebulaGraph 协议（graphd `10.50.75.136:9669`）；**禁止 Neo4j**；**Java 禁直连 nGQL**。  
> **Schema 真源**：`${GKX_ROOT}/repos/demo-algo-ent-analysis/docs/nebula-space-schema.md` · 实现 `entan/graph/nebula_loader.py`。  
> **一张 G**：七要素挂接目标 = `demo_gkx_chain`（决策 #7）；本文件的 `entan` / `demo_entan` 是企业分析联调 **as-built**，不是第二套本体，也不是「二期再并」。

## 1. Space

| 属性 | 值 |
|---|---|
| 一张 G（七要素） | `demo_gkx_chain` / `gkx_chain` |
| 企业分析联调 as-built | `entan`（现网）/ `demo_entan`（Demo 定名；弃用 `demo_gkx_enterprise` 作目标名） |
| vid_type（as-built） | `FIXED_STRING(64)` |
| partition_num / replica | 10 / 1 |

## 2. Tag / Edge（摘要）

**Tag**：`enterprise` · `industry` · `research` · `talent` · `service`（共享 name/node_type/weight/props）

**Edge**：`industry_belong` · `research_coop` · `talent_coop` · `service_provide` · `cooperate` · `supply` · `parent_sub`

## 3. 读写

| 写 | 读 |
|---|---|
| Python（`nebula_loader` / run_all） | Python；Java 经 Feign `/internal` |

ADS 镜像兜底：`graph_node` / `graph_edge`（见 [`../mysql/ads.md`](../mysql/ads.md)）。

## 4. 禁止

第二套七要素本体；把本 as-built space 写成「目标态分域、二期并进 `gkx_topic`」；用三方 ODS DDL 倒逼 Tag；前端直连 graphd。
