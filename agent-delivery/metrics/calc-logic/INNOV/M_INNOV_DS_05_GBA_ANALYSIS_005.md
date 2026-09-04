# 机会因素分析（M_INNOV_DS_05_GBA_ANALYSIS_005）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_05_GBA_ANALYSIS_005 |
| 指标名称 | 机会因素分析 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

同M_INNOV_GBA_SWOT_OPPORTUNITY-湾区创新能力机会因素

## 计算逻辑说明

同M_INNOV_GBA_SWOT_OPPORTUNITY-湾区创新能力机会因素

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集；dwd_policy_base(id, city, province, status, expire_date, publish_year, theme) — 政策窗口,主题；dwd_patent(pn, applicants, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,共申请人,IPC突现,申请年

## 待建字段

无

## 备注

OPEN draft 身份，口径/计算逻辑对齐正式指标 M_INNOV_GBA_SWOT_OPPORTUNITY（湾区创新能力机会因素）。05 不输出 Opportunities 象限。见 GA-D05。统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签。
