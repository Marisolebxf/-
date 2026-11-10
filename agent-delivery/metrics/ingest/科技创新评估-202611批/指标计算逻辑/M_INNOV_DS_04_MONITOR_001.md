# 创新点发现（M_INNOV_DS_04_MONITOR_001）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_04_MONITOR_001 |
| 指标名称 | 创新点发现 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 创新监测与分析 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_POINT_DISCOVERY（创新点发现）**。

## 计算逻辑说明

本指标与 **M_INNOV_POINT_DISCOVERY（创新点发现）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_patent(pn, keywords, main_classification_ipcr, first_applicant_name, apdt_year) — 专利关键词,IPC领域,申请人对齐,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_classification(id, keywords) — 中文论文关键词
- dwd_en_paper_classification(id, keywords) — 英文论文关键词
- dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐
- dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1] 研究前沿识别|Drexel University|—|Chen C. CiteSpace II: Detecting and visualizing emerging trends and transient patterns in scientific literature[J]. Journal of the American Society for Information Science and Technology, 2006, 57(3): 359-377.

[2]创新点发现｜北京大学信息管理系｜国家社会科学基金重大项目（21&ZD329）｜汪大锟，化柏林. 基于BERTopic的新兴技术主题识别研究[J]. 科技情报研究, 2025, 7(1): 131-140.
