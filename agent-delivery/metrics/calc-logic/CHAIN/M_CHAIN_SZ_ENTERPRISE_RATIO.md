---
metric_id: M_CHAIN_SZ_ENTERPRISE_RATIO
metric_name_zh: 深圳产业链企业占比
algorithm_type: STAT
version: 0.2.0
updated: 2026-10-14
owner: data-agent / human:淮政玮
status: 口径已定（单趟条件聚合）
---

# M_CHAIN_SZ_ENTERPRISE_RATIO 深圳产业链企业占比 — 计算逻辑说明

> 2026-10-14 human:徐滕强 拍板：单趟条件聚合。父指标 `M_CHAIN_SZ_ENTERPRISE_COUNT`（分子）与 `M_CHAIN_ENTERPRISE_COUNT`（分母）均 v0.2.0 已定，本条为其派生比。

## 1. 业务定义

深圳产业链关联企业数占全国该链企业总数比例 × 100。

**为什么单趟**：分子分母同 JOIN、同 `base_info.is_deleted=0` 软删、同 `chain_code` 参数——一趟内 `CASE WHEN` 分流，天然同过滤口径，杜绝两次查询间口径漂移。

## 2. 数据源

| 表 | 用途 |
|---|---|
| `demo_gkxlumenx_dwd.enterprise_industry_chain` | 上链桥（`chain_code=:chain_code`） |
| `demo_gkxlumenx_ods.dwd_org_base_info` | 深圳判定（`city='深圳市'`）+ 软删（`is_deleted=0`） |

## 3. SQL

```sql
SELECT ROUND(100 * COUNT(DISTINCT CASE WHEN b.city = '深圳市' THEN eic.org_id END)
                 / COUNT(DISTINCT eic.org_id), 2) AS sz_enterprise_ratio_pct
FROM demo_gkxlumenx_dwd.enterprise_industry_chain eic
JOIN demo_gkxlumenx_ods.dwd_org_base_info b
  ON b.org_id = eic.org_id AND b.is_deleted = 0
WHERE eic.chain_code = :chain_code;
```

注：`enterprise_industry_chain` 表 DDL 实核无 `is_deleted`，不加该表软删过滤（与 `M_CHAIN_SZ_ENTERPRISE_COUNT` 口径一致）。

## 4. 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `:chain_code` | 产业链编码 | 必填 |

## 5. 边界语义

- 分母 0（该链无上链企业）→ NULL（MySQL 除零），UI 显「无数据」，不伪造 0%。
- 上链桥当前 0 行 → NULL，如实展示。

## 6. 版本与变更

| 版本 | 日期 | 变更 | 拍板 |
|---|---|---|---|
| 0.1.0 | — | 旧稿：两父指标相除（无 SQL 本体） | — |
| 0.2.0 | 2026-10-14 | 单趟条件聚合定版 + 同过滤口径说明 | human:徐滕强 |

正式签名待 human:唐绍祖 会签。
