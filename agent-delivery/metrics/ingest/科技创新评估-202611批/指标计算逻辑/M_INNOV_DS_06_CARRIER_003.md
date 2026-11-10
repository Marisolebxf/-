# 创新价值排名（M_INNOV_DS_06_CARRIER_003）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_06_CARRIER_003 |
| 指标名称 | 深圳创新载体创新价值排名 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 深圳创新监测 / 创新载体综合展示 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_CARRIER_VALUE_RANK_SZ（深圳创新载体创新价值排名）**。

## 计算逻辑说明

本指标与 **M_INNOV_CARRIER_VALUE_RANK_SZ（深圳创新载体创新价值排名）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 深圳载体入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, org_type, reg_status) — 科研机构入集
- dwd_patent(pn, first_applicant_name, value, apdt_year) — 专利去重,申请人对齐,专利价值,申请年
- dwd_patent_cited(pn, cited_by_nums) — 专利被引次数
- dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,生效日,转移前后权利人
- dwd_zh_paper(id, publication_id, download_num, cover_year_start) — 中文论文,挂刊,下载量,发表年
- dwd_en_paper(id, publication_id, cover_year_start) — 英文论文,挂刊,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_zh_journal(publication_id, impact_score) — 中文刊影响指数
- dwd_en_journal(publication_id, impact_score) — 英文刊影响指数
- dwd_zh_paper_citation(id, citation_num) — 中文论文被引次数

## 待建字段

- 无

## 参考资料

[1]创新价值｜国务院办公厅｜国务院办公厅关于完善科技成果评价机制的指导意见：国办发〔2021〕26号｜2021-08-02｜https://www.gov.cn/zhengce/content/2021-08/02/content_5628987.htm.

[2]创新价值｜浙江工商大学统计与数学学院｜国家社会科学基金项目“学术期刊评价——指标创新与方法研究”（21FTQB016）｜俞立平，沈洁. 基于论文下载与被引分区的学术期刊评价研究[J]. 中国科技期刊研究, 2022, 33(2): 260-266.
