# 产业技术影响力（M_INNOV_POT_TECH_INFL）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_POT_TECH_INFL |
| 指标名称 | 产业技术影响力 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

按专利被引次数、同族规模综合评分，取值 0—100。不用标准必要专利。

## 计算逻辑说明

选定产业入集。采用加权平均，二维：专利被引次数（cited_by_nums）/ 同族规模（other_Versions）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 专利被引次数 |  | 产业相关专利被其他专利引用的总次数。 | SUM(cited_by_nums) | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年 |
| 同族规模 |  | 产业专利海外布局广度，用同族成员数均值衡量。 | 同族成员数合计 / 专利数 | dwd_patent(pn, first_applicant_name, other_Versions, apdt_year) — 同族专利,申请人对齐,申请年 |

## 源表字段

dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签；dwd_patent(pn, first_applicant_name, other_Versions, apdt_year) — 专利去重,申请人对齐,同族,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技创新评估.md|序号 150「基于专利引用、技术标准等数据，评估特定产业的技术影响力……（如专利被引次数、标准必要专利数量）」。对象=产业。≠ TINN 专利质量（单件 vs 产业）。参考权威机构方案。
