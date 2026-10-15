---
metric_id: M_CHAIN_BOTTLENECK_SEVERITY
metric_name_zh: 瓶颈严重度
algorithm_type: STAT
version: 0.2.0
updated: 2026-10-14
owner: data-agent / human:淮政玮
status: 口径已定（读表口径 + 双字段同返）
---

# M_CHAIN_BOTTLENECK_SEVERITY 瓶颈严重度 — 计算逻辑说明

> 2026-10-14 human:徐滕强 拍板：读表口径 + **分级与评分双字段同返**——`metric_value`（数值评分）+ `metric_label`（分级标签）一起返回，下游各取所需（UI 显分级、分析取数值）。表结构天然支持双形态，**无需等模型卡选边**。

## 1. 业务定义

指定产业链瓶颈识别结果的严重度（发布快照直读，分级 + 评分双字段）。

## 2. 表体系

同 `M_CHAIN_BOTTLENECK_COUNT.md` §2（ADS v2 `metric_fact` 消费 / DWD v5 `model_result_detail` 原子分；v1 壳表废止）。

## 3. SQL

```sql
SELECT f.metric_value AS severity_score,   -- 数值评分
       f.metric_label AS severity_label    -- 分级标签（如 高/中/低）
FROM demo_gkxlumenx_ads.industry_chain_metric_fact f
WHERE f.is_deleted = 0 AND f.publish_status = 'published'
  AND f.metric_id = 'M_CHAIN_BOTTLENECK_SEVERITY'
  AND f.object_type = 'chain' AND f.object_id = :chain_code
ORDER BY f.stat_period DESC, f.id DESC
LIMIT 1;   -- 最新发布快照；0 行 → NULL（无数据）
```

## 4. 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `:chain_code` | 产业链编码（INB） | 必填 |

## 5. 随附待办（不挡口径）

- `severity_level` 枚举冻结：v5 §9 开放项「待算法 Lead 模型卡」（影响写入侧标签集，不影响本读表）
- QC04 🟡

## 6. 版本与变更

| 版本 | 日期 | 变更 | 拍板 |
|---|---|---|---|
| 0.1.0 | — | 旧稿：MAX(severity_score) 0-100 对 v1 废弃壳（不可执行） | — |
| 0.2.0 | 2026-10-14 | 读表口径 + 双字段同返定版 | human:徐滕强 |

正式签名待 human:唐绍祖 会签。
