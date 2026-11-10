# 期刊影响力（M_INNOV_JOURNAL_INFLUENCE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_JOURNAL_INFLUENCE |
| 指标名称 | 期刊影响力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.3-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

期刊在学术传播中的影响程度。统计对象为期刊实体，从影响指数、发文量、被引用量综合，取值 0—100。

## 计算逻辑说明

第一步至合成：入集：`dwd_zh_journal`/`dwd_en_journal` 中 `publication_type` 为 journal/期刊，按 `publication_id` 去重。影响指数读 `impact_score`；发文量优先 `paper_nums`，没有则统计年论文 `COUNT(DISTINCT id)`；被引用量读 `cite_nums`（英文刊无该字段则该维缺测）。默认权重 0.50/0.25/0.25，缺测维重归一后 ×100。

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
期刊影响力=(0.5\times norm(影响指数)+0.25\times norm(发文量)+0.25\times norm(被引用量))\times 100
$$

输出：按二级子项给出原始值与合成结果（评分类为 0—100；聚类/异常/预测输出标签或期次）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 期刊影响力 | 影响指数 | 期刊影响指数。 | impact_score | dwd_zh_journal(publication_id, impact_score) — 中文影响指数；dwd_en_journal(publication_id, impact_score) — 英文影响指数 | 无 |
| 期刊影响力 | 发文量 | 发文规模。 | 优先 paper_nums；否则 COUNT(DISTINCT 论文id) | dwd_zh_journal(publication_id, paper_nums) — 中文发文量；dwd_en_journal(publication_id, paper_nums) — 英文发文量；dwd_zh_paper(id, publication_id, cover_year_start) — 中文发文回退,统计年；dwd_en_paper(id, publication_id, cover_year_start) — 英文发文回退,统计年 | 无 |
| 期刊影响力 | 被引用量 | 累计被引。 | cite_nums | dwd_zh_journal(publication_id, cite_nums) — 中文被引用量 | 无 |

## 源表字段

- dwd_zh_journal(publication_id, publication_type, zh_name, impact_score, paper_nums, cite_nums) — 中文期刊入集,影响指数,发文量,被引用量
- dwd_en_journal(publication_id, publication_type, en_name, impact_score, paper_nums) — 英文期刊入集,影响指数,发文量
- dwd_zh_paper(id, publication_id, publication_type, cover_year_start) — 中文发文回退,统计年
- dwd_en_paper(id, publication_id, publication_type, cover_year_start) — 英文发文回退,统计年

## 待建字段

- 无

## 参考资料

[1]期刊影响力｜中国科学技术信息研究所｜基金项目：国家十一五支撑计划项目（2006BAH03B05）；国家自然科学基金项目（70673019）｜俞立平，潘云涛，武夷山. 基于因子分析的学术期刊评价指标分类研究[J]. 图书情报工作, 2009, 53(8): 146-149.
