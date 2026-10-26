# 企业维 GDF 建表签收自检 · 长任务总控

> **日期**：2026-10-26  
> **授权**：未授权。禁止升 ready、禁止认领、禁止改库。  
> **监管人（授权后）**：`human:淮政玮`  
> **升级人**：DROP、写 ODS / 供应库 `gkx` → `human:李伟`。改列集由 `human:淮政玮` 直接改。  
> **前置**：政策维 `POLICY-DDL-CHECK-L04` 到联调闸门，且 `mysql-ddl-convention.md` 第 8 条已用于政策派单包。  
> **厚包**：本文件。强度：自检叶不改库；处理叶 `ponytail full`。

| 作业 | 任务 | 状态门 |
|------|------|--------|
| 自检 | `ENT-DDL-GDF-CHECK-L00` | 政策 CHECK 联调闸门。只跑 skill，不改包、不改库 |
| 处理 | `ENT-DDL-GDF-FIX-L01` | CHECK 联调闸门，且自检未通过。复制 md 里的 CREATE，再处理库差集 |

现行包：`agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v4/`。结构真源：`agent-delivery/data/data-design/storage/ENT/stores/mysql/` 下的 `dwd.md`、`ads.md`、`dwd-*.md`。

通过条件用 skill `gkx-gdf-ddl-signoff --dimension ent`：

1. 当前最新版本的派单包中的 sql 建表语句包含了 dwd/ads 相关的建表语句，且建表语句和线上的 demo 数据库保持一致，也和 dwd.md 和 ads.md 中的建表语句一致
2. 线上的 lumen 库中已经创建了相关的表，并且和 1 中的建表语句一致

GDF派单中有明确的建表语句和相关注释，派单包任务执行时，需要从dwd.md/ads.md copy相关的sql语句。

处理叶只补自检列出的缺口。md 里还没有 CREATE 的表，先把现网 demo 的带注释 CREATE 写入对应 md，再复制进派单包，不在派单包里另起一套。DROP 有数据的表、写 ODS / `gkx` 停下来升级李伟。
