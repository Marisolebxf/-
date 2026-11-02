---
name: gkx-graph-pack-signoff
description: >
  Self-check GKX Graph dispatch packs before sign-off: schema, first-batch
  scope, shared files, and the 回签 directory. Use when a Graph workpack is
  signed off (签收), or the user mentions Graph派单包签收, gkx-graph-pack-signoff,
  入图需求和派单, KG-ENT-GRAPH-LOAD, or KG-CHAIN-GRAPH-LOAD.
  Not for GDF DDL (use gkx-gdf-ddl-signoff).
---

# Graph 派单包签收自检

签收 Graph 入图派单任务（`ready_to_sign` → `done`，或用户说「签收」）时必须先跑本检查。未通过不得签收。`task-update-status` 把 `KG-*-GRAPH-LOAD-*` 改为 `done` 时会自动再跑本脚本，退出码非 0 则 `GATE_DENIED`，不改状态。只读，不改派单包，不连 Nebula，不执行 nGQL。

## 何时用

- `KG-ENT-GRAPH-LOAD-*` 或 `KG-CHAIN-GRAPH-LOAD-*` 签收
- 用户点名 `gkx-graph-pack-signoff`，或要求复检 `入图需求和派单`

不传 `--task` 时企业包和产业链包一起查。`--task` 只收窄到那一维，共用的 schema 仍然查。

## 通过条件

1. 企业包带齐 00–07 和 schema。产业链包只带自己的 00、01、05、06、07，schema 和环境指向企业包，不另放一份。
2. schema 只 `CREATE SPACE gkx_chain`。Tag、Edge 各一条，名单与企业包 `03-schema-gkx_chain.ngql` 的现行名单一致。没有 `DROP`，没有 `UNDIRECTED`。没有 Tag `chain`、`technology`、`talent`。
3. 企业第一批只点名企业点、`supply`、`parent_sub`。产业链第一批只点名 Tag `segment`。两份派单说明都写明回签上传到 `对接文档/燕大`。
4. 建图目录里的规则脚本自检通过。索引、WBS、handoff 不再指向旧目录 `data/Graph/入图/`。

登记表里已签收任务的 DoD、`touched_files`、`design_refs` 改不了。本检查不读 `task-registry.yaml`。

## 怎么跑

在 `gkx-orchestration` 根目录：

```powershell
python .cursor/skills/gkx-graph-pack-signoff/scripts/check_graph_pack.py
python .cursor/skills/gkx-graph-pack-signoff/scripts/check_graph_pack.py --task KG-CHAIN-GRAPH-LOAD-L01
```

退出码 `0` 才是通过。不要把图库口令或 MySQL 口令写进命令行、handoff 或聊天。脚本也不打印 `04-环境.md` 的正文。

## 范围

- 派单包：`agent-delivery/data/Graph/入图需求和派单/KG-*-WORKPACK-vN/`
- 抽取说明：`agent-delivery/data/Graph/建图/{企业,产业链}/`
- 索引：`data/Graph/README.md`、图数据库集成 WBS、智谱对接索引、对应 handoff
