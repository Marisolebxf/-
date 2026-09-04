# 短板因素分析（M_INNOV_DS_05_GBA_ANALYSIS_004）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_05_GBA_ANALYSIS_004 |
| 指标名称 | 短板因素分析 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

同M_INNOV_GBA_SWOT_WEAKNESS-湾区创新能力短板因素

## 计算逻辑说明

同M_INNOV_GBA_SWOT_WEAKNESS-湾区创新能力短板因素

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集；dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 专利去重,共申请人,申请人对齐,申请年；dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 合作项目；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_policy_base(id, city, province, status, expire_date, publish_year, rank, theme) — 政策供给,主题,有效

## 待建字段

无

## 备注

OPEN draft 身份，口径/计算逻辑对齐正式指标 M_INNOV_GBA_SWOT_WEAKNESS（湾区创新能力短板因素）。05 无短板识别专叶。见 GA-D04。统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签。
