# M_CHAIN_NEWS_COUNT 动态资讯数 计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（pk_id 直数 / industry_code 等值匹配 / 窗口参数化，默认窗口归前端）
- **类型**：STAT（池计数）
- **is_mock**：true（demo 90 行真实数据在，但样本不全；全量跟 CHAIN-P0-5；D4=ingesting 因 ODS 实数已活）

## 1. 原始定义档案

- **页面语境**：链详情页"资讯"区池计数三件套之三——这条链有多少条动态资讯。
- **白话**：带这条链标签的新闻条数。
- **旧稿问题**：v0.1.0 引用 `dwd.industry_chain_news` + `news_id` 去重——表名漂移（真表 = ods `dwd_industry_chain_news_info`），字段名漂移（真主键 = `pk_id`）。

## 2. 指标定义（v0.2.0）

**指定产业链（industry_code = :chain_code 等值）相关动态资讯的去重条数。**

| 决策点 | 拍板 | 说明 |
|---|---|---|
| ① 去重键 | `pk_id` 物理主键，`COUNT(*)` 直数 | 每行一条资讯；单表无 JOIN 无重复风险 |
| ② 挂链键 | `industry_code = :chain_code` 纯等值 | 表自带 INB 链码**免桥**；同 product_tags 拍板（禁 LIKE 迁就脏数据；值域比对仅质量参考） |
| ③ 时间窗 | 默认全量 + 近 N 年查询参数 | `publish_date` 时间轴；默认窗口（如"近 1 年"）是前端/API 的运营默认，不进口径 |

## 3. Formula（SQL）

```sql
-- 全量版（口径本体）
SELECT COUNT(*) AS chain_news_cnt
FROM demo_gkxlumenx_ods.dwd_industry_chain_news_info n
WHERE n.is_deleted = 0
  AND n.industry_code = :chain_code;

-- 近 N 年窗口版（查询参数，不进口径）：追加 AND n.publish_date >= :window_start
```

## 4. 与旧细稿的关系

旧 calc-logic（ADS `chain_news_stat` 月聚合版，`SUM(news_count) WHERE stat_month=最新月`）降为**补充视图**（适合月度增量页点位）；8 件套主口径用明细直数，与 definition"去重总数"一致。ADS 表不废，但主数不走它。

## 5. 执行模式建议

- 总量：预计算候选（ADS 快照）；
- 窗口查询：实时参数化 SQL；
- 量级评估届时用真实数据（量级不进口径）。

## 6. 表依赖与实核（2026-10-14 demo）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd_industry_chain_news_info` | 唯一活源 | demo **90 行**（pk_id/industry_code/industry_name/title/publish_date/abstract/source）；无 heat_score、无 sentiment（HOT_NEWS / SENTIMENT_RATIO 另行处理）；Group① 唯一当前即可跑指标 |

## 7. 缺口分型

| 项 | 分型 | 处置 |
|---|---|---|
| 90 行小样本 | 数据未灌全 | 跟 CHAIN-P0-5；口径不迁就 |
| industry_code↔chain_id 值域比对 | 质量参考项 | 回库一条 SQL 比对，不影响口径成立 |
| 旧稿表名/字段漂移 | 已重写 | `dwd.industry_chain_news`/`news_id` 弃 |

## 更新记录

- 2026-08-24: 初版 v0.1.0（表名字段双漂移稿）
- 2026-10-14: v0.2.0 口径重写（human:徐滕强 拍板）
