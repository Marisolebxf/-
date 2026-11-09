# 要素影响力（M_INNOV_DS_FACTORS_008）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_FACTORS_008 |
| 指标名称 | 要素影响力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.3-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_CONFERENCE_INFLUENCE（会议影响力）**。

## 计算逻辑说明

本指标与 **M_INNOV_CONFERENCE_INFLUENCE（会议影响力）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_zh_journal(publication_id, publication_type, zh_name, en_name, impact_score) — 中文侧会议实体,影响指数
- dwd_en_journal(publication_id, publication_type, zh_name, en_name, impact_score) — 英文侧会议实体,影响指数
- dwd_zh_paper(id, publication_id, publication_type, publication_zh_name, download_num, cover_year_start) — 中文会议论文,下载量,统计年
- dwd_en_paper(id, publication_id, publication_type, publication_en_name, cover_year_start) — 英文会议论文,统计年
- dwd_zh_author(paper_id, author_id, zh_name, en_name) — 中文作者
- dwd_en_author(paper_id, author_id, zh_name, en_name) — 英文作者

## 待建字段

- 无

## 参考资料

[1]会议影响力｜University of Oxford（牛津大学），University of Bonn（波恩大学），RWTH Aachen University（亚琛工业大学）等｜DFG（LA 3745/4-1）；ERC（819536）；Projekt DEAL｜Vahdati S, Fathalla S, Lange C, Behrend A, Say A, Say Z, Auer S. A comprehensive quality assessment framework for scientific events[J].Scientometrics, 2021, 126(1): 641-682.
