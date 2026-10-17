---
metric_id: M_CHAIN_SZ_PROBLEM_COUNT
metric_name_zh: 深圳产业问题数
algorithm_type: STAT
version: 0.2.0
updated: 2026-10-14
owner: data-agent / human:淮政玮
status: 口径已定（读表口径 + 440300 等值切片）
---

# M_CHAIN_SZ_PROBLEM_COUNT 深圳产业问题数 — 计算逻辑说明

> 2026-10-14 human:徐滕强 拍板：读表口径，`region_code='440300'` 等值切片（旧稿 `LIKE '4403%'` 基于废弃壳表，连同前缀匹配一并废止）。

## 1. 业务定义

深圳在指定产业链被诊断出的问题/短板数（发布快照直读，深圳切片）。

## 2. 表体系

同 `M_CHAIN_BOTTLENECK_COUNT.md` §2（ADS v2 `metric_fact` 消费 / DWD v5 `model_result_detail` 原子分 region_code=440300）。

## 3. SQL

```sql
SELECT f.metric_value AS sz_problem_cnt
FROM demo_gkxlumenx_ads.industry_chain_metric_fact f
WHERE f.is_deleted = 0 AND f.publish_status = 'published'
  AND f.metric_id = 'M_CHAIN_SZ_PROBLEM_COUNT'
  AND f.object_type = 'chain' AND f.object_id = :chain_code
  AND f.region_code = '440300'          -- 深圳，等值
ORDER BY f.stat_period DESC, f.id DESC
LIMIT 1;   -- 最新发布快照；0 行 → NULL（无数据）
```

## 4. 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `:chain_code` | 产业链编码（INB） | 必填 |

## 5. 随附待办（不挡口径）

- 深圳问题诊断模型未跑（现 0 行出 NULL）——数据事，不挡口径。

## 6. 版本与变更

| 版本 | 日期 | 变更 | 拍板 |
|---|---|---|---|
| 0.1.0 | — | 旧稿：LIKE '4403%' 对 v1 废弃壳 | — |
| 0.2.0 | 2026-10-14 | 读表口径 + 440300 等值切片定版 | human:徐滕强 |

正式签名待 human:唐绍祖 会签。
