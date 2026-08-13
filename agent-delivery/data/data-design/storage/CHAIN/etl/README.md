# CHAIN · ETL 管道索引

> Demo/Mock 与正式工厂**共用** [`../stores/`](../stores/)；本目录分**写入路径**。  
> S1：只保留 Demo 主路径口径。**其余管道文件由 S2 按 ENT 同构补齐。**

| 管道 | 文档 | 状态 |
|---|---|---|
| **Demo：约定 ODS→模拟 GDF** | [`pipeline-demo-mock.md`](./pipeline-demo-mock.md) | draft · S1 已钉真源/库名 |
| 可选：Mock 直写 ADS | `pipeline-mock-to-ads.md` | **S2 新建** |
| ODS → DWD | `pipeline-ods-to-dwd.md` | **S2 新建** |
| DWD → ADS | `pipeline-dwd-to-ads.md` | **S2 新建** |
| DWD → ES | `pipeline-dwd-to-es.md` | **S2 新建** |
| → Nebula | `pipeline-to-nebula.md` | **S2 新建** |
| → MinIO | `pipeline-to-minio.md` | **S2 新建**（前缀建议 `chain/{task_id}/`） |
