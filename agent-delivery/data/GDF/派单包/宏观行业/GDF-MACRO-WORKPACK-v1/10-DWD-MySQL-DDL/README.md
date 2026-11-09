# 10 · DWD MySQL DDL（宏观行业 v1.0）

> **状态：草稿，可投递给 GDF 核对。** `data-design/storage/` 下目前没有 MACRO 目录，本目录暂为结构真源（`OPEN-MACRO-05`，待 architect 会签后登记 storage）。  
> **未核现网**：本叶无产线库权限，`gkxlumenx_dwd` / `gkxlumenx_ads` 上这些表是否已存在、列是否一致，**没有查过**（`OPEN-MACRO-06`）。GDF 开工前先核；缺表按本目录新建，已有表只 `ADD COLUMN`，不 `DROP`、不改 UK。

**产线建表真源（本包冻结，草稿）**：

[macro-dwd.md](./macro-dwd.md)（六张 `macro_*`，库 `gkxlumenx_dwd`）

②a 的 ADS 表 `macro_city_section` 的 DDL 在 [12](../12-DWD后加工-城市截面ADS与实效代理附录.md) §2，库 `gkxlumenx_ads`。

库：`gkxlumenx_dwd`。表名带 `macro_` 前缀（无 `dwd_` 前缀），见 `01` §2。引擎 **仅 MySQL 8**。

## 本期必须存在的表

| 表 | 库 | 说明 |
|---|---|---|
| `macro_index_data` | `gkxlumenx_dwd` | 事实；UK 含 `area_code_type`；带区划反解派生列 |
| `macro_index_attribute` | `gkxlumenx_dwd` | 指标属性维度 |
| `macro_admin_area` | `gkxlumenx_dwd` | 区划维度 |
| `macro_index_cal` | `gkxlumenx_dwd` | 计算维度 |
| `macro_index_dur` | `gkxlumenx_dwd` | 时间维度 |
| `macro_source_code` | `gkxlumenx_dwd` | 来源维度 |
| `macro_city_section` | `gkxlumenx_ads` | ②a；Wave B 之后才灌 |

本期 **不要求** 建 ES / 图 / 向量库相关表。禁止为「表清单好看」灌假数据。

Demo 库 `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads` **不是**本包目标。

## 与供应方源表的差异（有意为之）

| 项 | 供应方 `dwd_*` | 本包 `macro_*` |
|---|---|---|
| 物理主键 | `dwd_id` auto_increment（供应方内部） | 自有 `id` auto_increment；**业务键另设 UK** |
| 技术字段 `creater` / `updater` / `table_data_source` / `operator_remarks` / `insert_remark` | 有 | **不进 DWD** |
| 供应方 `rid` | 有 | 落 `src_rid` |
| 供应方 `update_time` / `create_time`（业务口径） | 有 | 落 `src_update_time` / `src_create_time` |
| 供应方 `updated_time`（技术） | 有 | 落 `ods_updated_time`；DWD 自己的 `created_time` / `updated_time` 由作业生成 |
| 事实表区划反解 | 无 | 加 `area_resolve` / `city_code` / `city_name` / `province_code` |
| Excel `t_id` | Excel 有，live 无 | 不建 |
