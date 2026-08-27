# 区域产业化程度（M_CHAIN_REG_COMMERCIALIZATION）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_COMMERCIALIZATION |
| 指标名称 | 区域产业化程度 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业指数评价 |
| 三级模块 | 区域产业指数 |
| 更新频率 | 年 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q055+QC05 |


## 口径定义

指定区域在指定产业链上，链上企业专利去重件数。

## 计算逻辑说明

COUNT(DISTINCT patent_id)。从dwd_industry_chain_info确定目标产业链，关联dwd_org_industry_tags取链上企业；用credit_code关联dwd_org_base_info筛区域；用company_name匹配dwd_patent.first_applicant_name或assignees_2，申请年份用application_reference_4过滤统计年及以前，按patent_id去重。

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配
- dwd_org_base_info(external_id, province, city) — 企业信用代码关联, 省份, 城市
- dwd_patent(patent_id, first_applicant_name, assignees_2, application_reference_4) — 专利去重, 第一申请人匹配, 当前专利权人匹配, 申请年份

## 待建字段

- 无
