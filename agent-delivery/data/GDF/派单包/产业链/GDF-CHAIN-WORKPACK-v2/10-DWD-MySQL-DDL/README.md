# 10 · DWD MySQL DDL（产业链）

这四张的建表语句以 `dwd-chain.md` 为准，本目录只放复制件。v5 不再当这四张的结构真源。

复制件：`链树四表.md`。语句从 `data-design/storage/CHAIN/stores/mysql/dwd-chain.md` §2.1 原样复制，库名仍是 `demo_gkxlumenx_dwd`。产线 `gkxlumenx_dwd` 只换库名。

表名 **无** `dwd_` 前缀。

## 本期必须存在的表（Mapping wash）

| 表 | 设计说明（不是结构真源） |
|---|---|
| `industry_chain` | v5 §5.1 |
| `industry_chain_node` | v5 §5.2 |
| `industry_chain_node_rel` | v5 §5.3 |
| `industry_chain_entity_rel` | v5 §5.4 |

本期 **不要求** 建 `industry_analysis_*`（B2 不写入）。v5 其余十张 `industry_chain_*` 本期亦不要求建齐；禁止为「表清单好看」灌假数据。

行业分析六表结构快照仅作对照，路径：`data-design/storage/CHAIN/etl/demo_gkxlumenx_dwd_industry_analysis_show_create.sql`。**禁止**对本包 APPLY 六表。

文档 CREATE 的库名是 `demo_gkxlumenx_dwd`。产线执行时只把库名换成 `gkxlumenx_dwd`。
