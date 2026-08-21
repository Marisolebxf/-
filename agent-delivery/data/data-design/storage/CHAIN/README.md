# 产业链维（CHAIN）存储设计 — 入口

> **读我**：本目录是产业链维存储与数据工程的**现行入口**（并行于 `data-design/产业链/` legacy）。  
> **规范**：[`../README.md`](../README.md)（与 ENT 共用体系；本域同构落地）  
> **流图会签**：架构师 · Owner `human:李伟` · 文件 [`01-data-flow.md`](./01-data-flow.md)

```yaml
---
doc_id: CHAIN-STORAGE-INDEX
element: CHAIN
role: index
status: draft
version: "2026-08-20"
updated: 2026-08-20
---
```

## 读序（强制）

1. [`00-context.md`](./00-context.md) — 边界与铁律  
2. [`01-data-flow.md`](./01-data-flow.md) — 数据流图（**已会签 approved · 2026-08-13 · human:李伟**）；**人主看** [`01-data-flow.md` §8](./01-data-flow.md)  
3. [`sources/`](./sources/) — 第三方 / ODS 入站（产业链四表 [`sources/inventory.md`](./sources/inventory.md)；行业分析六表 [`sources/inventory-industry-analysis.md`](./sources/inventory-industry-analysis.md)）  
4. [`etl/`](./etl/) — 工厂与派生管道（**主**：[`etl/pipeline-demo-mock.md`](./etl/pipeline-demo-mock.md)；**Demo 逐步过程**：[`etl/pipeline-demo-sim-process.md`](./etl/pipeline-demo-sim-process.md)）  
5. [`seeds/`](./seeds/) — 少量覆盖样例索引  
6. [`stores/`](./stores/) — MySQL（含 **ADS**）· ES · Nebula（**S3** 灌；细表不得仅凭流图标 approved）  
7. MinIO → [`../platform/minio.md`](../platform/minio.md) + etl 索引（S2 补 `pipeline-to-minio`）

## 已锁定

| 项 | 值 |
|---|---|
| 根路径 | `data-design/storage/CHAIN/` |
| ADS | **必须** · 现行真源 **v2**（`stores/mysql/ads.md` → 原型与 Handoff 驱动稿） |
| MinIO | 平台级 + 本域引用 |
| RDBMS | 仅 MySQL |
| ODS 真源 | **权威** `third-party-source/doc/` xlsx；**优先读** `doc/md-extract/`（产业链要素库） |
| Demo ODS | `demo_gkxlumenx_ods`（S2 建表；禁默认写正式 `gkxlumenx_ods`） |
| 功能设计 | 不进本树 |
| 流图会签 | **approved** · `human:李伟` · 2026-08-13 |
| Demo/Mock | 主路径：约定 ODS → ETL 模拟 GDF；落 `demo_*` |
| 一张 G | **`demo_gkx_chain` / `gkx_chain`**（决策 #7 · 从建库起；无二期并库） |

## 任务

| 阶段 | Task | 状态 |
|---|---|---|
| S1 | `ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01` | **done** · 流图 approved · `human:李伟` |
| S2 | `DATA-CHAIN-STORAGE-S2-L01` | **done** |
| S3 | `DATA-CHAIN-STORAGE-S3-L01` | **done** · `human:淮政玮` 签收 2026-08-14；**2026-08-17 决策 #7**：一张 G 落 `demo_gkx_chain` |
| S4 | `DATA-CHAIN-STORAGE-S4-L01` | **done** · legacy stub → `storage/CHAIN` |
| 增量 | `DATA-CHAIN-INDANA-STORAGE-L01` | **行业分析六表切片已交** · 细表 draft · 主图未翻签 · 待 `human:李伟` 会签增量 |
| 增量 | `DEMO-CHAIN-SIM-PROCESS-L01` | **Demo 全链路过程文 + ODS→DWD 映射诚实** · 细表 draft · **未翻签** `01-data-flow` |
| 增量 | `CHAIN-INDUSTRY-CLUSTER-SUPP-L01` | **in_progress** · DIM 真源 + 波次 B DDL/契约/种子草稿；未 apply 库、未改业务仓 |
| 增量 | `DATA-POLICY-STORAGE-S1-L01` | **政策挂接** · 附录 B 已由 `human:淮政玮` 放行 · 不翻签主图 · 不经李伟 |

## 目录状态

| 路径 | 状态 |
|---|---|
| `00-context.md` | draft |
| `01-data-flow.md` | **approved** |
| `etl/pipeline-demo-mock.md` | draft · S2 脚本+DDL；过程指针 2026-08-16 |
| `etl/pipeline-demo-sim-process.md` | draft · Demo 逐步过程 |
| `etl/ods-to-dwd-mapping.md` | draft · 四表→十四表字段矩阵 |
| `etl/pipeline-*.md` | S2 指针齐套；细实现 S3 |
| `sources/inventory.md` | S2 四表字段摘要 |
| `sources/inventory-industry-analysis.md` | 行业分析六表切片（draft · 2026-08-16） |
| `stores/mysql/dwd-industry-analysis.md` | 项目 DWD `industry_analysis_*`（draft） |
| `seeds/` | S2 覆盖矩阵骨架 |
| `stores/` | **S3** 已灌；**ADS 指针 = v2**（细表仍 draft） |
| `stores/mysql/dim-industry-cluster.md` | draft · 2026-08-17 产业集群 15 + L0 映射 |
| `seeds/industry-cluster-sz-10+5-2026.yaml` | draft · 波次 B Demo/前端 mock 种子 |
| `CHANGELOG.md` | 启用 |
