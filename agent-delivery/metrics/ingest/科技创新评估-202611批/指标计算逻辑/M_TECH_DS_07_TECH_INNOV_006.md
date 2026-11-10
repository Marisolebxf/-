# 技术创新趋势预测（M_TECH_DS_07_TECH_INNOV_006）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_TECH_DS_07_TECH_INNOV_006 |
| 指标名称 | 技术创新趋势预测 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 技术创新力指标展示 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_TINN_FORECAST（技术创新趋势预测）**。

## 计算逻辑说明

本指标与 **M_INNOV_TINN_FORECAST（技术创新趋势预测）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年
- dwd_patent_cited(pn, cited_by_nums) — 专利被引次数
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日
- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1] 趋势预测|Monash University|—|Hyndman R J, Athanasopoulos G. Forecasting: Principles and Practice[M]. 3rd ed. Melbourne: OTexts, 2021.
[2] 统计学习（聚类/预测）|Stanford University|—|James G, Witten D, Hastie T, Tibshirani R. An Introduction to Statistical Learning[M]. New York: Springer, 2013.
