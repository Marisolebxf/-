# 企业维（ENT）存储设计 — 入口

> **读我**：本目录是企业维存储与数据工程的**现行入口**（并行于 `data-design/企业/` legacy）。  
> **规范**：[`../README.md`](../README.md)  
> **流图会签**：架构师 · 文件 [`01-data-flow.md`](./01-data-flow.md)

```yaml
---
doc_id: ENT-STORAGE-INDEX
element: ENT
role: index
status: draft
version: "2026-08-12"
updated: 2026-08-12
---
```

## 读序（强制）

1. [`00-context.md`](./00-context.md) — 边界与铁律  
2. [`01-data-flow.md`](./01-data-flow.md) — 数据流图（**已会签 approved · 2026-08-12**）  
3. [`sources/`](./sources/) — 第三方 / ODS 入站  
4. [`etl/`](./etl/) — 工厂与派生管道（**主**：[`pipeline-demo-mock.md`](./etl/pipeline-demo-mock.md)）  
5. [`seeds/`](./seeds/) — 少量覆盖样例索引（先闭环后性能）  
6. [`stores/`](./stores/) — MySQL（含 **ADS**）· ES · Nebula  
7. MinIO → [`../platform/minio.md`](../platform/minio.md)（平台正文 · 含 `demo_**` 桶）+ [`etl/pipeline-to-minio.md`](./etl/pipeline-to-minio.md)

## 已锁定

| 项 | 值 |
|---|---|
| 根路径 | `data-design/storage/ENT/` |
| ADS | 必须（`stores/mysql/ads.md`） |
| MinIO | 平台级 + 本域引用 |
| RDBMS | 仅 MySQL |
| 功能设计 | 不进本树 |
| 流图会签 | **approved** · `human:淮政玮` · 2026-08-12 |
| Demo/Mock | **主路径** LLM→约定 ODS→ETL 模拟 GDF；落 `demo_*`；结构共用 stores；少量覆盖、先闭环 |

## 会签完成

- Task：`ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01`  
- Handoff：`agent-delivery/agent-handoffs/企业战略分析-ENT/ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01.md`  
- 下游：**S2/S3 放行**；`stores/*` 细表仍不得仅凭流图标 approved

## 已完成 · S2

- Task：`DATA-ENT-STORAGE-S2-L01` = **done**  
- 范围：sources + etl 指针 + seeds；三方 ODS 权威 `doc/`、优先读 `md-extract/`

## 进行中 · S3

- Task：`DATA-ENT-STORAGE-S3-L01`（**in_progress** · `human:淮政玮`）  
- 说明 / handoff：`…/DATA-ENT-STORAGE-S3-L01-派单说明.md` · `…/DATA-ENT-STORAGE-S3-L01.md`  
- 范围：`stores/mysql|es|nebula` as-built 清单与指针；细表 **draft**

## 目录状态

| 路径 | 状态 |
|---|---|
| `00-context.md` | draft 骨架 |
| `01-data-flow.md` | **approved** |
| `etl/pipeline-demo-mock.md` | **approved** · S2 命名表已填 |
| `sources/` `etl/` `seeds/` | **S2 done** |
| `stores/` | **S3 已灌入** · 细表 draft（待结构评审） |
| `CHANGELOG.md` | 启用 |
