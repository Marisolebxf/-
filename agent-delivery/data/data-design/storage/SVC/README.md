# 服务机构维（SVC）存储设计 — 入口

> **读我**：本目录是服务机构维存储与数据工程的**现行入口**（并行于 `data-design/服务机构/` legacy）。  
> **规范**：[`../README.md`](../README.md)（与 ENT / CHAIN 共用体系；本域同构落地）  
> **流图会签**：架构师 · Owner `human:侯佳伟` · 文件 [`01-data-flow.md`](./01-data-flow.md)

```yaml
---
doc_id: SVC-STORAGE-INDEX
element: SVC
role: index
status: draft
version: "2026-08-14"
updated: 2026-08-18
---
```

## 读序（强制）

1. [`00-context.md`](./00-context.md) — 边界与铁律（**不复制**机构主数据）  
2. [`01-data-flow.md`](./01-data-flow.md) — 数据流图（**已会签 approved · 2026-08-14 · human:侯佳伟**）  
3. [`sources/`](./sources/) — 第三方 / ODS 入站（S1 占位；S2 表级清单）  
4. [`etl/`](./etl/) — 工厂与派生管道（**主**：[`pipeline-demo-mock.md`](./etl/pipeline-demo-mock.md)）  
5. [`seeds/`](./seeds/) — 少量覆盖样例索引  
6. [`stores/`](./stores/) — MySQL（含 **ADS**）· ES · Nebula（**S3** 灌；细表不得仅凭流图标 approved）  
7. MinIO → [`../platform/minio.md`](../platform/minio.md) + etl 索引（S2 补 `pipeline-to-minio`）

## 已锁定

| 项 | 值 |
|---|---|
| 根路径 | `data-design/storage/SVC/` |
| ADS | **必须**进入本树（S3 灌清单；细表不得仅凭流图标 approved） |
| MinIO | 平台级 + 本域引用 |
| RDBMS | 仅 MySQL |
| 图谱 | 仅 NebulaGraph |
| ODS 真源 | **权威** `third-party-source/doc/` xlsx；**优先读** `doc/md-extract/`（国内机构要素库） |
| Demo ODS | `demo_gkxlumenx_ods`（与 ENT **同实例复用**；禁默认写正式 `gkxlumenx_ods`） |
| 机构主体 | **权威在 ENT**；本域 **不复制** `dwd_org_base_info` |
| 本域只保留 | 服务机构圈定规则、关系、本域 ADS / ES；图谱挂接到一张 G |
| 功能设计 | 不进本树（E7 五件套不重跑） |
| 流图会签 | **approved** · `human:侯佳伟` · 2026-08-14 |
| Demo/Mock | 主路径：约定 ODS → ETL 模拟 GDF；落 `demo_*` |
| 一张 G | 服务机构点/边 → `demo_gkx_chain`（决策 #7）；`demo_gkx_svc` 不是第二张图 |

## 任务

| 阶段 | Task | 状态 |
|---|---|---|
| S1 | `ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01` | **approved** · 流图已签（本地未 push）· 放行 S2 |
| S2 | `DATA-SVC-STORAGE-S2-L01` | **本地签收 approved**（侯佳伟 · 2026-08-14 · 未 push）· 已放行 S3 |
| S3 | `DATA-SVC-STORAGE-S3-L01` | **本地签收**（放行 S4 · 未 push）· stores draft |
| S4 | `DATA-SVC-STORAGE-S4-L01` | **本地 stub 已交**（2026-08-17 · 未 push） |
| DDL | `DATA-SVC-STORAGE-DDL-L01` | **本地字段级 draft**（2026-08-17 · 排除数据口径 · 未 push） |
| **A 退出门** | `DEMO-SVC-A-RECLOSE-L01` | **2026-08-18 live 重跑** · ODS aligned · MOCK 24 · 管线文档 as-built |

## 目录状态

| 路径 | 状态 |
|---|---|
| `00-context.md` | draft · S1 |
| `01-data-flow.md` | **approved** |
| `etl/pipeline-demo-mock.md` | **as-built** · A-RECLOSE 已钉脚本+live 证据 |
| `sources/inventory.md` | draft · S2 33 表 + industry* 证据 |
| `seeds/README.md` | draft · S2 覆盖矩阵骨架（待核验） |
| `stores/` | S3 清单 + **DDL-L01 字段级**（mysql dwd/ads/dim draft） |
| `etl/demo_gkxlumenx_dwd_svc_tables.sql` | CREATE 草稿（禁默认真 APPLY 正式库） |
| `CHANGELOG.md` | 启用 |

## 与 ENT / CHAIN 边界（一句话）

- **ENT**：机构主体权威（`dwd_org_base_info` 及国内机构要素库主表）。  
- **CHAIN**：产业链节点/标签/资讯；禁复制 CHAIN 数据模型到 SVC 图谱。  
- **SVC**：在 ENT 主体之上做**圈定 + 关系 + 本域切片**；圈定规则受 **Q-SVC-010** 阻断，S1 **不伪闭合**。
