# 企业能力（M_CHAIN_ENTERPRISE_POWER）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_ENTERPRISE_POWER |
| 指标名称 | 企业能力 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业指数评价 |
| 三级模块 | 区域产业指数 |
| 更新频率 | 年 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q055+QC05 |


## 口径定义

指定区域在指定产业链上的企业能力竞争力得分，取值0—100。对齐算法库企业能力竞争力，由产业生态（企业数）、企业营收、产业化程度（专利）三维合成。

## 计算逻辑说明

三维等权。先按区域、链、年计算企业数、营业收入合计、专利去重件数，再在同一产业链、同一统计年度对全部对比区域做截面min-max归一化到[0,1]，算术平均后乘100。某维全部区域取值相同则该维取0.5。默认等权，前端可调权重但不另建权重表。区域用机构所在省、市过滤，深圳场景取city="深圳市"。从dwd_industry_chain_info确定目标产业链，关联dwd_org_industry_tags取链上企业，再关联dwd_org_base_info筛区域。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 区域产业指数 | 企业能力 | 产业生态 | 区域链上企业去重件数。credit_code关联dwd_org_base_info筛区域后COUNT(DISTINCT credit_code)。库无上下游协同度、公共服务配套度正式字段，本指标计企业集聚规模 | dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称; dwd_org_industry_tags(industry_code, credit_code) — 链上企业筛选, 信用代码关联; dwd_org_base_info(external_id, province, city) — 企业信用代码关联, 省份, 城市 | 无 |
| 区域产业指数 | 企业能力 | 企业营收 | 区域链上企业营业收入合计。credit_code关联dwd_org_base_info筛区域，再关联dwd_org_annual_financial_info.external_id，按year汇总operating_revenue | dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称; dwd_org_industry_tags(industry_code, credit_code) — 链上企业筛选, 信用代码关联; dwd_org_base_info(external_id, province, city) — 企业信用代码关联, 省份, 城市; dwd_org_annual_financial_info(external_id, year, operating_revenue) — 企业信用代码关联, 年报年度, 营业收入 | 无 |
| 区域产业指数 | 企业能力 | 产业化程度 | 区域链上企业专利去重件数。credit_code关联dwd_org_base_info筛区域后，用company_name匹配dwd_patent.first_applicant_name或assignees_2，按patent_id去重；申请年份用application_reference_4过滤统计年及以前。库无成果转化、技术交易额与产业链正式关联表，以专利作为产业化可计算代理 | dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称; dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配; dwd_org_base_info(external_id, province, city) — 企业信用代码关联, 省份, 城市; dwd_patent(patent_id, first_applicant_name, assignees_2, application_reference_4) — 专利去重, 第一申请人匹配, 当前专利权人匹配, 申请年份 | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配
- dwd_org_base_info(external_id, province, city) — 企业信用代码关联, 省份, 城市
- dwd_org_annual_financial_info(external_id, year, operating_revenue) — 企业信用代码关联, 年报年度, 营业收入
- dwd_patent(patent_id, first_applicant_name, assignees_2, application_reference_4) — 专利去重, 第一申请人匹配, 当前专利权人匹配, 申请年份

## 待建字段

- 无

## 参考文献

- 企业能力｜国家市场监督管理总局｜国家市场监督管理总局, 国家标准化管理委员会. 企业竞争力评价规范: GB/T 40957—2021[S/OL]. (2021-11-26)[2026-08-21]. https://std.samr.gov.cn/gb/search/gbDetailed?id=D1E86BE73A99430EE05397BE0A0A206B
