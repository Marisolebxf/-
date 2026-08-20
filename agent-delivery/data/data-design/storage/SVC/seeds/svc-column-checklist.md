# SVC Demo 列清单（规则 A + 卡面 B · 给人看一眼）

> **任务**：`DATA-SVC-STORAGE-PATCH-L02`  
> **读者**：`human:淮政玮`（看列过，不再会签流图）  
> **本页不灌数、不改 §1 工厂拓扑边。** 细表仍 **draft**。

```yaml
---
doc_id: SVC-COLUMN-CHECKLIST
element: SVC
role: seed-config
status: draft
version: "2026-08-20"
updated: "2026-08-20"
task_id: DATA-SVC-STORAGE-PATCH-L02
---
```

卡面 B（已落 `DATA-SVC-STORAGE-CARD-L02`）**维持**：名单走 ADS `svc_org_card`，线上不联 ODS。

---

## 1. 圈定扫描（只读 ODS，不落主体）

源：`demo_gkxlumenx_ods.dwd_org_base_info`（禁止 `gkxlumenx_ods` 当 F-SEED 源；禁止 `enterprise_*`）。

| 列 | 用途 |
|---|---|
| `org_id` | hang 键 |
| `name_cn` | 圈定 + 卡面投影 |
| `industry` | 圈定 / 分类 / 卡面投影 |
| `industry_l1_name` … `industry_l4_name` | 圈定 / 分类（有则扫） |
| `industry_l*_code` | 有则扫（名称/编码样例可能对调） |
| `business_scope` | 有则扫；Demo 主表**无此列** |
| `province` / `city` / `area` | **不参与圈定**；灌数投影卡面 / A2 A5 A6 |
| `district` | 仅当无 `area` 时写入卡面 `area`（Q-SVC-004） |
| `incorporation_date` / `incorporation_year` | A4；不拷 DWD |
| `org_size` | A5 可选；无列则省略 |
| `is_deleted` | 有则排除已删 |

**禁止扫描**：`org_type`（工商组织形式）；`dwd_org_tech_tag`。

规则：[`svc_rule_demo_kw_v1.md`](./svc_rule_demo_kw_v1.md) **v1.1**。

---

## 2. DWD `demo_gkxlumenx_dwd.svc_org_circle`

不是机构主表。只 hang。

| 列 | 说明 |
|---|---|
| `org_id` | UK；与 ODS/ENT 同一键 |
| `rule_version` | `svc_rule_demo_kw_v1.1` |
| `hit_fields` | JSON，命中的 ODS 列名 |
| `service_type_candidate` | 六类或 **空** |
| `pending_client_confirm` | **恒 1** |
| `etl_batch_id` | 灌数批次 |
| `ext` | 可选（如 `fallback_all_ods`） |

禁止平行 `svc_org_base`；禁止拷 `dwd_org_base_info` 全列。

---

## 3. ADS `demo_gkxlumenx_ads.svc_org_card`（选 B）

线上名单/详情只读本表。

| 列 | 来源 |
|---|---|
| `org_id` | circle |
| `name_cn` | ODS 同名列（灌数 JOIN **一次**） |
| `province` / `city` | ODS 同名列 |
| `area` | 优先 ODS `area` |
| `industry` | ODS `industry`；无列则空 |
| `service_type_candidate` | circle |
| `pending_client_confirm` | 1 |

禁止：地址/资本/法人等工商全列；50100/50892 **现拼 ODS**。

---

## 4. 同一批还写什么（本页只点名，细对照另文件）

| 表 | 何时 |
|---|---|
| `svc_org_finance_event` | A3 hang；可 0 行 |
| `svc_metric_dist` / `svc_region_dist` / `svc_metric_series` / `svc_metric_fact` | A1–A6 |
| 十模型 / `svc_org_graph_hang` / Nebula | **F-ALGO**，本清单不要求 |

列对照：[`../etl/ods-to-dwd-mapping.md`](../etl/ods-to-dwd-mapping.md) · [`../etl/ods-to-ads-mapping.md`](../etl/ods-to-ads-mapping.md)。
