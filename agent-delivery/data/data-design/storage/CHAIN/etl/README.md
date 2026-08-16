# CHAIN · ETL 管道索引

> Demo/Mock 与正式工厂**共用** [`../stores/`](../stores/)；本目录分**写入路径**。

| 管道 | 文档 | 状态 |
|---|---|---|
| **Demo：约定 ODS→模拟 GDF** | [`pipeline-demo-mock.md`](./pipeline-demo-mock.md) | draft · **S2 已钉脚本+DDL** |
| **Demo 逐步过程 + 映射诚实** | [`pipeline-demo-sim-process.md`](./pipeline-demo-sim-process.md) | draft · `DEMO-CHAIN-SIM-PROCESS-L01` |
| ODS→DWD 字段矩阵 | [`ods-to-dwd-mapping.md`](./ods-to-dwd-mapping.md) | draft · inventory + v5 列名 |
| 可选：Mock 直写 ADS | [`pipeline-mock-to-ads.md`](./pipeline-mock-to-ads.md) | draft · S2 指针 |
| ODS → DWD | [`pipeline-ods-to-dwd.md`](./pipeline-ods-to-dwd.md) | draft · S2 指针；细表 S3 |
| DWD → ADS | [`pipeline-dwd-to-ads.md`](./pipeline-dwd-to-ads.md) | draft · S2 指针 |
| DWD → ES | [`pipeline-dwd-to-es.md`](./pipeline-dwd-to-es.md) | draft · S2 指针 |
| **企业上链 ENT hang→INB** | [`pipeline-ent-hang.md`](./pipeline-ent-hang.md) | as-built · `ENT-CHAIN-HANG-MOCK-L01` |
| → Nebula | [`pipeline-to-nebula.md`](./pipeline-to-nebula.md) | draft · S2 指针 |
| → MinIO | [`pipeline-to-minio.md`](./pipeline-to-minio.md) | draft · 前缀 `chain/{task_id}/` |

DDL 快照：[`demo_gkxlumenx_ods_chain_tables.sql`](./demo_gkxlumenx_ods_chain_tables.sql)（产业链四表 ODS）。  
行业分析：入站 live [`gkx_industry_analysis_show_create.sql`](./gkx_industry_analysis_show_create.sql)；项目 DWD 去前缀稿 [`demo_gkxlumenx_dwd_industry_analysis_show_create.sql`](./demo_gkxlumenx_dwd_industry_analysis_show_create.sql)（**未 APPLY 正式库**）。
