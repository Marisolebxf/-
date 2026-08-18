# CHAIN · MySQL 存储

| 文档 | 内容 | S3 状态 |
|---|---|---|
| [`dwd-chain.md`](./dwd-chain.md) | 项目 DWD · v5 十四表 `industry_chain_*` | draft · 已灌清单 |
| [`dwd-industry-analysis.md`](./dwd-industry-analysis.md) | 项目 DWD · 行业分析六表 `industry_analysis_*`（CHAIN 切片） | draft · `DATA-CHAIN-INDANA-STORAGE-L01` |
| [`ads.md`](./ads.md) | **ADS 契约面（必须）** · **v2** 十表（对齐 DWD v5 + 原型/DEC） | draft · **现行指针 = v2**；v1 仅对照 |
| [`dim.md`](./dim.md) | 码表 / 对照 | draft · 2026-08-17 增集群两表指针 |
| [`dim-industry-cluster.md`](./dim-industry-cluster.md) | 产业集群 15 + L0 映射（展示目录，非 DWD）；DDL 见 `data/ddl/gkxlumenx_dim_industry_cluster.sql` | draft · 2026-08-17 |

库名约定：正式 `gkxlumenx_dwd` / `gkxlumenx_ads`；Demo `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`（见 `etl/pipeline-demo-mock.md`）。  
**细表不得仅因流图会签标 approved**（`DATA-CHAIN-STORAGE-S3-L01`）。  
**禁止**用供应方约定 ODS 四表（`dwd_industry_chain_*` 等）冒充本目录项目 DWD。  
**禁止**把行业分析六表塞进 `storage/ENT` / `dwd-entity`；**禁止**用 `dwd_industry_chain_news_info` 冒充文档表。
