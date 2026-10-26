# 10 · DWD MySQL DDL（政策 v2.0）

> 列快照继承 v1.0.4，含 `policy_base_info.is_history`。本目录不改 UK。

**产线建表真源（本包冻结）**：

[policy_base_info-MySQL.md](./policy_base_info-MySQL.md)

对照（**禁止**把 `policy_base_info` 的 as-built 列当 APPLY 目标）：

- `policy_base_info` 的 as-built 列清单：`data-design/storage/POLICY/stores/mysql/dwd.md` 主表段（仍 draft；含 `ext1`/`gis_location` 等）。该文件的 `policy_industry_rel` 节是关联表结构真源，不在此禁令内  
- 贴源结构：`data-design/storage/POLICY/sources/ods-ddl.md`

库：`gkxlumenx_dwd`。表名 **无** `dwd_` 前缀。引擎 **仅 MySQL 8**。

## 本期必须存在的表（Mapping wash）

| 表 | 说明 |
|---|---|
| `policy_base_info` | 国内+国际同表；UK `(source_plane, policy_id)`。Wave B 洗这张 |
| `policy_industry_rel` | Wave C 抽取产业。DWD 与 ADS 各一张，**不要**用 Mapping 从 ODS 灌入。结构真源：[dwd.md 的 `policy_industry_rel` 节](../../../../../data-design/storage/POLICY/stores/mysql/dwd.md)。行为约束：[policy_industry_rel-MySQL.md](./policy_industry_rel-MySQL.md) |

本期 **不要求** 建 ES / 图相关表。条款落在已有 ADS `policy_text_parse`，本目录不另给指标表 DDL。禁止为「表清单好看」灌假数据。

Demo 库 `demo_gkxlumenx_dwd` **不是** 本包目标。  
旧 v1 37 列宽表 **禁止** 当贴源，也 **禁止** 按该列集建产线 DWD。
