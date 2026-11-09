# 要素聚类分析（M_INNOV_DS_FACTORS_016）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_FACTORS_016 |
| 指标名称 | 要素聚类分析 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_FACTOR_CLUSTER（要素聚类）**。对会议、项目、专利、期刊四类要素，用对应影响力得分聚类。

## 计算逻辑说明

本指标与 **M_INNOV_FACTOR_CLUSTER（要素聚类）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

入集对象与特征来源：

- M_INNOV_CONFERENCE_INFLUENCE（会议影响力）
- M_INNOV_PROJECT_INFLUENCE（项目（含课题）影响力）
- M_INNOV_PATENT_INFLUENCE（专利影响力）
- M_INNOV_JOURNAL_INFLUENCE（期刊影响力）

## 源表字段

- dwd_zh_journal(publication_id, publication_type, zh_name, en_name, impact_score, paper_nums, cite_nums) — 会议/期刊入集,影响指数,发文量,被引用量
- dwd_en_journal(publication_id, publication_type, zh_name, en_name, impact_score, paper_nums) — 会议/期刊入集,影响指数,发文量
- dwd_zh_paper(id, publication_id, publication_type, download_num, cover_year_start) — 会议论文,下载量,期刊发文回退,统计年
- dwd_en_paper(id, publication_id, publication_type, cover_year_start) — 会议论文,期刊发文回退,统计年
- dwd_zh_author(paper_id, author_id, zh_name, en_name) — 中文作者,会议参与人数
- dwd_en_author(paper_id, author_id, zh_name, en_name) — 英文作者,会议参与人数
- dwd_zh_project(id, funded_amount, participating_institution, funded_institution, final_report_abstract, approval_year) — 国内项目入集,资助金额,参与机构,受资助机构,结题摘要,立项年
- dwd_en_project(id, funded_amount, participating_institution, funded_institution, final_report_abstract, approval_year) — 国外项目入集,资助金额,参与机构,受资助机构,结题摘要,立项年
- dwd_patent(pn, value, apdt_year, pbdt_year) — 专利去重,专利价值,申请年,公开年
- dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数

## 待建字段

- 无

## 参考资料

[1]要素聚类｜南京大学信息管理系，中国科学技术信息研究所｜国家十一五支撑计划项目（2006BAH03B05）；国家自然科学基金项目（70673019）｜俞立平，潘云涛，武夷山. 基于因子分析的学术期刊评价指标分类研究[J]. 图书情报工作, 2009, 53(8): 146-149.

[2]要素聚类｜同济大学上海国际知识产权学院，国家知识产权局｜国家自然科学基金项目（71874122、71403188）；国家知识产权局软科学研究项目（SS16-B-06）；江苏省社会科学基金重点项目（20WTA-010）；同济大学研究生课程思政研究项目（2021KCSZYJ28）｜刘谦，姜南，王亚利，等. 国内高价值专利研究热点演进与整合框架——基于SKM的可视化分析[J]. 科技进步与对策, 2022, 39(21): 151-160.
