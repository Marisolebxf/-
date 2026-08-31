# 重点资讯统计（M_ENT_BASE_97_4）

> 口径真源：T0-X / ALGO-ENT-BASE-97 → 2026-08-31 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **月总数**：`enterprise_news` 按年-月 COUNT + 环比。不按 `org_id` 分组。  
> 「重点」= 供应方表 `dwd_org_important_news_info` 整表，不挂 `KEY_TOTAL`。  
> 企业画像时间线走 `M_ENT_DEV_HISTORY`，本条不抢。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- 指标ID：`M_ENT_BASE_97_4`
- 名称：重点资讯统计
- 模块：企业基础指标 / ALGO-ENT-BASE-97
- 更新频率：月
- 关联Q：无独立 Q；SRS 融资/并购/新品细化不进本核

## 口径定义

自然月：重点资讯条数，以及相对上月环比。

```
COUNT(*)
FROM enterprise_news
WHERE news_date IS NOT NULL
GROUP BY DATE_FORMAT(news_date, '%Y-%m')
```

环比：

```
(cnt_m - cnt_m-1) / cnt_m-1
```

上月 0 或空 → 环比空。

- 一行一事。主键用表内 `id`（或标题+日期+org 去重实现细节，不进 8 件套）。
- **不按企业拆**。`org_id` 只给选产业 API 收窄，不进 GROUP BY。
- **不挂** `KEY_TOTAL`。有资讯就数。
- **选产业是 API**：经 `org_id` 上链过滤后再数月合计。ETL 全量月（及需要的链键）。
- 只国内。无国外资讯表，不 UNION。
- 禁止 CMS / `is_published`。禁止 `dwd_industry_chain_news_info`。禁止融资/并购/新品金额、交易对手进本核。
- 禁止抄 mock `ads.realdata_enterprise_news_stat` / `ads.ent_news_stat` 当已接通。

8 件套只留这条月 COUNT + 环比。下面实现不得改口径。

## 两点分开（强制）

### ① 本条口径

`enterprise_news.news_date` 在就能按月数。公式完整。

### ② 灌数（另一回事）

ODS `dwd_org_important_news_info` 行数不稳定（曾 0 / 913 / 19983）。不当 D4 live。不进「无法执行」。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_news` | DDL 有；灌数待 GDF |
| 目标 | `enterprise_news_month_stat`（建议：`stat_month + news_cnt + mom`） | **缺口：无此表** |

源 ≠ 目标。GDF 暂缓。

## 分场景 / 千万级（不进 8 件套）

| 层 | 做什么 |
|----|--------|
| ETL | 每月全量年-月 COUNT 写入目标表；环比用上月同行。选产业要链键则预存月×链。 |
| API | 按月 / 链键查行。禁止请求路径扫明细。 |
| 前端 | 月 KPI + 环比。按企看资讯走 `DEV_HISTORY`。 |

**计算公式文件**：`M_ENT_BASE_97_4.md`

## 源表字段

```
enterprise_news <- ods: dwd_org_important_news_info
```

计算 FROM 只用左端。日期列 = `news_date`。

来源系统：国内机构要素库。

## 现网探针（不进 8 件套）

- ODS 表在；2026-08 行数在 0～19983 间晃过。
- 项目 DWD `enterprise_news` 设计有 `org_id` / `news_title` / `news_date`，无类型列。本条不按类型拆。

## 待建 / 缺口（不是口径算不全）

1. GDF 灌 `enterprise_news`。
2. **无独立目标表**。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

acceptance `ALGO-ENT-BASE-97`；STAT。SRS「融资规模/并购/新品」不另造进本 ID。

---
*2026-08-31 COVER-STAT-L01：月总数+环比；不按企业拆*
