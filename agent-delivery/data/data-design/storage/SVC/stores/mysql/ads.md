# MySQL ADS · 服务机构契约面

```yaml
---
doc_id: SVC-STORE-ADS
element: SVC
role: store-mysql
status: draft
version: "2026-08-19"
updated: "2026-08-19"
engine: mysql
s3_task: DATA-SVC-STORAGE-S3-L02
---
```

> **必须文档**。阶段 P：Java **只读**本层。阶段 F：50100 → `demo-algo-ent-analysis` 直写 Demo ADS（联调台，不冒充产品链）。  
> **库名**：正式 `gkxlumenx_ads`（本总控零写）；Demo **`demo_gkxlumenx_ads`**。  
> **status=draft**。指标 8 件套真源仍是 metrics 体系；本文件只列物理表。  
> **DDL**：[`ddl-demo-empty.sql`](./ddl-demo-empty.sql)。

## 1. 写读矩阵

| 写 | 读 |
|---|---|
| Python（阶段 F：`demo-algo-ent-analysis`）；禁止 Java/前端写 | 阶段 P：Java 只读；阶段 F：50100 读 Demo ADS |

禁止三方 ODS 字段泄漏进契约面（D7）。禁止 `svcModelCatalog` / GraphView 内置节点充数。

## 2. 基础指标 A1–A6（招标 § 服务机构基础指标 · 不是十模型）

metric_id 对齐 `metrics/metric-readiness-matrix-SVC.yaml`。

| 招标项 | metric_id | 物理表 | 切片 |
|---|---|---|---|
| A1 全球服务机构产业布局 | `M_SVC_INDUSTRY_LAYOUT` | `svc_metric_dist` | 产业/六类候选 × 规模 |
| A2 全球服务机构分布 | `M_SVC_ORG_CNT` | `svc_region_dist` | `geo_level=country`（无国家则 `province` 诚实降级） |
| A3 投融资动态资讯 | `M_SVC_INVEST_Y` | `svc_metric_series` | 年 × 金额；无事件则 0 行 + 待核验 |
| A4 新增服务机构动态 | `M_SVC_NEW_CNT` | `svc_metric_series` | 年 × 新增数（ODS `incorporation_date` 聚合，不拷进 DWD 主体） |
| A5 深圳服务机构规模 | `M_SVC_SZ_SCALE` | `svc_metric_fact` | 单卡 KPI |
| A6 深圳服务机构分布 | `M_SVC_SZ_DISTRICT` | `svc_region_dist` | `geo_level=sz_district`（ODS `area`；Q-SVC-004） |

`svc_metric_fact` 也可承载 A1–A6 的卡片快照（`metric_id` + `value` + `period` + `etl_batch_id`）。

## 3. 十模型回写（招标 §9 · 出数铁律：读本表 → 算 → 回写）

| 模型 ID | 物理表 | 口径备注 |
|---|---|---|
| `SVC_SERVICE_CHAIN_GAP` | `svc_chain_gap` | **运行时 Q-SVCCHAIN-03**：`runtime_flag` = `blank`(0 家) / `weak`(≤1) / `bottleneck`(均深&lt;55)。`q061_score` **对照列** + `q061_pending_client=1`；F-ALGO **不得**用 Q061 切运行时 |
| `SVC_SERVICE_RELATION_CHAIN` | `svc_relation_chain` | Q062 🟡；图边在 `demo_gkx_chain`，本表存密度/中心性等结果 |
| `SVC_FINANCE_TECH_POWER` 等 ×6 | `svc_tech_power_score` | Q060 五维等权；`model_id` 区分六类 |
| `SVC_ATTRACTION_RECOMMEND` | `svc_attraction_recommend` | Q063 🟡 |
| `SVC_CULTIVATION_RECOMMEND` | `svc_cultivation_recommend` | Q063 🟡 |

公共列（各模型表）：`org_id`（可空：短板按环节汇总时用 `stage_code`）、`calc_batch_id`、`model_version`、`weights` JSON、`ext` JSON、`update_time`。

六类 `model_id`：`SVC_FINANCE_TECH_POWER` / `SVC_IP_TECH_POWER` / `SVC_HR_TECH_POWER` / `SVC_MKT_TECH_POWER` / `SVC_CONSULT_TECH_POWER` / `SVC_INNOV_TECH_POWER`。

## 4. 与 DWD / 图

- 圈定原料：[`dwd-svc.md`](./dwd-svc.md) `svc_org_circle`。  
- 图：hang [`../nebula/graph-svc.md`](../nebula/graph-svc.md)；**不要**用 ADS 当边真源。  
- A3 事件 hang：`svc_org_finance_event`（可空）。

## 5. 禁止

- 前端/Java 造假写 ADS  
- 把 DWD 圈定表伪装成对外契约  
- 细表仅因流图会签标 `approved`  
- 短板运行时切到 Q061  
- 平行 `gkx_ads.ads_model_score` 第二套冒充本树（旧稿仅对照）
