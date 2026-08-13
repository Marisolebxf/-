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
version: "2026-08-13"
updated: 2026-08-13
---
```

## 读序（强制）

1. [`00-context.md`](./00-context.md) — 边界与铁律  
2. [`01-data-flow.md`](./01-data-flow.md) — 数据流图（**已会签 approved · 2026-08-13 · human:李伟**）  
3. [`sources/`](./sources/) — 第三方 / ODS 入站  
4. [`etl/`](./etl/) — 工厂与派生管道（**主**：[`pipeline-demo-mock.md`](./etl/pipeline-demo-mock.md)）  
5. [`seeds/`](./seeds/) — 少量覆盖样例索引  
6. [`stores/`](./stores/) — MySQL（含 **ADS**）· ES · Nebula（**S3** 灌；细表不得仅凭流图标 approved）  
7. MinIO → [`../platform/minio.md`](../platform/minio.md) + etl 索引（S2 补 `pipeline-to-minio`）

## 已锁定

| 项 | 值 |
|---|---|
| 根路径 | `data-design/storage/CHAIN/` |
| ADS | 必须（`stores/mysql/ads.md`，S3） |
| MinIO | 平台级 + 本域引用 |
| RDBMS | 仅 MySQL |
| ODS 真源 | **权威** `third-party-source/doc/` xlsx；**优先读** `doc/md-extract/`（产业链要素库） |
| Demo ODS | `demo_gkxlumenx_ods`（S2 建表；禁默认写正式 `gkxlumenx_ods`） |
| 功能设计 | 不进本树 |
| 流图会签 | **approved** · `human:李伟` · 2026-08-13 |
| Demo/Mock | 主路径：约定 ODS → ETL 模拟 GDF；落 `demo_*` |

## 任务

| 阶段 | Task | 状态 |
|---|---|---|
| S1 | `ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01` | **approved** · registry=`integration`（会签完成） |
| S2 | `DATA-CHAIN-STORAGE-S2-L01` | **claimed** · 监管/建表 Owner=`human:李伟` · **建表主单** |
| S3 | `DATA-CHAIN-STORAGE-S3-L01` | backlog |
| S4 | `DATA-CHAIN-STORAGE-S4-L01` | backlog |

## 目录状态

| 路径 | 状态 |
|---|---|
| `00-context.md` | draft |
| `01-data-flow.md` | **approved** |
| `etl/pipeline-demo-mock.md` | draft · S1 口径；其余管道 **S2 补文件** |
| `sources/` `etl/` `seeds/` | S1 骨架；S2 充实 |
| `stores/` | S1 单入口占位；**S3** 灌 mysql/es/nebula |
| `CHANGELOG.md` | 启用 |
