# 政策实施效果（M_INNOV_PG_EFFECT）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PG_EFFECT |
| 指标名称 | 政策实施效果 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | — |

## 口径定义

基于实施后数据变化评估实际效果。对象=城市。三维：专利增幅、论文增幅、项目增幅。

## 计算逻辑说明

选定城市入集。需求未列关键指标字段，二级按实施前后成果变化。采用加权平均，三维：专利增幅 / 论文增幅 / 项目增幅。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 专利增幅 |  | 近窗专利相对基线。 | (近3年专利均值-前5年均值)/max(前5年均值,1) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年 |
| 论文增幅 |  | 近窗论文相对基线。 | (近3年论文均值-前5年均值)/max(前5年均值,1) | dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 项目增幅 |  | 近窗立项相对基线。 | (近3年项目均值-前5年均值)/max(前5年均值,1) | dwd_zh_project(id, funded_institution, funded_province, approval_year) — 项目去重,立项年 |

## 源表字段

dwd_policy_base(id, title, keywords, keypoints, theme, city, province, district, type, status, expire_date, publish_year) — 政策去重,主题,类型,区县,有效；dwd_zh_project(id, funded_amount, funded_institution, funded_province, approval_year) — 项目去重,资助额,立项年；dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 城市机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外机构入集；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技创新评估.md|政策实施效果评估 · 序号 156(查看政策实施前后的关键指标对比)。需求未列关键指标字段，二级按实施前后成果变化取专利增幅/论文增幅/项目增幅，参考权威机构方案。
