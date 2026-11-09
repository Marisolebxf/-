# 监测异常点识别（M_INNOV_DS_FACTORS_019）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_FACTORS_019 |
| 指标名称 | 监测异常点识别 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.3-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_FACTOR_ANOMALY（监测异常点识别）**。

## 计算逻辑说明

本指标与 **M_INNOV_FACTOR_ANOMALY（监测异常点识别）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_patent(pn, apdt_year, first_applicant_name) — 专利年聚合
- dwd_zh_paper(id, cover_year_start) — 中文论文年聚合
- dwd_en_paper(id, cover_year_start) — 英文论文年聚合
- dwd_scholar(scholar_id, paper_nums, citation_nums, h_index) — 学者存量
- dwd_org_base_info(org_id, name_cn, province, city) — 机构切片

## 待建字段

- 无

## 参考资料

[1] 统计学习（聚类/预测）|Stanford University|—|James G, Witten D, Hastie T, Tibshirani R. An Introduction to Statistical Learning[M]. New York: Springer, 2013.
