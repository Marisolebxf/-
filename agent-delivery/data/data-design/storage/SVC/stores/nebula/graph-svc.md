# NebulaGraph · 服务机构本域切片

```yaml
---
doc_id: SVC-STORE-NEBULA
element: SVC
role: store-nebula
status: draft
version: "2026-08-17"
updated: "2026-08-17"
engine: nebula
s3_task: DATA-SVC-STORAGE-S3-L01
as_built_source: data-design/服务机构/服务机构域数据库设计(v1).md §7（对照）
---
```

> **引擎**：仅 NebulaGraph（`192.168.88.43:9669`）；**禁止 Neo4j**；**Java 禁直连 nGQL**。  
> **关系真源**：DWD `service_org_chain_rel` / `service_org_org_rel`；Python 投影写入。  
> ETL：[`../../etl/pipeline-to-nebula.md`](../../etl/pipeline-to-nebula.md)。  
> **一张 G**：服务机构点/边挂接到 `demo_gkx_chain` / `gkx_chain`（决策 #7）。**禁止**复制 CHAIN `industry_chain_*` 模型另起第二张七要素图；`demo_gkx_svc` 不得写成目标态独立图或「二期再并」。

## 1. Space

| 属性 | 值 |
|---|---|
| 一张 G（目标） | `demo_gkx_chain` / `gkx_chain` |
| 历史设计名 | `gkx_svc` / `demo_gkx_svc` — **不作为**第二张图的建设目标 |
| vid | `svc:{service_org_code}`（与 DWD 对齐，挂到一张 G） |
| partition / replica | 与一张 G 相同 |

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

Neo4j；Java 直连；复制 CHAIN 数据模型另起一张图；把 `demo_gkx_svc` 当目标态分域再二期并库；ADS/ES 另建永久边真源；细表仅因流图会签标 approved。
