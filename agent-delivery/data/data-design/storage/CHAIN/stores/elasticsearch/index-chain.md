# Elasticsearch · 产业链索引

```yaml
---
doc_id: CHAIN-STORE-ES-INDEX
element: CHAIN
role: store-elasticsearch
status: draft
version: "2026-08-13"
updated: "2026-08-13"
engine: elasticsearch
s3_task: DATA-CHAIN-STORAGE-S3-L01
---
```

> **Mapping 真源**：待专题检索设计定稿后外链（本文件不粘贴全 mapping）。  
> **ETL**：[`../../etl/pipeline-dwd-to-es.md`](../../etl/pipeline-dwd-to-es.md)。  
> 引擎：Elasticsearch；前端不直连。

## 1. 索引规划（draft）

| 索引名（建议） | 文档单位 | 用途 |
|---|---|---|
| `gkx_chain` / `gkx_industry_chain` | 产业链 / L0 产业（`_id = chain_id` 或 `industry_id`） | 链检索 + 列表筛选 |
| `gkx_chain_news`（可选） | 资讯事件 | 热点/资讯检索 |

Demo：同构 mapping，前缀/别名隔离；**不拆第二套字段**。

## 2. 设计要点

- 宽表字段来自 DWD/ADS 投影，**禁止**三方 ODS 直灌检索契约。  
- 图明细不以 ES 为永久边真源（Nebula / DWD `*_rel`）。  
- 同步：[`sync.md`](./sync.md)。

## 3. 禁止

Neo4j；前端直连 ES；仅因流图会签标 approved。
