# Elasticsearch · 服务机构同步机制

```yaml
---
doc_id: SVC-STORE-ES-SYNC
element: SVC
role: store-elasticsearch
status: draft
version: "2026-08-14"
updated: "2026-08-14"
engine: elasticsearch
s3_task: DATA-SVC-STORAGE-S3-L01
---
```

| 项 | 指针 |
|---|---|
| 管道 | [`../../etl/pipeline-dwd-to-es.md`](../../etl/pipeline-dwd-to-es.md) |
| 失败语义 | 流图：不发布半成品索引；ADS 仍为指标权威 |
| 调度 DAG 名 | OPEN-SVC-FLOW-01 / OPEN-SVC-FLOW-04 |

索引清单见 [`index-svc.md`](./index-svc.md)。
