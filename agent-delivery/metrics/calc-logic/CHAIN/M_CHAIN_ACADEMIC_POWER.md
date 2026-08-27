# 学术生态（M_CHAIN_ACADEMIC_POWER）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_ACADEMIC_POWER |
| 指标名称 | 学术生态 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业指数评价 |
| 三级模块 | 区域产业指数 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q055+QC05 |


## 口径定义

指定区域在指定产业链上的学术生态竞争力得分，取值0—100。由论文产出、科研机构、人才储备三维合成。

## 计算逻辑说明

三维等权。先按区域、链、年计算科研机构数、学者数、论文数，再在同一产业链、同一统计年度对全部对比区域做截面min-max归一化到[0,1]，算术平均后乘100。某维全部区域取值相同则该维取0.5。默认等权，前端可调权重但不另建权重表。区域用机构所在省、市过滤，深圳场景取city="深圳市"。从dwd_industry_chain_info确定目标产业链，关联dwd_org_industry_tags取链上主体。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 区域产业指数 | 学术生态 | 科研机构 | 区域链上高校与科研机构去重件数。国内科研用tags.credit_code关联dwd_research_institute_base_info.external_id，高校用tags.credit_code关联dwd_org_heis_info.external_id，均按province、city筛区域后按org_id去重； | dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称; dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上机构筛选, 信用代码关联, 机构名称匹配; dwd_research_institute_base_info(org_id, external_id, name_cn, province, city) — 国内科研机构标识, 信用代码关联, 机构名称, 省份, 城市; dwd_org_heis_info(org_id, external_id, name_cn, province, city) — 高校标识, 信用代码关联, 学校名称, 省份, 城市 | 无 |
| 区域产业指数 | 学术生态 | 人才储备 | 上述机构下学者去重人数。scholar_org_id等于机构org_id，或scholar_org_name_zh包含机构name_cn，按scholar_id去重 | dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称; dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上机构筛选, 信用代码关联, 机构名称匹配; dwd_research_institute_base_info(org_id, external_id, name_cn, province, city) — 国内科研机构标识, 信用代码关联, 机构名称, 省份, 城市; dwd_org_heis_info(org_id, external_id, name_cn, province, city) — 高校标识, 信用代码关联, 学校名称, 省份, 城市;  dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh) — 学者去重, 所属机构标识, 所属机构名称 | 无 |
| 区域产业指数 | 学术生态 | 论文产出 | 上述学者在统计年及以前的论文去重件数。经dwd_scholar_paper_relation按scholar_id关联，paper_id去重，year过滤统计年 | dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称; dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上机构筛选, 信用代码关联, 机构名称匹配; dwd_research_institute_base_info(org_id, external_id, name_cn, province, city) — 国内科研机构标识, 信用代码关联, 机构名称, 省份, 城市; dwd_org_heis_info(org_id, external_id, name_cn, province, city) — 高校标识, 信用代码关联, 学校名称, 省份, 城市;; dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh) — 学者去重, 所属机构标识, 所属机构名称; dwd_scholar_paper_relation(scholar_id, paper_id, year) — 学者论文关联, 论文去重, 发表年份 | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上机构筛选, 信用代码关联, 机构名称匹配
- dwd_research_institute_base_info(org_id, external_id, name_cn, province, city) — 国内科研机构标识, 信用代码关联, 机构名称, 省份, 城市
- dwd_org_heis_info(org_id, external_id, name_cn, province, city) — 高校标识, 信用代码关联, 学校名称, 省份, 城市
- dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh) — 学者去重, 所属机构标识, 所属机构名称
- dwd_scholar_paper_relation(scholar_id, paper_id, year) — 学者论文关联, 论文去重, 发表年份

## 待建字段

- 无

## 参考文献

- 学术生态｜中国科学院武汉文献情报中心｜钟永恒, 中国基础研究竞争力报告2020. 湖北省, 中国科学院武汉文献情报中心, 2020-10-01.
