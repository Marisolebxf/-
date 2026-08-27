# 深圳专利维度（M_CHAIN_SZ_PATENT）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SZ_PATENT |
| 指标名称 | 深圳专利维度 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业情况分析对比 |
| 三级模块 | 综合优势 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q058+QC08 |


## 口径定义

从专利数量与质量等维度评估深圳专利相对优势。

## 计算逻辑说明

专利数量、专利质量等维度加权评分。权重待甲方确认。

| 二级指标 | 三级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- |
| 专利 | 专利数量 | 深圳市专利总量 | dwd_patent(patent_id, first_applicant_name, first_current_assignee_name) | 无 |
| 专利 | 专利质量 | 专利价值 | dwd_patent(value) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配
- dwd_org_base_info(external_id, city) — 企业信用代码关联, 城市筛选
- dwd_patent(patent_id, first_applicant_name, first_current_assignee_name, value) — 专利去重(专利数量), 申请人匹配, 专利权人匹配, 专利价值(专利质量)

## 待建字段

- 无

## 参考文献

- 深圳专利维度｜深圳市统计局｜深圳市统计局. 深圳市2025年国民经济和社会发展统计公报[EB/OL]. [2026-08-19]. https://www.sz.gov.cn/cn/xxgk/zfxxgj/tjsj/tjgb/content/post_12805133.html
- 深圳专利维度｜山东省工业和信息化厅｜山东省企业技术中心评价指标体系[EB/OL]. [2026-08-19]. http://www.lckfq.gov.cn/resources/oldres/cd6937aac19dc34b3aef5b6c635d8b07.pdf

对应Excel超链接：.\指标计算逻辑-V2\M_CHAIN_SZ_PATENT.md
