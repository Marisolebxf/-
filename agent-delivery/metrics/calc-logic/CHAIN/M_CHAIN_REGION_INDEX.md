# 区域产业指数（M_CHAIN_REGION_INDEX）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REGION_INDEX |
| 指标名称 | 区域产业指数 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业指数评价 |
| 三级模块 | 区域产业指数 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q055+QC05 |


## 口径定义

指定区域在指定产业链上的综合发展指数，取值0—100。按算法库区域产业指数模型，综合企业能力竞争力、学术生态竞争力、配套生态竞争力三维。用于同一产业链下多区域对比。原型四力展示词不得覆盖本指标三维名称。

## 计算逻辑说明

三维等权，维内子项等权。先按区域、链、年计算各子项原始值，再在同一产业链、同一统计年度对全部对比区域做截面min-max归一化到[0,1]，维内平均得到维分，三维算术平均后乘100。配套维政策子项用政策覆盖率，不用政策条数。默认等权，前端可调权重但不另建权重表。区域用机构所在省、市过滤，深圳场景取city或province含深圳。从dwd_industry_chain_info确定目标产业链，关联dwd_org_industry_tags取链上企业，再关联基本信息筛区域。

| 一级指标 | 二级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- |
| 区域产业指数 | 企业能力竞争力 | 维内等权：区域链上企业数、营业收入合计、专利去重件数。企业数按credit_code去重；营收国内按year、海外按occur_period汇总operating_revenue；专利用company_name匹配first_applicant_name或assignees_2 | dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称; dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配; dwd_org_base_info(external_id, province, city) — 国内企业信用代码关联, 省份, 城市; dwd_forg_base_info(org_id, name_en, city, state) — 海外企业标识, 企业名称匹配, 城市, 州省; dwd_org_annual_financial_info(external_id, year, operating_revenue) — 国内企业信用代码关联, 年报年度, 营业收入; dwd_foreign_org_annual_financial_info(org_id, occur_period, operating_revenue) — 海外企业财务关联, 报表数据期, 营业收入; dwd_patent(patent_id, first_applicant_name, assignees_2, application_reference_4) — 专利去重, 第一申请人匹配, 当前专利权人匹配, 申请年份 | 无 |
| 区域产业指数 | 学术生态竞争力 | 维内等权：区域链上科研机构数、机构下学者数、学者论文数。国内科研用tags.credit_code关联dwd_research_institute_base_info.external_id并按province、city筛区域；海外科研用company_name关联dwd_forg_research_org_info.name_std并按city、region筛区域；学者用scholar_org_id或scholar_org_name_zh对齐上述机构；论文经dwd_scholar_paper_relation按scholar_id、paper_id去重，year过滤统计年 | dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称; dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上机构筛选, 信用代码关联, 机构名称匹配; dwd_research_institute_base_info(org_id, external_id, name_cn, province, city) — 国内科研机构标识, 信用代码关联, 机构名称, 省份, 城市; dwd_forg_research_org_info(org_id, name_std, city, region) — 海外科研机构标识, 机构名称匹配, 城市, 行政区划; dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh) — 学者去重, 所属机构标识, 所属机构名称; dwd_scholar_paper_relation(scholar_id, paper_id, year) — 学者论文关联, 论文去重, 发表年份 | 无 |
| 区域产业指数 | 配套生态竞争力 | 维内等权：政策覆盖率、区域链上融资事件数。政策覆盖率=政策命中环节数/全链环节数×100%，口径同M_CHAIN_REG_POLICY_COVERAGE。融资用链上企业credit_code关联dwd_org_financing_info，按org_id与completion_date去重。库无独立服务机构产业链表，不另建 | dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 目标产业链范围, 产业链名称, 全链环节去重, 环节名称匹配政策; dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配; dwd_org_base_info(external_id, province, city) — 国内企业信用代码关联, 省份, 城市; dwd_policy_base(id, title, keywords, keypoints, theme, province, city, status, publish_year, rank) — 政策去重, 标题匹配环节, 关键词匹配环节, 要点匹配环节, 主题匹配环节, 政策省份, 政策城市, 有效状态, 发布年, 国家级覆盖全部区域; dwd_org_financing_info(org_id, external_id, completion_date, funding_amount) — 融资企业标识, 信用代码关联, 融资完成时间, 融资金额 | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 目标产业链范围, 产业链名称, 全链环节去重, 环节名称匹配政策
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配
- dwd_org_base_info(external_id, province, city) — 国内企业信用代码关联, 省份, 城市
- dwd_forg_base_info(org_id, name_en, city, state) — 海外企业标识, 企业名称匹配, 城市, 州省
- dwd_org_annual_financial_info(external_id, year, operating_revenue) — 国内企业信用代码关联, 年报年度, 营业收入
- dwd_foreign_org_annual_financial_info(org_id, occur_period, operating_revenue) — 海外企业财务关联, 报表数据期, 营业收入
- dwd_patent(patent_id, first_applicant_name, assignees_2, application_reference_4) — 专利去重, 第一申请人匹配, 当前专利权人匹配, 申请年份
- dwd_research_institute_base_info(org_id, external_id, name_cn, province, city) — 国内科研机构标识, 信用代码关联, 机构名称, 省份, 城市
- dwd_forg_research_org_info(org_id, name_std, city, region) — 海外科研机构标识, 机构名称匹配, 城市, 行政区划
- dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh) — 学者去重, 所属机构标识, 所属机构名称
- dwd_scholar_paper_relation(scholar_id, paper_id, year) — 学者论文关联, 论文去重, 发表年份
- dwd_policy_base(id, title, keywords, keypoints, theme, province, city, status, publish_year, rank) — 政策去重, 标题匹配环节, 关键词匹配环节, 要点匹配环节, 主题匹配环节, 政策省份, 政策城市, 有效状态, 发布年, 国家级覆盖全部区域
- dwd_org_financing_info(org_id, external_id, completion_date, funding_amount) — 融资企业标识, 信用代码关联, 融资完成时间, 融资金额

## 待建字段

- 无

## 参考文献

- 区域产业指数｜中国科技发展战略研究小组；中国科学院大学中国创新创业管理研究中心｜中国科技发展战略研究小组, 中国科学院大学中国创新创业管理研究中心. 中国区域创新能力评价报告2024[R]. 北京: 科学技术文献出版社, 2024. http://www.news.cn/tech/20241104/9da6e6839a604358b28dd670034a9f28/c.html
- 区域产业指数｜经济合作与发展组织（OECD）；欧盟委员会联合研究中心（JRC）｜OECD, European Commission Joint Research Centre. Handbook on constructing composite indicators: methodology and user guide[R]. Paris: OECD Publishing, 2008. DOI: 10.1787/9789264043466-en. https://doi.org/10.1787/9789264043466-en
- 区域产业指数｜国家市场监督管理总局｜国家市场监督管理总局, 国家标准化管理委员会. 企业竞争力评价规范: GB/T 40957—2021[S/OL]. (2021-11-26)[2026-08-21]. https://std.samr.gov.cn/gb/search/gbDetailed?id=D1E86BE73A99430EE05397BE0A0A206B

对应Excel超链接：.\指标计算逻辑-V2\M_CHAIN_REGION_INDEX.md
