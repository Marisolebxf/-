# 城市对标分析（M_INNOV_CITY_BENCHMARK_GLOBAL）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CITY_BENCHMARK_GLOBAL |
| 指标名称 | 城市对标分析 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 全球创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | — |

## 口径定义

用户选定至少 2 城，对比创新投入、创新产出、创新环境。对象=城市。取值展示原始值与 0—100 维得分，不另开公式。

## 计算逻辑说明

选定城市入集。采用加权平均，三维：创新投入（研发经费/人员）/ 创新产出（专利+论文）/ 创新环境（政策+高企）。本批城内极值归一后对比。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 创新投入 |  | 上市研发经费，否则研发人员。 | SUM(research_development_amount)；空则 SUM(development_employee) | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 |
| 创新产出 |  | 专利与论文去重件数。 | COUNT(DISTINCT pn)+COUNT(DISTINCT 论文id) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 创新环境 |  | 有效政策与高企覆盖。 | 0.5×norm(政策数)+0.5×norm(高企数) | dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策件数；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 城市机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外机构入集；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员；dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策件数；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|全球创新监测.md|城市对标分析 · 序号 85(展示各城市在创新投入、创新产出、创新环境等方面的差异)
