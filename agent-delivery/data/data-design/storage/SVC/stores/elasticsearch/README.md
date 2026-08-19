# Elasticsearch · 服务机构（指针 · 不挡 F）

```yaml
---
doc_id: SVC-STORE-ES
element: SVC
role: store-elasticsearch
status: draft
version: "2026-08-19"
updated: "2026-08-19"
engine: elasticsearch
s3_task: DATA-SVC-STORAGE-S3-L02
---
```

> **本总控（阶段 F）不施工独立 SVC 索引。** 底座退出门认 50100 + Demo ADS/图，不认 ES。  
> OPEN-SVC-FLOW-04（同步失败 SLA）保持开放，不阻塞本单。

| 项 | 约定 |
|---|---|
| 阶段 F | 不新建 `svc_*` 索引；不挡 F-SEED / F-ALGO |
| 阶段 P（未授权） | 若检索需要，跟 ENT 企业索引策略对齐，另单 |
| 权威 | 指标以 ADS 为准；ES 失败不得冒充灌完 |

禁止前端直连 ES。禁止用 ES 替代 `svc_org_circle` / ADS 契约表。
