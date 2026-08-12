# ENT · ETL 管道索引

> Demo/Mock 与正式工厂**共用** [`../stores/`](../stores/)；本目录分**写入路径**。  
> S2：`DATA-ENT-STORAGE-S2-L01`

| 管道 | 文档 | 状态 |
|---|---|---|
| **Demo：LLM→约定 ODS→模拟 GDF** | [`pipeline-demo-mock.md`](./pipeline-demo-mock.md) | **approved** · OPEN-06 **已关** · 脚本 `run_llm_ods.py` |
| 可选：Mock 直写 ADS | [`pipeline-mock-to-ads.md`](./pipeline-mock-to-ads.md) | draft · 旁路 |
| ODS → DWD | [`pipeline-ods-to-dwd.md`](./pipeline-ods-to-dwd.md) | S2 指针已填 · DAG 名 OPEN-01 |
| DWD → ADS | [`pipeline-dwd-to-ads.md`](./pipeline-dwd-to-ads.md) | S2 指针已填 |
| DWD → ES | [`pipeline-dwd-to-es.md`](./pipeline-dwd-to-es.md) | S2 · lumen-etl-es-py |
| → Nebula | [`pipeline-to-nebula.md`](./pipeline-to-nebula.md) | S2 指针已填 |
| → MinIO | [`pipeline-to-minio.md`](./pipeline-to-minio.md) | S2 · 本域前缀建议已填 |
