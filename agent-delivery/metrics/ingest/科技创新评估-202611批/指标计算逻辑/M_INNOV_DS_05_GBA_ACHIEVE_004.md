# 创新热点区域识别（M_INNOV_DS_05_GBA_ACHIEVE_004）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_05_GBA_ACHIEVE_004 |
| 指标名称 | 湾区创新热点区域 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新成果综合展示 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_GBA_HOTSPOT（湾区创新热点区域）**。

## 计算逻辑说明

本指标与 **M_INNOV_GBA_HOTSPOT（湾区创新热点区域）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, addr_lng, addr_lat) — 湾区机构入集,区县主键,名称对齐,落图
- dwd_research_institute_base_info(org_id, name_cn, city, province, area, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集
- dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC类型,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_zh_project(id, funded_institution, approval_year) — 受资助机构,立项年

## 待建字段

- 无

## 参考资料

[1]创新热点区域识别｜重庆生产力促进中心，重庆工商大学数学与统计学院，重庆市科学技术情报学会｜《重庆科技创新指数报告2023》[R]. 西南财经大学出版社, 2024-09-25.

[2]创新热点区域识别｜广州大学地理科学与遥感学院｜国家自然科学基金项目（41771127）｜陈小兰，千庆兰，张凯煌. 广州创新区的分布、类型及资产特征[J]. 现代城市研究, 2021(1): 39-44.

[3]创新热点区域识别｜武汉理工大学土木工程与建筑学院｜李文诗. 基于DBSCAN算法的武汉东湖高新区创新空间集群识别与分布特征研究[J]. 建筑与文化, 2025(7): 67-69. DOI: 10.19875/j.cnki.jzywh.2025.07.022.
