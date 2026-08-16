# 管道 · → Nebula（产业链）

> S2 指针 · 图空间/边类型 **S3** · 仅 NebulaGraph（禁 Neo4j）

## 意图

产业链节点/企业/产品关系写入 Nebula（`192.168.88.43:9669` 环境约定见架构基线）。

## 指针

| 项 | 路径 |
|---|---|
| 流图 | [`../01-data-flow.md`](../01-data-flow.md) |
| stores | [`../stores/README.md`](../stores/README.md) |
| ENT 参考 | [`../../ENT/etl/pipeline-to-nebula.md`](../../ENT/etl/pipeline-to-nebula.md) |
| 企业上链（MySQL 真源） | [`pipeline-ent-hang.md`](./pipeline-ent-hang.md)：`enterprise_industry_chain` + `industry_chain_entity_rel`（`entity_id=org_id`）。本管道投影 **fail-soft**；`ENT-CHAIN-HANG-MOCK-L01` **不强制**写 Nebula（图投影见 `DEMO-CHAIN-PY-GRAPH-L01`）。 |
| Demo 投影 | `project.py` → space 目标 `demo_gkx_chain`；现行 fail-soft；**禁止 Neo4j** |
