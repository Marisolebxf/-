# 深圳人才维度（M_CHAIN_SZ_TALENT）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SZ_TALENT |
| 指标名称 | 深圳人才维度 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业情况分析对比 |
| 三级模块 | 综合优势 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q058+QC08 |


## 口径定义

从人才数量与结构等维度评估深圳人才相对优势。

## 计算逻辑说明

人才数量、人才结构等维度加权评分。权重待甲方确认。

| 二级指标 | 三级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- |
| 人才 | 人才数量 | 深圳市人才总量 | dwd_scholar(scholar_id, scholar_org_name_zh); dwd_org_heis_info(city); dwd_research_institute_base_info(city) | 无 |
| 人才 | 人才综合水平 | 硕博人员占比 | dwd_scholar_education_background(degree_zh, degree_en) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配
- dwd_org_heis_info(org_id, external_id, name_cn, province, city) — 高校标识, 信用代码关联, 学校名称, 省份, 城市
- dwd_research_institute_base_info(org_id, external_id, name_cn, province, city) — 国内科研机构标识, 信用代码关联, 机构名称, 省份, 城市
- dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh) — 学者去重, 所属机构标识, 所属机构名称
- dwd_scholar_education_background(scholar_id, degree_zh, degree_en) — 学者关联, 中文学位, 英文学位

## 待建字段

- 无

## 参考文献

- 深圳人才维度｜深圳市统计局｜深圳市统计局. 深圳市2025年国民经济和社会发展统计公报[EB/OL]. [2026-08-19]. https://www.sz.gov.cn/cn/xxgk/zfxxgj/tjsj/tjgb/content/post_12805133.html
- 深圳人才维度｜国务院｜国务院. 李强主持召开国务院常务会议 审议通过关于加快发展先进制造业集群的意见等[EB/OL]. (2023-05-05)[2026-08-19]. https://www.gov.cn/yaowen/2023-05/05/content_5754266.htm

对应Excel超链接：.\指标计算逻辑-V2\M_CHAIN_SZ_TALENT.md
