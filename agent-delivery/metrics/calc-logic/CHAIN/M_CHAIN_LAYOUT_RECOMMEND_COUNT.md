---
metric_id: M_CHAIN_LAYOUT_RECOMMEND_COUNT
metric_name_zh: 重点布局推荐数
algorithm_type: STAT
version: 0.2.0
updated: 2026-10-14
owner: data-agent / human:淮政玮
status: 口径已定（方案A：单链发展方案条数）
---

# M_CHAIN_LAYOUT_RECOMMEND_COUNT 重点布局推荐数 — 计算逻辑说明

> 2026-10-14 human:徐滕强 拍板**方案A**：统计对象 = **单链发展方案条数**（`object_type='chain'`，带链参数），贴 demo 页面「发展方案 N 项」语义。旧稿 `COUNT(DISTINCT chain_id) WHERE 评分>=阈值`（全局被推荐链数）废止——阈值是查询参数不是口径，模型输出已固化在发布快照。

## 1. 业务定义

指定产业链由布局推荐模型产出的重点布局推荐条数（发布快照直读）。

## 2. 表体系

| 层 | 表 | 说明 |
|---|---|---|
| 发布消费 | ADS v2 `demo_gkxlumenx_ads.industry_chain_metric_fact` | v2 §6 映射本条（标量卡片） |
| 模型原子分 | DWD v5 `industry_chain_model_result_detail` | `priority_level` 归档（推荐档位）；模型卡/QC09 定档后指标引擎写数 |

## 3. SQL

```sql
SELECT f.metric_value AS layout_recommend_cnt
FROM demo_gkxlumenx_ads.industry_chain_metric_fact f
WHERE f.is_deleted = 0 AND f.publish_status = 'published'
  AND f.metric_id = 'M_CHAIN_LAYOUT_RECOMMEND_COUNT'
  AND f.object_type = 'chain' AND f.object_id = :chain_code
ORDER BY f.stat_period DESC, f.id DESC
LIMIT 1;   -- 最新发布快照；0 行 → NULL（无数据）
```

## 4. 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `:chain_code` | 产业链编码（INB） | 必填 |

## 5. 随附待办（不挡口径）

- QC09：推荐权重/档位 🟡 客户决策清单——降级为模型写入侧随附待办，影响何时有数不影响读表口径。
- demo 页「发展方案 3 项」为前端写死清单，模型灌数前不得当真数。

## 6. 版本与变更

| 版本 | 日期 | 变更 | 拍板 |
|---|---|---|---|
| 0.1.0 | — | 旧稿：全局链数 + 阈值口径（语义分叉） | — |
| 0.2.0 | 2026-10-14 | 方案A 单链条数 + 读表口径定版 | human:徐滕强（方案A） |

正式签名待 human:唐绍祖 会签。
