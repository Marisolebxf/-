# Elasticsearch · 产业链同步机制

```yaml
---
doc_id: CHAIN-STORE-ES-SYNC
element: CHAIN
role: store-elasticsearch
status: draft
version: "2026-08-13"
updated: "2026-08-13"
engine: elasticsearch
s3_task: DATA-CHAIN-STORAGE-S3-L01
---
```

| 项 | 指针 |
|---|---|
| 管道 | [`../../etl/pipeline-dwd-to-es.md`](../../etl/pipeline-dwd-to-es.md) |
| 失败语义 | 流图：不发布半成品索引；ADS 仍为指标权威 |
| 调度 DAG 名 | 开放（产线未回写） |

索引清单见 [`index-chain.md`](./index-chain.md)。
