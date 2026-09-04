# 城市创新能力要素表现（M_INNOV_CITY_FACTOR_GLOBAL）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CITY_FACTOR_GLOBAL |
| 指标名称 | 城市创新能力要素表现 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 全球创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | — |

## 口径定义

各城在人才、资金、政策三要素上的量化表现，取值 0—100。对象=城市。不拆成多条 ID。

## 计算逻辑说明

城市入集。采用加权平均，三维：人才（学者+研发人员）/ 资金（研发经费）/ 政策（有效政策数）。本批城内极值归一。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 人才 |  | 学者与研发人员。 | 学者去重数 + SUM(development_employee) | dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 |
| 资金 |  | 上市研发投入。 | SUM(research_development_amount) | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入 |
| 政策 |  | 有效政策去重件数。 | COUNT(DISTINCT id) | dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 城市机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外机构入集；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员；dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|全球创新监测.md|创新能力要素分析 · 序号 86(如人才、资金、政策)
