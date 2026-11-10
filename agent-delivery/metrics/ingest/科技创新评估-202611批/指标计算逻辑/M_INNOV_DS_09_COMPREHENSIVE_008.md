# 潜在科技发展方向预警（M_INNOV_DS_09_COMPREHENSIVE_008）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_09_COMPREHENSIVE_008 |
| 指标名称 | 潜在科技发展方向预警 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 综合发展规划 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_PLAN_DIRECTION_ALERT（潜在科技发展方向预警）**。

## 计算逻辑说明

本指标与 **M_INNOV_PLAN_DIRECTION_ALERT（潜在科技发展方向预警）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,关键词袋,申请人对齐,IPC领域,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_classification(id, keywords) — 中文论文关键词
- dwd_en_paper_classification(id, keywords) — 英文论文关键词
- dwd_zh_project(id, keywords, discipline, approval_year) — 项目关键词,学科,立项年
- dwd_scholar_research_direction(scholar_id, fields) — 学者研究方向
- dwd_scholar_paper_relation(scholar_id, year) — 学者发文年
- dwd_policy_base(id, keywords, theme, keypoints, publish_year, city, province) — 政策关键词,主题,要点,发布年,空间
- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1]潜在科技发展方向预警｜中国科学技术信息研究所｜国家自然科学基金项目“科学基金项目产出专利对产业技术发展的影响研究”（L1624039）；国家社会科学基金项目“面向科技型中小企业创新的技术竞争情报方法体系研究”（12CTQ030）｜毛一雷，刘志辉，刘洢颖，姚长青. 公共基金资助产出及影响研究述评[J]. 情报探索, 2017(11): 97-103.

[2]潜在科技发展方向预警｜内蒙古大学经济管理学院，中国科学院科技政策与管理科学研究所，中国科学院创新发展研究中心，中国科学院研究生院管理学院｜国家自然科学基金青年项目（71103078、71103173）；内蒙古自然科学基金项目（2011BS1002）；中国博士后科学基金第四批特别项目（201104158）；中国科学院王宽诚博士后工作奖励项目（2011年度）｜高霞，陈凯华，官建成. 标度无关性视角下的我国区域科技创新绩效评价研究[J]. 中国软科学, 2012(8): 65-74.

[3]潜在科技发展方向预警｜浙江工商大学统计与数学学院｜浙江省重点建设高校优势特色学科（浙江工商大学统计学）和“统计数据工程技术与应用协同创新中心”资助｜杨双双，解静. 基于改进CRITIC的中国区域创新能力测度分析[J]. 统计与管理, 2023, 38(9): 40-54. DOI: 10.16722/j.issn.1674-537x.2023.09.007.
