# 深圳科技发展指标对比（M_INNOV_CITY_COMPARE_SZ）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CITY_COMPARE_SZ |
| 指标名称 | 深圳科技发展指标对比 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 深圳创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | — |

## 口径定义

深圳市与选定对标城市在研发投入、专利数量、高新技术企业数量、创新人才上的横向对比。对象=城市，不是载体、不是湾区 11 城固定集合。

## 计算逻辑说明

深圳与对标城入集。四维：研发投入（研发经费/人员）/ 专利数量 / 高新技术企业数量 / 创新人才（学者+研发人员）。本批城内对比。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 研发投入 |  | 该城上市研发经费，否则研发人员。 | SUM(research_development_amount)；空则 SUM(development_employee) | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 |
| 专利数量 |  | 该城专利去重件数。 | COUNT(DISTINCT pn) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年 |
| 高新技术企业数量 |  | org_tag 含高新技术的机构去重数。 | COUNT(DISTINCT org_id WHERE org_tag 含高新技术) | dwd_org_tech_tag(org_id, org_tag) — 高新技术标签 |
| 创新人才 |  | 对齐到该城的学者与研发人员。 | 学者去重数 + SUM(development_employee) | dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 城市机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外机构入集；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|深圳创新监测.md|科技发展指标对比 · 序号 130(包括研发投入、专利数量、高新技术企业数量、创新人才等指标)
