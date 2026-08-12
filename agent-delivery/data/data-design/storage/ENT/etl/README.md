# ENT · ETL 管道索引

> Demo/Mock 与正式工厂**共用** [`../stores/`](../stores/)；本目录分**写入路径**。见 [`../../README.md`](../../README.md) §5.1。

| 管道 | 文档 | 状态 |
|---|---|---|
| **Demo：LLM→约定 ODS→模拟 GDF** | [`pipeline-demo-mock.md`](./pipeline-demo-mock.md) | **approved** · 主路径（淮政玮 2026-08-12） |
| 可选：Mock 直写 ADS | [`pipeline-mock-to-ads.md`](./pipeline-mock-to-ads.md) | draft · 旁路 · 不得冒充全链路验收 |
| ODS → DWD | [`pipeline-ods-to-dwd.md`](./pipeline-ods-to-dwd.md) | draft · 正式 GDF / Demo 同构调度复用 |
| DWD → ADS | [`pipeline-dwd-to-ads.md`](./pipeline-dwd-to-ads.md) | draft |
| DWD → ES | [`pipeline-dwd-to-es.md`](./pipeline-dwd-to-es.md) | draft |
| → Nebula | [`pipeline-to-nebula.md`](./pipeline-to-nebula.md) | draft |
| → MinIO | [`pipeline-to-minio.md`](./pipeline-to-minio.md) | draft · 含 `demo_**` 桶约定 |
