# NebulaGraph · 企业相关子图

```yaml
---
doc_id: ENT-STORE-NEBULA-ENT
element: ENT
role: store-nebula
status: draft
version: "2026-08-12"
updated: "2026-08-12"
engine: nebula
as_built_source: repos/demo-algo-ent-analysis/docs/nebula-space-schema.md
s3_task: DATA-ENT-STORAGE-S3-L01
---
```

> **引擎**：仅 NebulaGraph（`192.168.88.43:9669`）；**禁止 Neo4j**；**Java 禁直连 nGQL**。  
> **Schema 真源**：`${GKX_ROOT}/repos/demo-algo-ent-analysis/docs/nebula-space-schema.md` · 实现 `entan/graph/nebula_loader.py`。  
> Demo 目标 space：`demo_entan` / `demo_gkx_enterprise`（过渡现网常见 `entan` / `gkx_enterprise`）。

## 1. Space（过渡 as-built）

| 属性 | 值（现网 Demo） |
|---|---|
| Space | `entan`（过渡） |
| vid_type | `FIXED_STRING(64)` |
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

第二套图模型；用三方 ODS DDL 倒逼 Tag；前端直连 graphd。
