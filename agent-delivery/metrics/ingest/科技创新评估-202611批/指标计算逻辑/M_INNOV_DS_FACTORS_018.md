# 监测趋势预测（M_INNOV_DS_FACTORS_018）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_FACTORS_018 |
| 指标名称 | 监测趋势预测 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_FACTOR_FORECAST（监测趋势预测）**。

## 计算逻辑说明

本指标与 **M_INNOV_FACTOR_FORECAST（监测趋势预测）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_zh_journal(publication_id, publication_type) — 会议/期刊入集,出版物类型
- dwd_en_journal(publication_id, publication_type) — 会议/期刊入集,出版物类型
- dwd_zh_paper(id, publication_id, publication_type, cover_year_start) — 中文论文去重,会议/期刊区分,发表年
- dwd_en_paper(id, publication_id, publication_type, cover_year_start) — 英文论文去重,会议/期刊区分,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐
- dwd_zh_project(id, approval_year, funded_province) — 国内项目去重,立项年,资助省
- dwd_en_project(id, approval_year) — 国外项目去重,立项年
- dwd_patent(pn, apdt_year, first_applicant_name) — 专利去重,申请年,申请人对齐
- dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1] 统计学习（聚类/预测）|Stanford University|—|James G, Witten D, Hastie T, Tibshirani R. An Introduction to Statistical Learning[M]. New York: Springer, 2013.

[1]监测趋势预测｜南京大学信息管理系，中国科学技术信息研究所｜国家十一五支撑计划项目（2006BAH03B05）；国家自然科学基金项目（70673019）｜俞立平，潘云涛，武夷山. 基于因子分析的学术期刊评价指标分类研究[J]. 图书情报工作, 2009, 53(8): 146-149.

[2]监测趋势预测｜同济大学上海国际知识产权学院，国家知识产权局｜国家自然科学基金项目（71874122、71403188）；国家知识产权局软科学研究项目（SS16-B-06）；江苏省社会科学基金重点项目（20WTA-010）；同济大学研究生课程思政研究项目（2021KCSZYJ28）｜刘谦，姜南，王亚利，等. 国内高价值专利研究热点演进与整合框架——基于SKM的可视化分析[J]. 科技进步与对策, 2022, 39(21): 151-160.
