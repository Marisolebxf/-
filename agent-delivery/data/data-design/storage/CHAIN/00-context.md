# 产业链维存储 · 上下文与铁律

```yaml
---
doc_id: CHAIN-STORAGE-CONTEXT
element: CHAIN
role: context
status: draft
version: "2026-08-13"
updated: 2026-08-13
signoff_owner: human:李伟
---
```

## 1. Data Product 边界

- **域**：产业链维（CHAIN / 科技专题 · 产业链分析相关存储）
- **内**：本域 ODS 依赖清单、DWD/ADS/DIM、产业链相关 ES / Nebula、本域 MinIO 对象前缀
- **外**：功能设计、UI、指标口径正文（见 metrics / 产品定义）；企业/机构等主体完整属性由各权威域维护，本域只保留稳定业务键与关系

## 2. 铁律（摘自架构基线，存储视角）

1. 调用链：前端 → Java → Python `/internal/*`；前端/Java **不**直连 DB / Nebula / MinIO（下载经门面）
2. Java **只读 ADS**；不扫 ODS/DWD；不写 ADS；不直连 nGQL
3. 算法与 ETL 在 Python / 数据工厂；写 ADS / Nebula / ES / MinIO（按管道）
4. 图谱引擎 = **NebulaGraph**；禁止 Neo4j
5. 关系库 = **MySQL**；本文禁止 PostgreSQL / `dwd.` PG schema 叙述
6. 三方源变更不传导 ADS 契约面（D7）

## 3. 存储角色一览

见上级 [`../README.md`](../README.md) §5 矩阵（ENT 与 CHAIN 同构；实例前缀/对象前缀按域区分）。

## 4. ODS / DWD 分层（勿混淆）

| 层 | 本域约定 | 说明 |
|---|---|---|
| **约定贴源（ODS）** | 表名/字段 = `doc/` xlsx；日常读 `md-extract/`「产业链要素库」 | 供应方表名常带 `dwd_*` 前缀，**落库角色仍是 ODS** |
| **Demo ODS 实例** | `demo_gkxlumenx_ods` | **S2 建表目标**；禁止默认写 `gkxlumenx_ods` |
| **项目 DWD** | 目标见 `data-design/产业链/产业链-DWD表设计-业务需求驱动(v5).md`（`industry_chain_*`） | 经 GDF/模拟 GDF 映射；**不是**把要素库原样当项目 DWD |
| **冲突** | 旧 `DATA-CHAIN-db-design.md`（PostgreSQL）、7 张 Mock `chain_*` 映射 | **以本树会签流图为准**；旧稿仅历史输入 |

## 5. Demo / Mock

- **主路径**：按 **`third-party-source/doc/`**（优先 `md-extract/`）约定表结构写入 → `demo_*` ODS → **ETL 调度模拟 GDF** → 下游。见 [`etl/pipeline-demo-mock.md`](./etl/pipeline-demo-mock.md) · 流图 [`01-data-flow.md`](./01-data-flow.md) §7。
- **结构**与正式共用 [`stores/`](./stores/)；**ODS 口径**不以 `gkx-mysql-raw` as-built 为准。
- **样本**：[`seeds/`](./seeds/) 少量覆盖；先闭环后性能。
- **旁路**：直写 ADS（D7）不替代全链路验收；细则 S2 补 `etl/pipeline-mock-to-ads.md`。

## 6. 下一步

1. [`01-data-flow.md`](./01-data-flow.md) 已于 **2026-08-13** 会签 **approved**（`human:李伟`）  
2. **S2 已放行**：`DATA-CHAIN-STORAGE-S2-L01` — 按产业链要素库在 `demo_gkxlumenx_ods` **建表**  
