# Elasticsearch · 企业同步机制

```yaml
---
doc_id: ENT-STORE-ES-SYNC
element: ENT
role: store-elasticsearch
status: draft
version: "2026-08-12"
updated: "2026-08-12"
engine: elasticsearch
s3_task: DATA-ENT-STORAGE-S3-L01
---
```

| 项 | 指针 |
|---|---|
| 更新机制设计 | `data-design/企业/企业搜索-ES更新机制.md`（若存在） |
| ETL 仓 | `${GKX_ROOT}/repos/lumen-etl-es-py` · `scripts/run_etl.py` / `create_enterprise_index.py` |
| 管道说明 | [`../../etl/pipeline-dwd-to-es.md`](../../etl/pipeline-dwd-to-es.md) |
| 失败语义 | 流图：不发布半成品索引；ADS 仍为指标权威 |

调度 cron/DAG 名 → OPEN-ENT-FLOW-01（S2 已挂工作包，DAG 名仍缺）。
