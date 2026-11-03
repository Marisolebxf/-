# 10 · DWD MySQL DDL（产业链）

> **v2.2 修订（round2 问 14 答复）**：链树四表结构真源 = 本目录 **`dwd-chain.md`**（复制件，库名已全局改为正式库 `gkxlumenx_dwd`）。旧 `链树四表.md`（库名 demo、口径混用）已删除作废。

表名 **无** `dwd_` 前缀，统一 `industry_chain_*`。

## 本期必须存在的表（Mapping wash）

| 表 | 设计说明（不是结构真源） |
|---|---|
| `industry_chain` | v5 §5.1 |
| `industry_chain_node` | v5 §5.2 |
| `industry_chain_node_rel` | v5 §5.3 |
| `industry_chain_entity_rel` | v5 §5.4 |

本期 **不要求** 建 `industry_analysis_*`（B2 不写入）。其余十张 `industry_chain_*` 本期亦不要求建齐；禁止为「表清单好看」灌假数据。

## 真源与作废声明

| 文件 | 地位 |
|---|---|
| `10-DWD-MySQL-DDL/dwd-chain.md`（本目录复制件） | ✅ **链树四表唯一结构真源**（库名 `gkxlumenx_dwd`，2026-11-02 核对与正式库一致） |
| `data-design/storage/CHAIN/stores/mysql/dwd-chain.md` | 源真源（我方仓内维护；更新时随轮次同步复制件） |
| `产业链-DWD表设计-业务需求驱动(v5).md` | ❌ 作废（不再当四张的结构真源）；设计说明仍可参照 |
| ~~`链树四表.md`~~ | ❌ 已删除（v2.1 版库名 demo、与正式库不符） |

GDF 施工**只认本目录 `dwd-chain.md`**；禁读 demo 库（2026-11-02 环境红线）。行业分析六表结构快照仅作对照：`data-design/storage/CHAIN/etl/demo_gkxlumenx_dwd_industry_analysis_show_create.sql`，**禁止**对本包 APPLY 六表。
