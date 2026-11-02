# 服务机构维（SVC）存储设计 — 入口

> **读我**：本目录是服务机构维存储与数据工程的**现行入口**（2026-08-18 范围 3 整树删除后，阶段 F 重建）。  
> **规范**：[`../README.md`](../README.md)  
> **流图会签**：Owner **`human:淮政玮`** · 文件 [`01-data-flow.md`](./01-data-flow.md)（**approved · 2026-08-19**）  
> **人选 B（2026-08-20）**：名单卡面 [`stores/mysql/ads.md`](./stores/mysql/ads.md) `svc_org_card`；人主看图 [`01-data-flow.md`](./01-data-flow.md) **§1.1**（`SVC-STORAGE-LINEAGE`）。§1 工厂拓扑未改。  
> **规则 A（2026-08-20）**：圈定 [`seeds/svc_rule_demo_kw_v1.md`](./seeds/svc_rule_demo_kw_v1.md) `v1.1`；淮总看列 [`seeds/svc-column-checklist.md`](./seeds/svc-column-checklist.md)。不再会签流图。  
> **本阶段**：**S1–S4 文档闭环** + 缺口 / 卡面 + **规则 A 列清单**（`DATA-SVC-STORAGE-PATCH-L02`）。细表仍 **draft**。  
> **2026-11-02 现网对照**：[`02-asbuilt-process-chain.md`](./02-asbuilt-process-chain.md)（`SYSINT-06-21-01-L02`，draft，待会签）。demo 库已有圈定行；正式库同名表 0 行；GDF 作业未建。这不是细表 approved，也不是产线跑通。  
> **不要**：把「文档闭环 / 列清单」当成灌数完成或细表 approved。  
> **灌数**：F-SEED = `DEMO-SVC-LAB-SEED-L01`（本入口不执行 50100）。  
> **F-GATE 冻结**：[`formula-freeze-cut-a.md`](./formula-freeze-cut-a.md)（切法 A · `DEMO-SVC-LAB-GATE-L01`）。**不是**授权开 50892。  
> **细表不得**仅因流图会签或本入口标 `approved`。

```yaml
---
doc_id: SVC-STORAGE-INDEX
element: SVC
role: index
status: draft
version: "2026-11-02"
updated: 2026-11-02
s4_task: DATA-SVC-STORAGE-S4-L02
gap_task: DATA-SVC-STORAGE-GAP-L02
card_task: DATA-SVC-STORAGE-CARD-L02
---
```

## 读序（强制）

1. [`00-context.md`](./00-context.md) — 边界与铁律  
2. [`01-data-flow.md`](./01-data-flow.md) — 数据流图（**会签 approved · 2026-08-19**）+ **§1.1 表级血缘（人选 B · 人主看图）**。2026-11-02 只加了待会签对照，未改 `signoff_status`，未改 §1 工厂拓扑图  
2b. [`02-asbuilt-process-chain.md`](./02-asbuilt-process-chain.md) — 现网加工链路、分场景流程图、指标库对照（draft · `SYSINT-06-21-01-L02`）  
3. [`sources/inventory.md`](./sources/inventory.md) — ODS 表级清单（33 表与 ENT 共用；本波读法）  
4. [`etl/pipeline-demo-mock.md`](./etl/pipeline-demo-mock.md) — 模拟 GDF 指针（**不灌数**）  
4b. [`etl/pipeline-to-nebula.md`](./etl/pipeline-to-nebula.md) — **112/113 图谱契约**（A/B/C/D · 灌数零图谱 · `SVC-GRAPH-TRIPLE`；**不灌数**）  
5. [`etl/ods-to-dwd-mapping.md`](./etl/ods-to-dwd-mapping.md) — OPEN-06：ODS 贴源 → SVC DWD hang  
6. [`etl/ods-to-ads-mapping.md`](./etl/ods-to-ads-mapping.md) — A1–A6 ODS→ADS **列对照**  
7. [`seeds/svc_rule_demo_kw_v1.md`](./seeds/svc_rule_demo_kw_v1.md) — 六类临时词表 v1.1（规则 A · Q-SVC-010）  
7b. [`seeds/svc-column-checklist.md`](./seeds/svc-column-checklist.md) — 圈定/circle/card 列清单（给人看一眼）  
8. [`seeds/README.md`](./seeds/README.md) — 覆盖矩阵骨架  
9. [`stores/`](./stores/README.md) — DWD/ADS/图 hang（**draft** · `DATA-SVC-STORAGE-S3-L02`）  
10. [`etl/pipeline-to-minio.md`](./etl/pipeline-to-minio.md) — 前缀 `svc/{task_id}/`（平台正文不复制）  
11. [`formula-freeze-cut-a.md`](./formula-freeze-cut-a.md) — F-GATE 切法 A（P 总控才消费；本文件不施工 50892）

## 已锁定（流图已会签；文档闭环 ≠ 灌数）

| 项 | 值 |
|---|---|
| 根路径 | `data-design/storage/SVC/` |
| ADS | 必须 · S3 draft（**卡面 `svc_org_card`** + A1–A6 + 十模型） |
| MinIO | 平台级 + 本域引用 |
| RDBMS | 仅 MySQL |
| Demo ODS | 共用 `demo_gkxlumenx_ods`（不新建、不 DROP 约定 33 表） |
| 圈定 | `svc_rule_demo_kw_v1.1`（规则 A）· Q-SVC-010 🟡 · 主读 ODS `dwd_org_base_info` |
| 主体 | hang ENT `org_id`；禁 `svc_org_base`；禁复制 `dwd_org_base_info` 全列 |
| 一张 G | hang `demo_gkx_chain`（决策 #7）；禁平行 `gkx_service` |
| 阶段 F 写库 | `demo-algo-ent-analysis` ← 50100；不碰 lumen 四仓 |
| 短板 Demo | 运行时 **Q-SVCCHAIN-03**；Q061 对照列 |
| 流图会签 | **approved** · `human:淮政玮` · 2026-08-19 |
| S1–S4 | **文档闭环** · `DATA-SVC-STORAGE-S4-L02` |
| CHAIN | 冻结，不改 |

## 缺口已补文档（灌数引擎仍另开）

`DATA-SVC-STORAGE-GAP-L02` **已写**下列文档。**不等于** 50100 / F-SEED 完成。引擎开工读这些文件，不要猜列、不要另造词表。

| 项 | 落盘 | 仍禁止 |
|---|---|---|
| A1–A6 ODS→ADS **列对照** | [`etl/ods-to-ads-mapping.md`](./etl/ods-to-ads-mapping.md) | 当 8 件套 aligned |
| `svc_rule_demo_kw_v1` **六类词表** | [`seeds/svc_rule_demo_kw_v1.md`](./seeds/svc_rule_demo_kw_v1.md) | 当 live 准入 / 关闭 Q-SVC-010 |
| `pipeline-to-minio.md` | [`etl/pipeline-to-minio.md`](./etl/pipeline-to-minio.md) | 本文件写现网密钥 |
| 指标矩阵血缘 | `metrics/registry/metric-readiness-matrix-SVC.yaml` 改指 `svc_metric_*` / `demo_gkx_chain` | 改绿 D1/D4 |

## 废作对照

旧叶 `ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01` / 旧 `DATA-SVC-STORAGE-S4-L01` 及旧 `storage/SVC/` 已随范围 3 删除/废作。**不以旧 approved 当本轮会签。**  
旧稿目录：[`../../服务机构/README.md`](../../服务机构/README.md) → 强制导航本树。
