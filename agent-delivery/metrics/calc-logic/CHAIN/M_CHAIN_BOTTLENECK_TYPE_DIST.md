---
metric_id: M_CHAIN_BOTTLENECK_TYPE_DIST
metric_name_zh: 瓶颈类型分布
algorithm_type: STAT
version: 0.2.0
updated: 2026-10-14
owner: data-agent / human:淮政玮
status: 口径已定（metric_dist 桶直读）
---

# M_CHAIN_BOTTLENECK_TYPE_DIST 瓶颈类型分布 — 计算逻辑说明

> 2026-10-14 human:徐滕强 拍板：读表口径。本条是 ADS v2 §6 中**唯一**映射到 `metric_dist`（分布表）的指标，读桶行。

## 1. 业务定义

指定产业链瓶颈按类型的分布计数（类型码 / 类型名 / 计数 / 占比，桶行直读）。

## 2. 表体系

| 层 | 表 | 说明 |
|---|---|---|
| 发布消费 | ADS v2 `demo_gkxlumenx_ads.industry_chain_metric_dist` | 桶结构：`bucket_code` / `bucket_name` / `bucket_value` / `bucket_ratio`；v2 §6 唯一分布映射 |
| 模型原子分 | DWD v5 `industry_chain_model_result_detail` | `dimension_code` 维度行（tech/talent/market/capital/policy），指标引擎聚合写桶 |

## 3. SQL

```sql
SELECT d.bucket_code, d.bucket_name, d.bucket_value, d.bucket_ratio
FROM demo_gkxlumenx_ads.industry_chain_metric_dist d
WHERE d.is_deleted = 0 AND d.publish_status = 'published'
  AND d.metric_id = 'M_CHAIN_BOTTLENECK_TYPE_DIST'
  AND d.object_type = 'chain' AND d.object_id = :chain_code
ORDER BY d.bucket_value DESC;   -- 最新发布批次；0 行 → 无数据
```

## 4. 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `:chain_code` | 产业链编码（INB） | 必填 |

## 5. 随附待办（不挡口径）

- 五维字典（技术/人才/市场/资本/政策）与一瓶颈多类型计数方式（展开 vs 主类型）：QC04 / 模型卡冻结后指标引擎按字典写桶——影响**写哪些桶**，不影响读 SQL。

## 6. 版本与变更

| 版本 | 日期 | 变更 | 拍板 |
|---|---|---|---|
| 0.1.0 | — | 旧稿：GROUP BY bottleneck_type 对 v1 废弃壳 | — |
| 0.2.0 | 2026-10-14 | metric_dist 桶直读定版 | human:徐滕强 |

正式签名待 human:唐绍祖 会签。
