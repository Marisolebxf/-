# SVC · ETL 管道索引

> Demo/Mock 与正式工厂**共用** [`../stores/`](../stores/)；本目录分**写入路径**。  
> 细表 **draft**。**未灌数。**

| 管道 | 文档 | 状态 |
|---|---|---|
| **Demo：约定 ODS→模拟 GDF** | [`pipeline-demo-mock.md`](./pipeline-demo-mock.md) | draft 指针 · S2 |
| **→ Nebula（112/113 · 灌数零图谱）** | [`pipeline-to-nebula.md`](./pipeline-to-nebula.md) | draft 契约 · `DEMO-SVC-GRAPH-TRIPLE-UI-L01` 步1 · `diagram_id=SVC-GRAPH-TRIPLE` |
| ODS → SVC DWD（hang） | [`ods-to-dwd-mapping.md`](./ods-to-dwd-mapping.md) | draft · OPEN-06 写作关 |
| ODS → ADS（A1–A6 列对照） | [`ods-to-ads-mapping.md`](./ods-to-ads-mapping.md) | draft · `DATA-SVC-STORAGE-GAP-L02` |
| → MinIO | [`pipeline-to-minio.md`](./pipeline-to-minio.md) | draft 指针 · 前缀 `svc/{task_id}/` |

Demo 空表 DDL：[`../stores/mysql/ddl-demo-empty.sql`](../stores/mysql/ddl-demo-empty.sql)（**未执行**）。
