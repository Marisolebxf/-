# Elasticsearch · 服务机构索引

```yaml
---
doc_id: SVC-STORE-ES-INDEX
element: SVC
role: store-elasticsearch
status: draft
version: "2026-08-14"
updated: "2026-08-14"
engine: elasticsearch
s3_task: DATA-SVC-STORAGE-S3-L01
---
```

> **Mapping 真源**：待专题检索设计定稿后外链（本文件不粘贴全 mapping）。  
> **ETL**：[`../../etl/pipeline-dwd-to-es.md`](../../etl/pipeline-dwd-to-es.md)。  
> 文档单位来自 **项目 DWD/ADS 投影**，禁止三方 ODS 直灌检索契约。

## 1. 索引规划（draft）

| 索引名（建议） | 文档单位 | 用途 |
|---|---|---|
| `gkx_svc_org` | 圈定机构（`_id = service_org_code`） | 列表检索 / 筛选（类型·区域·待核验标记） |
| `gkx_svc_rec`（可选） | 招引/培育名单行 | 名单检索；可先走 ADS 直出 |

Demo：同构 mapping，前缀/别名隔离；**不拆第二套字段**。  
索引文档须带 `verification_status`（有则），避免把待核验池当 live 默认。

## 2. 设计要点

- 宽表来自 `service_org*` / ADS 投影；机构全量属性仍经键回 ENT。  
- 图边不以 ES 为永久真源（Nebula / DWD `*_rel`）。  
- 同步：[`sync.md`](./sync.md)。

## 3. 禁止

Neo4j；前端直连 ES；仅因流图会签标 approved。
