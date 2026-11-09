# 威胁因素分析（M_INNOV_DS_05_GBA_ANALYSIS_006）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_05_GBA_ANALYSIS_006 |
| 指标名称 | 湾区创新能力威胁因素 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新能力分析（SWOT） |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_GBA_SWOT_THREAT（湾区创新能力威胁因素）**。

## 计算逻辑说明

本指标与 **M_INNOV_GBA_SWOT_THREAT（湾区创新能力威胁因素）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集
- dwd_policy_base(id, city, province, status, expire_date, publish_year) — 政策有效失效,到期日
- dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC集中度,申请年

## 待建字段

- 无

## 参考资料

[1] 威胁因素分析｜西北政法大学经济学院，中南财经政法大学经济学院｜陕西省科技厅项目（2021JM-454）｜徐梅，张露. 补贴退坡对新能源企业技术创新的影响研究[J]. 重庆社会科学, 2025(8): 85-100. DOI: 10.19631/j.cnki.css.2025.008.006.

[2]威胁因素分析｜知识产权出版社有限责任公司｜王彦嫱，张聿文，姚长利. 基于HHI指数的中国类脑智能产业专利集中度研究[J]. 中国发明与专利, 2026, 23(6): 15-22.
