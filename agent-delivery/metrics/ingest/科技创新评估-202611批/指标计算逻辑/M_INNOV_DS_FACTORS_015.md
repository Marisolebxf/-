# 要素影响力（M_INNOV_DS_FACTORS_015）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_FACTORS_015 |
| 指标名称 | 要素影响力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.3-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_JOURNAL_INFLUENCE（期刊影响力）**。

## 计算逻辑说明

本指标与 **M_INNOV_JOURNAL_INFLUENCE（期刊影响力）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_zh_journal(publication_id, publication_type, zh_name, impact_score, paper_nums, cite_nums) — 中文期刊
- dwd_en_journal(publication_id, publication_type, en_name, impact_score, paper_nums) — 英文期刊
- dwd_zh_paper(id, publication_id, publication_type, cover_year_start) — 中文发文回退
- dwd_en_paper(id, publication_id, publication_type, cover_year_start) — 英文发文回退

## 待建字段

- 无

## 参考资料

[1]期刊影响力｜中国科学技术信息研究所｜基金项目：国家十一五支撑计划项目（2006BAH03B05）；国家自然科学基金项目（70673019）｜俞立平，潘云涛，武夷山. 基于因子分析的学术期刊评价指标分类研究[J]. 图书情报工作, 2009, 53(8): 146-149.
