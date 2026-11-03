---
name: gkx-gdf-ddl-signoff
description: >
  Self-check a GKX GDF workpack CREATE TABLE against storage dwd.md/ads.md,
  the live demo database, and the live lumen database. Use when a GDF workpack
  is signed off (签收), when the user mentions GDF派单包签收, gkx-gdf-ddl-signoff,
  or rechecking GDF-POLICY-WORKPACK, GDF-ENT-WORKPACK, GDF-CHAIN-WORKPACK, or GDF-SVC-WORKPACK.
  Not for generating CDC Excel (use gkx-gdf-cdc-workpack).
---

# GDF 派单包签收自检

规约：`agent-delivery/data/data-design/storage/mysql-ddl-convention.md` 第 8 条。

GDF派单中有明确的建表语句和相关注释，派单包任务执行时，需要从dwd.md/ads.md copy相关的sql语句。

签收（`ready_to_sign` → `done`，或用户说「签收」）时必须先跑本检查。未通过不得签收。`task-update-status` 把 `GDF-*-WORKPACK-*` 改为 `done` 时会自动再跑本脚本，退出码非 0 则 `GATE_DENIED`，不改状态。只读，不改库、不改派单包。

## 何时用

- 政策 / 企业 / 产业（产业链）/ 服务机构任一 GDF 派单包任务签收
- 用户点名 `gkx-gdf-ddl-signoff`，或要求按该 skill 复检 `GDF-*-WORKPACK-*`

维度从任务 ID 取：`GDF-POLICY-` → `policy`，`GDF-ENT-` → `ent`，`GDF-CHAIN-` → `chain`，`GDF-SVC-` 或「服务机构」→ `svc`。服务机构现行包目录没有版本号。

## 通过条件

1. 当前最新版本的派单包中的 sql 建表语句包含了 dwd/ads 相关的建表语句，且建表语句和线上的 demo 数据库保持一致，也和 dwd.md 和 ads.md 中的建表语句一致
2. 线上的 lumen 库中已经创建了相关的表，并且和 1 中的建表语句一致

库名按所在库替换。列、类型、空值、默认值、注释、索引、排序规则必须相同。连不上库，或口令未设置，条件 2 记为未核对，整次不通过。

## 怎么跑

在 `gkx-orchestration` 根目录：

```powershell
python .cursor/skills/gkx-gdf-ddl-signoff/scripts/check_gdf_ddl.py --task GDF-POLICY-WORKPACK-V2-L01
```

`--dimension policy|ent|chain|svc` 可代替 `--task`。退出码 `0` 才是通过。

业务库口令只从环境变量 `GKX_LUMEN_MYSQL_PASSWORD` 读（主机默认 `10.50.11.76`，用户默认 `gkxlumenx`）。不要把口令写进命令行、handoff 或聊天。

## 范围

- 最新未作废派单包：`agent-delivery/data/GDF/派单包/{政策|企业|产业链}/GDF-*-WORKPACK-vN/`，以及 `派单包/服务机构/GDF-SVC-WORKPACK/`
- 结构真源：`agent-delivery/data/data-design/storage/{POLICY|ENT|CHAIN|SVC}/stores/mysql/` 下的 `dwd.md`、`ads.md` 以及同目录 `dwd-*.md`
- demo 库：`demo_gkxlumenx_dwd`、`demo_gkxlumenx_ads`
- lumen 库：`gkxlumenx_dwd`、`gkxlumenx_ads`

md 里没有 `CREATE TABLE` 的表，派单包不得另写一套。派单包有而 md 没有的建表语句，算未从 md 复制，不通过。
