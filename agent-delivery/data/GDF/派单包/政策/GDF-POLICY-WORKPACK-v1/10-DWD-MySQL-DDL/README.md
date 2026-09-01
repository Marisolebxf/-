# 10 · DWD MySQL DDL（政策）

**产线建表真源（本包冻结）**：

[policy_base_info-MySQL.md](./policy_base_info-MySQL.md)

对照（**禁止**当 APPLY 目标）：

- as-built Demo 列清单：`data-design/storage/POLICY/stores/mysql/dwd.md`（仍 draft；含 `ext1`/`gis_location` 等）  
- 贴源结构：`data-design/storage/POLICY/sources/ods-ddl.md`

库：`gkxlumenx_dwd`。表名 **无** `dwd_` 前缀。引擎 **仅 MySQL 8**。

## 本期必须存在的表（Mapping wash）

| 表 | 说明 |
|---|---|
| `policy_base_info` | 国内+国际同表；UK `(source_plane, policy_id)` |

本期 **不要求** 建 ADS / ES / 图相关表。禁止为「表清单好看」灌假数据。

Demo 库 `demo_gkxlumenx_dwd` **不是** 本包目标。  
旧 v1 37 列宽表 **禁止** 当贴源，也 **禁止** 按该列集建产线 DWD。
