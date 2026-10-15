---
metric_id: M_CHAIN_NEWS_SENTIMENT_RATIO
metric_name_zh: 资讯正面情感占比
algorithm_type: STAT
version: 0.2.0
updated: 2026-10-14
owner: data-agent / human:淮政玮
status: 口径已定（读表口径）；缺口登记 GAP-CHAIN-SENTIMENT；无临时口径
---

# M_CHAIN_NEWS_SENTIMENT_RATIO 资讯正面情感占比 — 计算逻辑说明

> 2026-10-14 human:徐滕强 确认：**情感字段缺失，无法完整完成**——本条按「读表口径定版 + 缺口登记」处理，非伪闭合。

## 1. 业务定义

指定产业链相关资讯中正面情感占比（%）。

- **分母** = 该链全部有效资讯数（`COUNT(pk_id)`，同 `M_CHAIN_NEWS_COUNT` 口径）
- **分子** = `sentiment` 命中正面值集的资讯数
- 正面判定值集（`'positive'` / `'正面'`）：**随 NLP 管线契约定，不预拍**

## 2. 数据源与缺口（实核 2026-10-14）

| 项 | 状态 |
|---|---|
| `dwd_industry_chain_news_info` | 12 业务字段，**无 sentiment 字段**（pk_id/industry_code/title/publish_date/abstract/source 等） |
| 全库情感表/字段（ods/dwd/ads） | **不存在**（sentiment/emotion 检索 0 结果） |
| ADS v2 `industry_chain_metric_fact` | 映射在（v2 §6 标量），管线产出后指标引擎写数 |

**缺口**：`GAP-CHAIN-SENTIMENT` —— NLP 情感管线产出 sentiment 标注 + 指标引擎按链聚合写 `metric_fact`。归算法侧，与 `GAP-CHAIN-HEAT-SCORE`（热度打分）同族，**建议并入同一条资讯 NLP 管线任务**（一次模型跑完 heat_score + sentiment 双标注）。

## 3. SQL（读表口径，当前生效）

```sql
SELECT f.metric_value AS positive_sentiment_pct
FROM demo_gkxlumenx_ads.industry_chain_metric_fact f
WHERE f.is_deleted = 0 AND f.publish_status = 'published'
  AND f.metric_id = 'M_CHAIN_NEWS_SENTIMENT_RATIO'
  AND f.object_type = 'chain' AND f.object_id = :chain_code
ORDER BY f.stat_period DESC, f.id DESC
LIMIT 1;   -- 管线未落 → 0 行 → NULL（无数据，如实展示）
```

上游聚合语义（管线落地后由指标引擎执行）：

```sql
-- 语义参考，非当前可执行（sentiment 字段不存在）
SELECT ROUND(100 * COUNT(CASE WHEN n.sentiment IN (:positive_enum) THEN 1 END)
                 / COUNT(n.pk_id), 2)
FROM demo_gkxlumenx_ods.dwd_industry_chain_news_info n
WHERE n.is_deleted = 0 AND n.industry_code = :chain_code;
```

## 4. 与 M_CHAIN_HOT_NEWS_COUNT 的差异（同族不同命）

| | HOT_NEWS（已落） | 本条 SENTIMENT |
|---|---|---|
| 字段缺失 | heat_score 缺 | sentiment 缺 |
| 临时口径 | **有**（全量代热点，UI 不体现） | **无**（情感占比没有诚实代理值，不出数就是 NULL） |
| 正式口径 | P90 分位 Top10%（已锁） | 正面/全量占比（值集随管线契约） |

## 5. 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `:chain_code` | 产业链编码（INB） | 必填 |
| `:positive_enum` | 正面值集 | **待管线契约**（GAP-CHAIN-SENTIMENT） |

## 6. 边界语义

- 管线落地前：NULL（无数据）——**禁止**用关键词规则在前端/SQL 冒充情感判定。
- 无一 ELSE 兜底：非正面值（负面/中性/未知）全部计入分母，分子只认正面值集。

## 7. 解挂条件

1. NLP 情感管线落 `sentiment` 标注（建议与 heat_score 同管线一次产出）；
2. 指标引擎按链聚合写 `metric_fact`（metric_id=本条）；
3. 正面值集随管线契约冻结后回填 `:positive_enum`。

## 8. 版本与变更

| 版本 | 日期 | 变更 | 拍板 |
|---|---|---|---|
| 0.1.0 | — | 旧稿：pending_algorithm 对废弃壳字段 | — |
| 0.2.0 | 2026-10-14 | 读表口径定版 + GAP-CHAIN-SENTIMENT 登记 + 无临时口径如实 NULL | human:徐滕强 |

正式签名待 human:唐绍祖 会签。
