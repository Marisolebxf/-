# MySQL 建表规约

> **状态**：第 8 条于 2026-10-26 写入。第 1–7 条仍由 `POLICY-DDL-CONV-L00` 补齐。补齐时不要删第 8 条。  
> **签收自检**：`.cursor/skills/gkx-gdf-ddl-signoff`

## 8. GDF 派单包建表语句

GDF派单中有明确的建表语句和相关注释，派单包任务执行时，需要从dwd.md/ads.md copy相关的sql语句。

派单包签收时自动触发 skill `gkx-gdf-ddl-signoff`（按该任务的维度：政策 / 企业 / 产业）。通过条件：

1. 当前最新版本的派单包中的 sql 建表语句包含了 dwd/ads 相关的建表语句，且建表语句和线上的 demo 数据库保持一致，也和 dwd.md 和 ads.md 中的建表语句一致
2. 线上的 lumen 库中已经创建了相关的表，并且和 1 中的建表语句一致

库名按所在库替换（`demo_gkxlumenx_*` 与 `gkxlumenx_*`），不把库名不同算作不一致。列、类型、空值、默认值、注释、索引、排序规则必须相同。
