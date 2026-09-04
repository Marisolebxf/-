# 深圳创新能力指数（M_INNOV_CITY_INDEX_SZ）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CITY_INDEX_SZ |
| 指标名称 | 深圳创新能力指数 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 深圳创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | — |

## 口径定义

衡量深圳在创新资源、创新主体、创新环境上的综合水平，取值 0—100。对象=深圳，可并列对标城。

## 计算逻辑说明

深圳与对标城入集。需求未列指数构成维度，二级按区域创新能力文献。采用加权平均，三维：创新资源 / 创新主体 / 创新环境。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 创新资源 |  | 研发经费，否则研发人员。 | SUM(research_development_amount)；空则 SUM(development_employee) | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 |
| 创新主体 |  | 存续机构与高企。 | 0.5×norm(机构数)+0.5×norm(高企数) | dwd_org_base_info(org_id, city, reg_status) — 存续机构；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签 |
| 创新环境 |  | 有效政策去重件数。 | COUNT(DISTINCT id) | dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 城市机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外机构入集；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员；dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策件数；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|深圳创新监测.md|城市排名展示 · 序号 131(了解深圳市的科技发展水平)。需求未列指数构成维度，二级按《中国区域创新能力评价报告》收口为创新资源/创新主体/创新环境，参考权威机构方案。
