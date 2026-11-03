# 10-DWD-MySQL-DDL — 建表快照

> **工作包**：GDF-SVC-WORKPACK  
> **目标库**：MySQL 8 · `gkxlumenx_dwd`、`gkxlumenx_ads`。不在库名以 `demo_` 开头的库建表。  
> **来源**：`dwd-svc.md` §2.4、`ads.md` §2.1。这两处与 `ddl-demo-empty.sql` 同文。库名换成正式库。  
> **不执行**：正式库表已经在。本目录不 DROP、不重建。缺表时用快照里的 CREATE。

| 文件 | 范围 |
|------|------|
| [DWD表结构设计-服务机构-MySQL.md](./DWD表结构设计-服务机构-MySQL.md) | 圈定池、投融资事件、卡面、四张基础指标表的字段和 CREATE。图谱挂表只附 CREATE，本包不写 |

列的填法仍以 `09` 为准。本目录只定表结构。

## 自检

2026-11-02 `check_gdf_ddl.py --dimension svc` 通过。8 张表与 `dwd-svc.md`、`ads.md`、demo 库、正式库一致。未执行建表。细节在设计稿 §4。
