# MySQL DWD · 企业指标 / 预聚合

```yaml
---
doc_id: ENT-STORE-DWD-AGG
element: ENT
role: store-mysql
status: draft
version: "2026-08-12"
updated: "2026-08-12"
engine: mysql
as_built_source: data-design/企业/DWD表结构设计-企业指标汇总表-MySQL-v3.1.md
as_built_source_extra: data-design/企业/DWD表结构设计-企业模块-MySQL-v3.0.md
s3_task: DATA-ENT-STORAGE-S3-L01
---
```

> **主真源**：[`DWD表结构设计-企业指标汇总表-MySQL-v3.1.md`](../../../企业/DWD表结构设计-企业指标汇总表-MySQL-v3.1.md)  
> **补充**：`enterprise_distribution` / `sz_city_benchmark` 见模块 MySQL-v3.0（非旧版摘编 8 表内）。  
> **不是**指标 8 件套目录（仍认 `metrics/*` + data-lineage-policy）。

## 1. 预聚合表清单

| 表名 | 粒度（摘要） | 用途 |
|---|---|---|
| `enterprise_region_summary` | region × type × stat_date | 区域 KPI / 热力 |
| `enterprise_industry_distribution` | region × chain × stat_date | 区内产业分布 |
| `enterprise_growth_trend` | region × year × month × stat_date | 月度增长 |
| `enterprise_industry_summary` | chain × year × stat_date | 产业 KPI（`chain_code='ALL'` 去重行） |
| `enterprise_stat_summary` | stat_type × dim × year × stat_date | 通用单维统计 |
| `enterprise_type_scale_stats` | type × scale × region × stat_date | 三维交叉 |
| `shenzhen_enterprise_summary` | 深圳专题统计 | 深圳介绍 |
| `enterprise_risk_summary` | org_id × risk_type | 检索风险筛选 / 详情计数 |
| `enterprise_org_type` | org × 机构类型 | 2026-08-12 新增 |
| `enterprise_distribution` | 见 v3.0 | 分布类（模块文档） |
| `sz_city_benchmark` | 见 v3.0 | 城市对标 |

## 2. 关键纠偏（指针）

- `enterprise_risk_summary`：2026-08-12 长表重建（`UNIQUE(org_id, risk_type)`）；详见指标汇总 §3.8 / §7。  
- 跨产业总数禁止简单相加产业行。

## 3. 明确排除（勿当 DWD 汇总）

| 表 | 去向 |
|---|---|
| `enterprise_score` 等算法结果 | [`ads.md`](./ads.md) |
| `enterprise_star` | 配置/运营，非本层预聚合 |

## 4. 禁止

粘贴整份 DDL；把统计表当 ADS 契约面直接给 Java（须经 ADS/API 门面或既定只读约定）。
