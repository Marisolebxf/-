# 服务机构维（SVC）存储设计 — 入口

> **读我**：本目录是服务机构维存储与数据工程的**重建入口**（2026-08-18 范围 3 整树删除后，本轮阶段 F 重开）。  
> **规范**：[`../README.md`](../README.md)  
> **流图会签**：Owner **`human:淮政玮`** · 文件 [`01-data-flow.md`](./01-data-flow.md)（**approved · 2026-08-19**）  
> **本阶段**：流图已会签。S2 指针 + **S3 stores 细表 draft**（含 OPEN-06 映射与 Demo 空表 CREATE）。  
> **不要**：把本目录当成「建设完成」；S4 才会把 `storage/README.md` 的 SVC 行标绿。  
> **仍禁止**：50100 灌数 / F-SEED（须本树契约表；S4 入口后再开灌数叶）。  
> **细表不得**仅因流图会签标 `approved`。

```yaml
---
doc_id: SVC-STORAGE-INDEX
element: SVC
role: index
status: draft
version: "2026-08-19"
updated: 2026-08-19
---
```

## 读序（强制）

1. [`00-context.md`](./00-context.md) — 边界与铁律  
2. [`01-data-flow.md`](./01-data-flow.md) — 数据流图（**会签 approved · human:淮政玮 · 2026-08-19**）  
3. [`sources/inventory.md`](./sources/inventory.md) — ODS 表级清单（33 表与 ENT 共用）  
4. [`etl/pipeline-demo-mock.md`](./etl/pipeline-demo-mock.md) — 模拟 GDF 指针（**不灌数**）  
5. [`etl/ods-to-dwd-mapping.md`](./etl/ods-to-dwd-mapping.md) — OPEN-06：ODS 贴源 → SVC DWD  
6. [`seeds/README.md`](./seeds/README.md) — 覆盖矩阵骨架  
7. [`stores/`](./stores/README.md) — DWD/ADS/图 hang（**draft** · `DATA-SVC-STORAGE-S3-L02`）  
8. MinIO → [`../platform/minio.md`](../platform/minio.md)

## 已锁定（流图已会签；放行 S2 拓扑，不放行灌数）

| 项 | 值 |
|---|---|
| 根路径 | `data-design/storage/SVC/` |
| ADS | 必须 · S3 draft（A1–A6 + 十模型） |
| MinIO | 平台级 + 本域引用 |
| RDBMS | 仅 MySQL |
| Demo ODS | 共用 `demo_gkxlumenx_ods`（不新建、不 DROP 约定 33 表） |
| 圈定 | `svc_rule_demo_kw_v1` · Q-SVC-010 🟡 |
| 主体 | hang ENT `org_id`；禁 `svc_org_base`；禁复制 `dwd_org_base_info` 全列 |
| 一张 G | hang `demo_gkx_chain`（决策 #7）；禁平行 `gkx_service` |
| 阶段 F 写库 | `demo-algo-ent-analysis` ← 50100；不碰 lumen 四仓 |
| 短板 Demo | 运行时 **Q-SVCCHAIN-03**；Q061 对照列 |
| 流图会签 | **approved** · `human:淮政玮` · 2026-08-19 |
| CHAIN | 冻结，不改 |

## 废作对照

旧叶 `ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01` 及旧 `storage/SVC/` 已随范围 3 删除/废作。**不以旧 approved 当本轮会签。**
