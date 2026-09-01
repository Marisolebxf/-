# 竞争力-企业能力（M_CHAIN_REG_COMP_ENTERPRISE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_COMP_ENTERPRISE |
| 指标名称 | 竞争力-企业能力 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业竞争力评价 |
| 三级模块 | 竞争力指数 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q055+QC05 |


## 口径定义

从企业规模、经营质量、创新能力等维度评估区域企业竞争力。

## 计算逻辑说明

采用加权平均。维度：企业规模/经营质量/创新能力。权重待甲方确认。

| 三级指标 | 计算方式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- |
| 人均产值 | 总产值（或营业收入）÷ 企业平均人数 | dwd_org_annual_financial_info(operating_revenue, employees_number) | 无 |
| 研发投入强度 | R&D经费 ÷ 营业收入 × 100% | dwd_org_stock_finance_info(research_development_amount, operating_revenue) | 无 |
| 有效专利数量 | 企业作为第一专利权人的有效发明专利总量 | dwd_patent(patent_id, first_current_assignee_name, kind, granted_number); dwd_patent_legal(status, expiration_year) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配
- dwd_org_base_info(external_id, city) — 企业信用代码关联, 城市筛选
- dwd_org_annual_financial_info(external_id, year, operating_revenue, employees_number) — 企业信用代码关联, 年报年度, 营业收入, 从业人数
- dwd_org_stock_finance_info(external_id, occur_period, operating_revenue, research_development_amount) — 上市企业信用代码关联, 数据期, 营业收入, 研发投入金额
- dwd_patent(patent_id, first_applicant_name, first_current_assignee_name, kind, granted_number) — 专利去重, 申请人匹配, 专利权人匹配, 申请类型, 授权判定
- dwd_patent_legal(pn, status, expiration_year) — 专利关联, 法律状态(有效授权), 到期年

## 待建字段

- 无

## 参考文献

- 企业能力｜国家市场监督管理总局｜国家市场监督管理总局, 国家标准化管理委员会. 企业竞争力评价规范: GB/T 40957—2021[S/OL]. (2021-11-26)[2026-08-19]. https://std.samr.gov.cn/gb/search/gbDetailed?id=D1E86BE73A99430EE05397BE0A0A206B
- 企业能力｜工业和信息化部｜工业和信息化部. 中小企业专精特新发展评价指标体系[EB/OL]. (2024-12-01)[2026-08-19]. http://gxj.zhangzhou.gov.cn/cms/html/zzsjjhxxhwyh/2024-12-16/765965713.html
