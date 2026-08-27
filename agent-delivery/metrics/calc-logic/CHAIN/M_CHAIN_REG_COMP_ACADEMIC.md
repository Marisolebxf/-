# 竞争力-学术生态（M_CHAIN_REG_COMP_ACADEMIC）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_COMP_ACADEMIC |
| 指标名称 | 竞争力-学术生态 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业竞争力评价 |
| 三级模块 | 竞争力指数 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q055+QC05 |


## 口径定义

从论文产出、科研机构、人才供给等维度评估区域学术生态竞争力。

## 计算逻辑说明

采用加权平均。维度：论文产出/科研机构/人才供给。权重待甲方确认。

| 三级指标 | 计算方式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- |
| 论文产出 | 链上高校与科研机构所属学者发表论文去重件数 | dwd_scholar(scholar_id, scholar_org_name_zh); dwd_scholar_paper_relation(scholar_id, paper_id, year); dwd_scholar_papers(id, status); dwd_org_heis_info(name_cn, city); dwd_research_institute_base_info(name_cn, city) | 无 |
| 人才储备 | 链上高校与科研机构所属学者去重人数 | dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh); dwd_org_heis_info(name_cn, city); dwd_research_institute_base_info(name_cn, city) | 无 |
| 科研机构 | 链上高校与科研机构去重数量 | dwd_org_heis_info(org_id, external_id, name_cn, city); dwd_research_institute_base_info(org_id, external_id, name_cn, city); dwd_org_industry_tags(credit_code) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上机构筛选, 信用代码关联, 机构名称匹配
- dwd_org_base_info(external_id, city) — 信用代码关联, 区域城市筛选
- dwd_org_heis_info(org_id, external_id, name_cn, city) — 高校去重(科研机构), 信用代码关联, 学校名称匹配学者, 区域筛选
- dwd_research_institute_base_info(org_id, external_id, name_cn, city) — 科研机构去重, 信用代码关联, 机构名称匹配学者, 区域筛选
- dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh) — 学者去重(人才供给/人才储备), 所属机构关联
- dwd_scholar_paper_relation(scholar_id, paper_id, year) — 学者论文关联, 论文产出去重, 发表年
- dwd_scholar_papers(id, status) — 论文去重, 有效状态

## 待建字段

- 无

## 参考文献

- 学术生态竞争力｜国家市场监督管理总局｜国家市场监督管理总局, 国家标准化管理委员会. 企业竞争力评价规范: GB/T 40957—2021[S/OL]. (2021-11-26)[2026-08-19]. https://std.samr.gov.cn/gb/search/gbDetailed?id=D1E86BE73A99430EE05397BE0A0A206B
- 学术生态竞争力｜国务院｜国务院. 李强主持召开国务院常务会议 审议通过关于加快发展先进制造业集群的意见等[EB/OL]. (2023-05-05)[2026-08-19]. https://www.gov.cn/yaowen/2023-05/05/content_5754266.htm
