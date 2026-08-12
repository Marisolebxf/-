# 企业维存储 · 上下文与铁律

```yaml
---
doc_id: ENT-STORAGE-CONTEXT
element: ENT
role: context
status: draft
version: "2026-08-12"
updated: 2026-08-12
signoff_owner: architect
---
```

## 1. Data Product 边界

- **域**：企业维（ENT / 科技专题 · 企业分析相关存储）
- **内**：本域 ODS 依赖清单、DWD/ADS/DIM、企业 ES 索引、企业相关 Nebula 子图、本域 MinIO 对象前缀
- **外**：功能设计、UI、指标口径正文（见 metrics / 产品定义）

## 2. 铁律（摘自架构基线，存储视角）

1. 调用链：前端 → Java → Python `/internal/*`；前端/Java **不**直连 DB / Nebula / MinIO（下载经门面）
2. Java **只读 ADS**；不扫 ODS/DWD；不写 ADS；不直连 nGQL
3. 算法与 ETL 在 Python / 数据工厂；写 ADS / Nebula / ES / MinIO（按管道）
4. 图谱引擎 = **NebulaGraph**；禁止 Neo4j
5. 关系库 = **MySQL**；本文禁止 PostgreSQL 叙述
6. 三方源变更不传导 ADS 契约面（D7）

## 3. 存储角色一览

见上级 [`../README.md`](../README.md) §5 矩阵。

## 4. Demo / Mock

- **主路径**：LLM 按 **`third-party-source/doc/`**（**优先读 `md-extract/`**）表结构写 Mock → `demo_*` ODS → **ETL 调度模拟 GDF** → 下游（含 MinIO `demo_**`、Nebula `demo_**`）。见 [`etl/pipeline-demo-mock.md`](./etl/pipeline-demo-mock.md) · 流图 [`01-data-flow.md`](./01-data-flow.md) §7。
- **结构**与正式共用 [`stores/`](./stores/)；**ODS 口径**权威认 xlsx、查阅认 `md-extract/`，不以现网三方 as-built 为准。
- **样本**：[`seeds/`](./seeds/) 少量覆盖；先全链路闭环，后性能。
- **旁路**：[`etl/pipeline-mock-to-ads.md`](./etl/pipeline-mock-to-ads.md)（直写 ADS）不替代全链路验收。

## 5. 下一步

[`01-data-flow.md`](./01-data-flow.md) 已于 **2026-08-12** 会签 **approved**（含 §7 Demo 口径补记）。  
下游：S2 填在线约定文档入口、`demo_*` 命名、LLM/ETL 脚本与 seeds 覆盖矩阵；S3 `stores` as-built。
