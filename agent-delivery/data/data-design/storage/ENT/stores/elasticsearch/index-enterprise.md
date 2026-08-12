# Elasticsearch · 企业索引

```yaml
---
doc_id: ENT-STORE-ES-INDEX
element: ENT
role: store-elasticsearch
status: draft
version: "2026-08-12"
updated: "2026-08-12"
engine: elasticsearch
as_built_source: data-design/企业/企业搜索-ES索引设计.md
s3_task: DATA-ENT-STORAGE-S3-L01
---
```

> **Mapping / 字段真源**：[`企业搜索-ES索引设计.md`](../../../企业/企业搜索-ES索引设计.md)（勿在本文件粘贴全 mapping）。  
> **ETL**：[`../../etl/pipeline-dwd-to-es.md`](../../etl/pipeline-dwd-to-es.md) → `lumen-etl-es-py`。  
> 历史文档中「PG DWD」表述以 **现网 MySQL DWD** 为准（引擎已迁）。

## 1. 索引规划（as-built 设计）

| 索引名 | 文档单位 | 用途 |
|---|---|---|
| `gkx_enterprise` | 企业（`_id = org_id`） | 检索 + 详情宽表 + 分析聚合 |

Demo：可用同构别名/索引前缀；实例隔离策略与正式 mapping **不拆第二套字段**。

## 2. 设计要点（摘要）

- 宽表 + nested；司法全量明细 **不灌 ES**（仅 `risk_flags` / `risk_level` 等筛选字段）。  
- `nested_objects.limit` 等运维参数见设计文档。  
- 同步机制：[`sync.md`](./sync.md)。

## 3. 禁止

Neo4j；前端直连 ES；把三方 ODS 字段直接打进检索契约而不经 DWD。
