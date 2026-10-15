---
metric_id: M_CHAIN_HOT_NEWS_COUNT
metric_name_zh: 热门资讯数
algorithm_type: STAT
version: 0.2.0
updated: 2026-10-14
owner: data-agent / human:淮政玮
status: 临时口径生效中（三段式：临时出数 + 正式锁定 + 切换条件）
---

# M_CHAIN_HOT_NEWS_COUNT 热门资讯数 — 计算逻辑说明

> 2026-10-14 human:徐滕强 拍板「路径A：三段式」。本指标当前**不可诚实出真热门数**（`heat_score` 字段现库不存在），采用「临时出数 + 正式口径锁定 + 切换条件写明」策略，UI 侧不体现临时标注。

## 1. 业务定义

- **临时口径（当前生效）**：以链资讯全量代热点，与 `M_CHAIN_NEWS_COUNT` 同源同数。定义层如实标注「临时=全量代热点，热门语义未实现，当前值≠真热门数」。
- **正式口径（锁定待切换）**：heat_score 落地后，链内 P90 分位 Top 10% 资讯计数（至少 1 条）。

## 2. 数据源

| 表 | 字段 | 说明 |
|---|---|---|
| `demo_gkxlumenx_ods.dwd_industry_chain_news_info` | `pk_id`（主键）、`industry_code`、`publish_date`、`is_deleted` | 临时与正式同源；demo 实测 90 行 |
| 同上（待增） | `heat_score` | **现库不存在**。NLP 打分管线产出，缺口登记 `GAP-CHAIN-HEAT-SCORE`，归算法侧 |

## 3. SQL

### 3.1 临时口径（当前生效，可执行）

```sql
SELECT COUNT(*) AS hot_news_cnt
FROM demo_gkxlumenx_ods.dwd_industry_chain_news_info n
WHERE n.is_deleted = 0
  AND n.industry_code = :chain_code;
```

### 3.2 正式口径（锁定待切换；heat_score 字段落地后可执行）

```sql
SELECT COUNT(*) AS hot_news_cnt
FROM (
  SELECT
    n.*,
    ROW_NUMBER() OVER (ORDER BY n.heat_score DESC) AS rk,
    COUNT(*) OVER () AS total
  FROM demo_gkxlumenx_ods.dwd_industry_chain_news_info n
  WHERE n.is_deleted = 0
    AND n.industry_code = :chain_code
) t
WHERE t.rk <= GREATEST(CEIL(t.total * 0.1), 1);
```

- NULL `heat_score` 排序沉底（自然不进 Top10%）。
- `GREATEST(..., 1)` 保证小样本链至少 1 条。
- 旧稿 `heat_score >= 80` 绝对阈值**废除**：字段不存在，且绝对阈值抗不住分布漂移。

## 4. 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `:chain_code` | 产业链编码 | 必填 |

## 5. 版本与变更

| 版本 | 日期 | 变更 | 拍板 |
|---|---|---|---|
| 0.1.0 | — | 旧稿：heat_score>=80 绝对阈值（字段不存在，不可执行） | — |
| 0.2.0 | 2026-10-14 | 三段式：临时全量代热点 + 正式 P90 分位 Top10% 锁定 + 切换条件写明；UI 不体现临时标注 | human:徐滕强 |

## 6. 切换条件（临时 → 正式）

1. NLP 打分管线（`GAP-CHAIN-HEAT-SCORE`，算法侧）在 `dwd_industry_chain_news_info` 落 `heat_score` 字段并完成首灌；
2. 首灌完成后弃临时口径、启用正式口径，本指标与 `M_CHAIN_NEWS_COUNT` 自然分离；
3. 正式口径签名待 human:唐绍祖 会签（分位规则属 D1 决策点）。
