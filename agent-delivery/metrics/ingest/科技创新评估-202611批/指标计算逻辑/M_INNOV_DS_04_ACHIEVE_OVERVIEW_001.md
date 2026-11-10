# 创新价值（M_INNOV_DS_04_ACHIEVE_OVERVIEW_001）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_04_ACHIEVE_OVERVIEW_001 |
| 指标名称 | 创新价值 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 创新成果综合展示 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_ACHIEVE_VALUE（创新价值）**。

## 计算逻辑说明

本指标与 **M_INNOV_ACHIEVE_VALUE（创新价值）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_patent(pn, value, first_applicant_name, apdt_year) — 专利去重,专利价值,申请人对齐,申请年
- dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日
- dwd_zh_paper(id, publication_id, download_num, cover_year_start) — 中文论文去重,挂刊,下载量,发表年
- dwd_en_paper(id, publication_id, cover_year_start) — 英文论文去重,挂刊,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐
- dwd_zh_journal(publication_id, impact_score, jn_zone) — 中文刊影响指数,分区
- dwd_en_journal(publication_id, impact_score, jn_zone) — 英文刊影响指数,分区
- dwd_zh_project(id, funded_amount, final_report_abstract, project_level, approval_year, funded_province) — 国内项目资助,结题,级别,立项年,资助省
- dwd_en_project(id, funded_amount, final_report_abstract, project_level, approval_year) — 国外项目资助,结题,级别,立项年
- dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1]创新点价值｜中国科学院文献情报中心，中国科学院大学｜席崇俊，吕璐成，赵亚娟，等. 基于全代引证的专利学术影响力成长路径及获奖因素影响研究[J]. 文献与数据学报, 2024, 6(3): 34-46.

[2]创新点价值｜天津工业大学经济与管理学院｜天津市知识产权局委托项目“面向2035年天津市提升知识产权创造能力的思路和重大举措研究”｜郑晓红，唐家龙. 京津冀地区专利质量动态演进趋势分析[J]. 安徽科技, 2021(3): 31-35.
