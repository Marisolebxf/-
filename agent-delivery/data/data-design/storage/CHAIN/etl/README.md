# CHAIN · ETL 管道索引

> Demo/Mock 与正式工厂**共用** [`../stores/`](../stores/)；本目录分**写入路径**。

| 管道 | 文档 | 状态 |
|---|---|---|
| **Demo：约定 ODS→模拟 GDF** | [`pipeline-demo-mock.md`](./pipeline-demo-mock.md) | draft · **S2 已钉脚本+DDL** |
| 可选：Mock 直写 ADS | [`pipeline-mock-to-ads.md`](./pipeline-mock-to-ads.md) | draft · S2 指针 |
| ODS → DWD | [`pipeline-ods-to-dwd.md`](./pipeline-ods-to-dwd.md) | draft · S2 指针；细表 S3 |
| DWD → ADS | [`pipeline-dwd-to-ads.md`](./pipeline-dwd-to-ads.md) | draft · S2 指针 |
| DWD → ES | [`pipeline-dwd-to-es.md`](./pipeline-dwd-to-es.md) | draft · S2 指针 |
| → Nebula | [`pipeline-to-nebula.md`](./pipeline-to-nebula.md) | draft · S2 指针 |
| → MinIO | [`pipeline-to-minio.md`](./pipeline-to-minio.md) | draft · 前缀 `chain/{task_id}/` |

DDL 快照：[`demo_gkxlumenx_ods_chain_tables.sql`](./demo_gkxlumenx_ods_chain_tables.sql)
