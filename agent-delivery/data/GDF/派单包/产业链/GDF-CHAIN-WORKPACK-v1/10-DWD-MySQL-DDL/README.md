# 10 · DWD MySQL DDL（产业链）

**链树四表建表真源**（勿在本目录复制全文 DDL，以免与 v5 双源）：

`agent-delivery/data/data-design/产业链/产业链-DWD表设计-业务需求驱动(v5).md`

入口：`data-design/storage/CHAIN/stores/mysql/dwd-chain.md`

库：`gkxlumenx_dwd`。表名 **无** `dwd_` 前缀。

## 本期必须存在的表（Mapping wash）

| 表 | v5 节 |
|---|---|
| `industry_chain` | §5.1 |
| `industry_chain_node` | §5.2 |
| `industry_chain_node_rel` | §5.3 |
| `industry_chain_entity_rel` | §5.4 |

本期 **不要求** 建 `industry_analysis_*`（B2 不写入）。v5 其余十张 `industry_chain_*` 本期亦不要求建齐；禁止为「表清单好看」灌假数据。

行业分析六表结构快照仅作对照，路径：`data-design/storage/CHAIN/etl/demo_gkxlumenx_dwd_industry_analysis_show_create.sql`。**禁止**对本包 APPLY 六表。

Demo 库 `demo_gkxlumenx_dwd` **不是** 本包目标。
