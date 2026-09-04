# 深圳城市科技发展排名（M_INNOV_CITY_RANK_SZ）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CITY_RANK_SZ |
| 指标名称 | 深圳城市科技发展排名 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 深圳创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | — |

## 口径定义

深圳在研发投入、专利数量、高新技术企业数量、创新人才上相对对标城的名次。

## 计算逻辑说明

深圳与对标城入集。四维：研发投入 / 专利数量 / 高新技术企业数量 / 创新人才。各维分别排名，综合名次按四维等权。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 研发投入 |  | 该城上市研发经费，否则研发人员。 | SUM(research_development_amount)；空则 SUM(development_employee) | dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入 |
| 专利数量 |  | 该城专利去重件数。 | COUNT(DISTINCT pn) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年 |
| 高新技术企业数量 |  | org_tag 含高新技术的机构去重数。 | COUNT(DISTINCT org_id WHERE org_tag 含高新技术) | dwd_org_tech_tag(org_id, org_tag) — 高新技术标签 |
| 创新人才 |  | 对齐到该城的学者与研发人员。 | 学者去重数 + SUM(development_employee) | dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 城市机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外机构入集；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|深圳创新监测.md|城市排名展示 · 序号 131(展示深圳市在不同科技发展指标上的城市排名)。科技发展指标收口序号 130(研发投入、专利数量、高新技术企业数量、创新人才)
