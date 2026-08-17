# NebulaGraph · 服务机构本域切片

```yaml
---
doc_id: SVC-STORE-NEBULA
element: SVC
role: store-nebula
status: draft
version: "2026-08-14"
updated: "2026-08-14"
engine: nebula
s3_task: DATA-SVC-STORAGE-S3-L01
as_built_source: data-design/服务机构/服务机构域数据库设计(v1).md §7（对照）
---
```

> **引擎**：仅 NebulaGraph（`192.168.88.43:9669`）；**禁止 Neo4j**；**Java 禁直连 nGQL**。  
> **关系真源**：DWD `service_org_chain_rel` / `service_org_org_rel`；Python 投影写入。  
> ETL：[`../../etl/pipeline-to-nebula.md`](../../etl/pipeline-to-nebula.md)。  
> **禁止**复制 CHAIN `industry_chain_*` 图谱模型到本 space。

## 1. Space（设计目标）

| 属性 | 值 |
|---|---|
| Space（正式目标） | `gkx_svc` |
| Demo | `demo_gkx_svc`（建议） |
| vid | `svc:{service_org_code}`（与 DWD 对齐） |
| partition / replica | 与平台约定；开放项可复用 ENT |

## 2. Tag / Edge（摘要 · draft）

| 类型 | 名（建议） | 说明 |
|---|---|---|
| Tag | `service_org` | 圈定机构点；属性仅本域必要字段 |
| Tag | `service_link`（可选） | 服务链环节点（本域定义；**非** CHAIN 节点照搬） |
| Edge | `svc_serves_link` | 机构 → 环节 |
| Edge | `svc_coop_with` | 机构 ↔ 机构（合作等） |

> OPEN：Tag/Edge 与 E7 生态叶子边类型对齐后再结构评审；当前 **draft**。

## 3. 读写

| 写 | 读 |
|---|---|
| Python | Python；Java 经 Feign `/internal` |

## 4. 禁止

Neo4j；Java 直连；复制 CHAIN 数据模型；ADS/ES 另建永久边真源；细表仅因流图会签标 approved。
