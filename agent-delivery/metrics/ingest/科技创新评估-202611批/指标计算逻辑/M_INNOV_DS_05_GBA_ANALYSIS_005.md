# 机会因素分析（M_INNOV_DS_05_GBA_ANALYSIS_005）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_05_GBA_ANALYSIS_005 |
| 指标名称 | 湾区创新能力机会因素 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新能力分析（SWOT） |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_GBA_SWOT_OPPORTUNITY（湾区创新能力机会因素）**。

## 计算逻辑说明

本指标与 **M_INNOV_GBA_SWOT_OPPORTUNITY（湾区创新能力机会因素）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集
- dwd_policy_base(id, city, province, status, expire_date, publish_year, theme) — 政策窗口,主题
- dwd_patent(pn, applicants, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,共申请人,IPC突现,申请年

## 待建字段

- 无

## 参考资料

[1] 机会因素分析｜华中科技大学管理学院，华中科技大学法学院｜教育部人文社会科学基金青年基金项目（20YJC630201）｜纪亚琨，余翔，张奔，彭文波. 专利网络视角下的潜在颠覆性技术识别——以自动驾驶领域为例[J]. 情报杂志, 2022, 41(12): 46-50, 139.

[2]机会因素分析｜北京理工大学珠海学院｜广东省哲学社会科学规划2023年度青年项目（GD23YJY01）；北京理工大学珠海学院粤港澳大湾区高质量发展重大问题研究课题（XK-2023-034）｜马静娴. 粤港澳大湾区产学协同创新网络结构特征及优化对策[J]. 科技和产业, 2024, 24(22): 230-240.
