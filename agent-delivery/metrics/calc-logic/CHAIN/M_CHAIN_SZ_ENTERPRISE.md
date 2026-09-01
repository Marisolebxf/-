# 深圳企业维度（M_CHAIN_SZ_ENTERPRISE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SZ_ENTERPRISE |
| 指标名称 | 深圳企业维度 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业情况分析对比 |
| 三级模块 | 综合优势 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q058+QC08 |


## 口径定义

从企业数量、规模、质量等维度评估深圳企业相对优势。

## 计算逻辑说明

企业数量、规模、质量等维度加权评分。权重待甲方确认。

| 二级指标 | 三级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- |
| 企业 | 企业数量 | 深圳市企业总量 | dwd_org_industry_tags(credit_code); dwd_org_base_info(city) | 无 |
| 企业 | 企业规模 | 统计年度内深圳企业的营业收入总额 | dwd_org_annual_financial_info(operating_revenue, year) | 无 |
| 企业 | 企业质量 | 研发强度（研发经费占营业收入比重） | dwd_org_stock_finance_info(research_development_amount, operating_revenue) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配
- dwd_org_base_info(external_id, city) — 企业信用代码关联, 城市筛选
- dwd_org_annual_financial_info(external_id, year, operating_revenue) — 企业信用代码关联, 年报年度, 营业收入
- dwd_org_stock_finance_info(external_id, occur_period, operating_revenue, research_development_amount) — 上市企业信用代码关联, 数据期, 营业收入, 研发投入金额

## 待建字段

- 无

## 参考文献

- 深圳企业维度｜深圳市统计局｜深圳市统计局. 深圳市2025年国民经济和社会发展统计公报[EB/OL]. [2026-08-19]. https://www.sz.gov.cn/cn/xxgk/zfxxgj/tjsj/tjgb/content/post_12805133.html
- 深圳企业维度｜工业和信息化部｜工业和信息化部. 中小企业专精特新发展评价指标体系[EB/OL]. (2024-12-01)[2026-08-19]. http://gxj.zhangzhou.gov.cn/cms/html/zzsjjhxxhwyh/2024-12-16/765965713.html

对应Excel超链接：.\指标计算逻辑-V2\M_CHAIN_SZ_ENTERPRISE.md
