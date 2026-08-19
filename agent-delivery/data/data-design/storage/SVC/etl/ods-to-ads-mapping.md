# SVC · ODS → ADS 列对照（A1–A6 · OPEN 聚合缺口）

> **任务**：`DATA-SVC-STORAGE-GAP-L02`  
> **用途**：F-SEED 聚合时禁止猜列。本文件**只写对照**，不灌数、不执行 DDL。  
> **人口**：先 `demo_gkxlumenx_dwd.svc_org_circle` hang 的 `org_id`，再 **JOIN** ODS 取属性。禁止把主体拷进 DWD。  
> **结构真源**：md-extract 国内机构要素库。Q-SVC-009：live 可能缺 `industry*`——列不存在则跳过该粒度，不伪造。

```yaml
---
doc_id: SVC-ETL-ODS-ADS-MAPPING
element: SVC
role: etl
status: draft
version: "2026-08-19"
updated: "2026-08-19"
task_id: DATA-SVC-STORAGE-GAP-L02
---
```

人口 SQL 形态（示意，非作业）：

```text
FROM demo_gkxlumenx_dwd.svc_org_circle c
JOIN demo_gkxlumenx_ods.dwd_org_base_info o ON o.org_id = c.org_id
```

---

## 公共降级

| 条件 | 做法 |
|---|---|
| 圈定 0 行 | ADS 对应指标 **0 行**；不伪池 |
| 命中 &lt;10 | 按 Q-SVC-010：**退回全表**仍一律 `pending_client_confirm`；不伪闭合 live |
| ODS 缺列 | 跳过依赖该列的粒度；`ext.missing_cols` 记下 |
| `org_type` | **禁止**准入 / 六类 |

---

## A1 `M_SVC_INDUSTRY_LAYOUT` → `demo_gkxlumenx_ads.svc_metric_dist`

| 目标列 | 来源 | 规则 |
|---|---|---|
| `metric_id` | 常量 | `M_SVC_INDUSTRY_LAYOUT` |
| `category`（六类粒） | `c.service_type_candidate` | `COUNT(*)`；候选来自 [`../seeds/svc_rule_demo_kw_v1.md`](../seeds/svc_rule_demo_kw_v1.md) |
| `category`（产业粒） | ODS `industry`；空则 `industry_l2_name` | 有列才写；Q-SVC-009 无列则**只留六类粒** |
| `value` | 上计 | 机构数 |
| `ext.org_size` | ODS `org_size` | 可选直方图；无列则省略 |

禁止用国民经济代码当服务六类。

---

## A2 `M_SVC_ORG_CNT` → `demo_gkxlumenx_ads.svc_region_dist`

ODS **无国家列**。

| 目标列 | 来源 | 规则 |
|---|---|---|
| `metric_id` | 常量 | `M_SVC_ORG_CNT` |
| `geo_level` | 常量 | **`province`**（诚实降级；不要写 `country` 冒充全球国家） |
| `region_name` | ODS `province` | `GROUP BY`；空省丢弃或标 `(unknown)` 须进 `ext` |
| `org_count` | `COUNT(*)` | 圈定人口 |

卡片快照可另写 `svc_metric_fact`（`slice_key=all`，值为圈定总数）。

---

## A3 `M_SVC_INVEST_Y` → `svc_org_finance_event` hang + `svc_metric_series`

事件 hang 列对照见 [`ods-to-dwd-mapping.md`](./ods-to-dwd-mapping.md) §3（已钉融资/投资列名）。ADS：

| 目标 | 规则 |
|---|---|
| 人口 | `event.org_id ∈ circle` |
| `svc_metric_series.metric_id` | `M_SVC_INVEST_Y` |
| `period` | `YEAR(event_date)`；**无日期的行不进时序**（不编年） |
| `value` | `SUM(amount)`；金额空当 0 仍计年，或跳过——F-SEED 须二选一并写 `ext` |
| 0 事件 | 0 行 + 待核验；Q-SVC-006 **不伪闭合 live** |

---

## A4 `M_SVC_NEW_CNT` → `svc_metric_series`

| 目标 | 来源 | 规则 |
|---|---|---|
| 人口 | 圈定 JOIN 主表 | |
| `period` | `YEAR(incorporation_date)`；空则 `incorporation_year` | 两者皆空跳过 |
| `value` | `COUNT(*)` | 仅圈定内 |

---

## A5 `M_SVC_SZ_SCALE` → `svc_metric_fact`

| 目标 | 规则 |
|---|---|
| 过滤 | ODS `city` ∈ {`深圳`, `深圳市`} |
| `metric_id` | `M_SVC_SZ_SCALE` |
| `value` | 过滤后 `COUNT(*)` |
| `period` | 灌数批次年或 `all`；写进 `ext.filter=city` |

规模四档若用 `org_size`：可附加 `svc_metric_dist`（`metric_id` 仍 A5 或放 `ext`）；无列则只出总数。

---

## A6 `M_SVC_SZ_DISTRICT` → `svc_region_dist`

| 目标列 | 来源 | 规则 |
|---|---|---|
| 过滤 | 同 A5 `city` | |
| `metric_id` | 常量 | `M_SVC_SZ_DISTRICT` |
| `geo_level` | 常量 | `sz_district` |
| `region_name` | **优先** md-extract `area`；若 live 仅有 `district`（Q-SVC-004 🟢）则用 `district` | 两列都无则 0 行，禁止从 `address` 解析冒充 |
| `org_count` | `COUNT(*)` | |

---

## 禁止

- 把本对照当 8 件套已 aligned / D4 live  
- `SELECT enterprise_*` 当聚合源  
- 拷 ODS 全列进 DWD 再聚合  
- 本单 50100 / 连库执行
