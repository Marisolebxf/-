---
metric_id: M_CHAIN_BOTTLENECK_COUNT
metric_name_zh: 瓶颈堵点数
algorithm_type: STAT
version: 0.2.0
updated: 2026-10-14
owner: data-agent / human:淮政玮
status: 口径已定（读表口径，等模型灌数）
---

# M_CHAIN_BOTTLENECK_COUNT 瓶颈堵点数 — 计算逻辑说明

> 2026-10-14 human:徐滕强 拍板：**STAT 条目口径 = 读表口径**。读表 SQL 定了，口径即全定；模型侧怎么算（判定维度/阈值/枚举）属 MODEL/模型卡职责，不进口径本体。模型卡未冻结只影响**何时有数**（现 0 行 → NULL 无数据），不影响口径。

## 1. 业务定义

指定产业链被瓶颈识别模型判定入库的瓶颈/堵点数（发布快照直读）。

## 2. 表体系（重要：废弃表禁用声明）

| 层 | 现行表 | 废止表 |
|---|---|---|
| 发布消费 | **ADS v2 `demo_gkxlumenx_ads.industry_chain_metric_fact`**（v2 §6 已映射本条；2026-08-13 S3 收口） | ~~`chain_bottleneck` 等 v1 旧 ADS 八表~~（S3 废止当真源，现网空壳） |
| 模型原子分 | **DWD v5 `industry_chain_model_result_detail`**（指标引擎聚合来源，经 `run_id` 回链） | ~~`dwd.industry_bottleneck`~~（v1 废弃壳，不存在） |

## 3. SQL

```sql
SELECT f.metric_value AS bottleneck_cnt
FROM demo_gkxlumenx_ads.industry_chain_metric_fact f
WHERE f.is_deleted = 0 AND f.publish_status = 'published'
  AND f.metric_id = 'M_CHAIN_BOTTLENECK_COUNT'
  AND f.object_type = 'chain' AND f.object_id = :chain_code
ORDER BY f.stat_period DESC, f.id DESC
LIMIT 1;   -- 最新发布快照；0 行 → NULL（无数据）
```

## 4. 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `:chain_code` | 产业链编码（INB，Q053 冻结） | 必填 |

## 5. 随附待办（不挡口径）

- QC04：瓶颈判定维度/阈值 🟡 客户决策清单——影响模型写入侧
- v5 §9 开放项「诊断 severity / 瓶颈 label 正式枚举 | 待算法 Lead 模型卡」

## 6. 版本与变更

| 版本 | 日期 | 变更 | 拍板 |
|---|---|---|---|
| 0.1.0 | — | 旧稿：COUNT 对 v1 废弃壳表（不可执行） | — |
| 0.2.0 | 2026-10-14 | 读表口径定版（metric_fact 最新发布快照） | human:徐滕强 |

正式签名待 human:唐绍祖 会签。
