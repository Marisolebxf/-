# SVC · ETL 管道索引

> Demo/Mock 与正式工厂**共用** [`../stores/`](../stores/)；本目录分**写入路径**。  
> 细表 **draft**。本索引自己不执行灌数。  
> **2026-11-02**：demo 库服务机构表已有行，正式库同名表 0 行，GDF 作业未建。行数与触发见 [`../02-asbuilt-process-chain.md`](../02-asbuilt-process-chain.md)。不要把本索引早期的「未灌数」读成「库里没有表」。

| 管道 | 文档 | 状态 |
|---|---|---|
| **Demo：约定 ODS→模拟 GDF** | [`pipeline-demo-mock.md`](./pipeline-demo-mock.md) | draft 指针 · S2 |
| **→ Nebula（112/113 · 灌数零图谱）** | [`pipeline-to-nebula.md`](./pipeline-to-nebula.md) | draft 契约 · `DEMO-SVC-GRAPH-TRIPLE-UI-L01` 步1 · `diagram_id=SVC-GRAPH-TRIPLE` |
| 产业关联实查 | [产业检索服务机构条数](../../../../../qa/test-cases/SDWJSF-KJZTFWSFK/svc-产业服务分析/产业检索服务机构条数-20261024.md) | 2026-10-24 demo · 按产业 / 节点可命中的机构数（链码关联为 0） |
| ODS → SVC DWD（hang） | [`ods-to-dwd-mapping.md`](./ods-to-dwd-mapping.md) | draft · OPEN-06 写作关 |
| ODS → ADS（A1–A6 列对照） | [`ods-to-ads-mapping.md`](./ods-to-ads-mapping.md) | draft · `DATA-SVC-STORAGE-GAP-L02` |
| → MinIO | [`pipeline-to-minio.md`](./pipeline-to-minio.md) | draft 指针 · 前缀 `svc/{task_id}/` |

Demo 空表 DDL：[`../stores/mysql/ddl-demo-empty.sql`](../stores/mysql/ddl-demo-empty.sql)。本索引不执行它。2026-11-02 demo 表已有行、正式库同名表已建且 0 行；仓内这份 DDL 只写 `demo_gkxlumenx_*`，对不上正式库建表人，未闭合。
