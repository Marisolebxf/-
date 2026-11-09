# MACRO · MySQL 存储

| 文档 | 内容 | 状态 |
|---|---|---|
| [`dwd.md`](./dwd.md) | 宏观行业 DWD 六表：`macro_index_data` / `macro_admin_area` / `macro_index_attribute` / `macro_index_cal` / `macro_index_dur` / `macro_source_code` | draft |
| [`ads.md`](./ads.md) | ADS：`macro_city_section`（②a 城市宏观截面，整体重建） | draft |

CREATE 复制自派单包 `data/GDF/派单包/宏观行业/GDF-MACRO-WORKPACK-v1/` 的 `10-DWD-MySQL-DDL/macro-dwd.md` 与 `12-...附录.md` §2。改列先改派单包，再同步本目录，不得两边各写一套。

库名约定：文档写 `demo_gkxlumenx_*`，产线换 `gkxlumenx_*`，其余相同（`../../../mysql-ddl-convention.md` §1）。引擎 MySQL 8 only。

现网是否已建表未核（`OPEN-MACRO-06`）。签收自检：`.cursor/skills/gkx-gdf-ddl-signoff`。
