# 管道 · → NebulaGraph

> S2 回填 · 仅 Python 写图；Java 禁直连 nGQL

## 意图

企业关系/供应链等子图写入 Nebula；Demo 落 `demo_*` space（目标名见 [`pipeline-demo-mock.md`](./pipeline-demo-mock.md) §4）。

## 指针

| 项 | 路径 |
|---|---|
| 引擎规约 | `agent-delivery/graph-engine.md` |
| storage 契约 | [`../stores/nebula/graph-enterprise.md`](../stores/nebula/graph-enterprise.md) |
| Demo 参考 space | `demo-algo-ent-analysis/conf/settings.yaml` → `entan`（过渡） |
| schema 说明 | `demo-algo-ent-analysis/docs/nebula-space-schema.md` |
| 模型注册 space | `cfg_model_registry` 中 `gkx_enterprise`（过渡名） |
| 企业上链 MySQL 真源 | CHAIN [`../../CHAIN/etl/pipeline-ent-hang.md`](../../CHAIN/etl/pipeline-ent-hang.md)；本叶不强制投影 |

## 禁止

Neo4j；Java 直连 nGQL；用现网三方 DDL 倒逼图 schema。
