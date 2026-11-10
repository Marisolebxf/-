# 创新影响分数（M_INNOV_DS_04_REALTIME_004）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_04_REALTIME_004 |
| 指标名称 | 创新影响分数 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 全球创新实时数据 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_IMPACT_SCORE（创新影响分数）**。

## 计算逻辑说明

本指标与 **M_INNOV_IMPACT_SCORE（创新影响分数）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_org_base_info(org_id, name_cn, province, city) — 机构对齐,空间过滤
- dwd_patent(pn, first_applicant_name, applicants, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,共申请人,IPC领域,申请年
- dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,统计年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,统计年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 受资助机构,参与机构,立项年

## 待建字段

- 无

## 参考资料

[1]创新影响分数｜科学技术部｜生物技术产业创新能力评价指标体系（征求意见稿）｜2013年｜[生物技术产业创新能力评价指标体系 -中华人民共和国科学技术部](https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/t20131129_110671.html).
