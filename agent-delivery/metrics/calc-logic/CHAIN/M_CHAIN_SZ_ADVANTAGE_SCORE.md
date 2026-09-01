# 深圳优势评分（M_CHAIN_SZ_ADVANTAGE_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SZ_ADVANTAGE_SCORE |
| 指标名称 | 深圳优势评分 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业情况分析对比 |
| 三级模块 | 综合优势 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q058+QC08 |


## 口径定义

指定产业链上，深圳相对默认对标城市的四维综合得分，取值0—100。四维为企业、专利、政策、人才。先定链，再按城市筛区域。本综合分的三级以本表为准：专利只用数量、政策只用数量，不含专利质量与政策强度。

## 计算逻辑说明

默认对标城市集合 \(C=\) \{北京市、上海市、广州市、深圳市\}，用 `city` 字段匹配（含「北京」「上海」「广州」「深圳」即可）。甲方可扩集合。深圳取 `city` 匹配深圳市。权重默认如下，甲方可改，但须同一层权重和为1。

| 层级 | 默认权重 |
| --- | --- |
| 四维 | 各 25% |
| 企业数量 / 规模 / 质量 | 各 1/3 |
| 专利数量 | 1 |
| 政策数量 | 1 |
| 人才数量 / 人才综合水平 | 各 1/2 |

第一步：定链后按城市取三级原始值

从 `dwd_industry_chain_info` 按 `industry_code` 定链。对每个对标城市 \(c\in C\) 计算：

- **企业数量**：`dwd_org_industry_tags` 链上企业，`credit_code` 关联 `dwd_org_base_info`，`city` 匹配 \(c\)，`COUNT(DISTINCT credit_code)`。
- **企业规模**：上述企业关联 `dwd_org_annual_financial_info`，统计年 `operating_revenue` 合计。
- **企业质量**：上述企业中能关联到 `dwd_org_stock_finance_info` 的上市样本，研发强度 = \(\sum\)`research_development_amount` / \(\sum\)`operating_revenue`。无上市样本则该市该三级取0。非上市不进入质量分。
- **专利数量**：上述企业 `company_name` 匹配 `dwd_patent.first_applicant_name` 或 `first_current_assignee_name`，`pbdt_year`≤统计年，`COUNT(DISTINCT patent_id)`。
- **政策数量**：`dwd_policy_base` 中 `status` 有效、`city` 匹配 \(c\)，且 `industry_name` 出现在 `title`/`keywords`/`keypoints`/`theme` 任一字段，`COUNT(DISTINCT id)`。
- **人才数量**：链上机构限定为 tags 中的 `credit_code`/`company_name` 能对上的高校、科研机构（`dwd_org_heis_info` / `dwd_research_institute_base_info` 的 `external_id` 或 `name_cn`），再筛 `city` 匹配 \(c\)；学者 `scholar_org_id` 或 `scholar_org_name_zh` 与这些机构对应，`COUNT(DISTINCT scholar_id)`。未挂到该链的全市学者不计入。
- **人才综合水平**：上述学者中，`dwd_scholar_education_background` 的 `degree_zh`/`degree_en` 含硕士、博士、Master、PhD、Doctor 等计为硕博。硕博占比 = 硕博人数 / 有学位记录的学者人数；分母为0则取0。

第二步：对标截面标准化

对每个三级指标 \(j\)，在集合 \(C\) 上 min-max 到 0—100：
$$
指标得分_{c,j} = \frac{x_{c,j}-\min_{c'\in C}(x_{c',j})}{\max_{c'\in C}(x_{c',j})-\min_{c'\in C}(x_{c',j})}\times 100
$$
全体对标城市该指标取值相同则得分取50。

第三步：维度分与综合分

企业维度 =（数量 + 规模 + 质量）/ 3  
专利维度 = 专利数量得分  
政策维度 = 政策数量得分  
人才维度 =（人才数量 + 人才综合水平）/ 2  
$$
深圳优势评分 = 0.25\times(企业+专利+政策+人才)
$$
输出深圳市在该链上的综合分。得分越高，相对对标城市的综合优势越强。

| 一级 | 二级 | 三级 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 深圳优势评分 | 企业 | 企业数量 | 该链、该市企业去重件数 | dwd_org_industry_tags(credit_code); dwd_org_base_info(city) | 无 |
| | | 企业规模 | 该链、该市企业统计年营业收入合计 | dwd_org_annual_financial_info(operating_revenue, year) | 无 |
| | | 企业质量 | 该链、该市上市企业研发强度 | dwd_org_stock_finance_info(research_development_amount, operating_revenue) | 无 |
| | 专利 | 专利数量 | 该链、该市企业专利去重件数（公开年≤统计年） | dwd_patent(patent_id, first_applicant_name, first_current_assignee_name, pbdt_year) | 无 |
| | 政策 | 政策数量 | 该市有效政策且命中产业链名称的去重件数 | dwd_policy_base(id, city, title, keywords, keypoints, theme, status) | 无 |
| | 人才 | 人才数量 | 该链上且位于该市的高校/科研机构所属学者去重人数 | dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh); dwd_org_heis_info(city); dwd_research_institute_base_info(city) | 无 |
| | | 人才综合水平 | 上述学者中有学位记录者的硕博占比 | dwd_scholar_education_background(degree_zh, degree_en) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称匹配政策
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业/机构筛选, 信用代码关联, 名称匹配
- dwd_org_base_info(external_id, city) — 信用代码关联, 对标城市筛选
- dwd_org_annual_financial_info(external_id, year, operating_revenue) — 年报年度, 营业收入(企业规模)
- dwd_org_stock_finance_info(external_id, occur_period, operating_revenue, research_development_amount) — 上市研发强度
- dwd_patent(patent_id, first_applicant_name, first_current_assignee_name, pbdt_year) — 专利去重, 申请人匹配, 专利权人匹配, 公开年
- dwd_policy_base(id, title, keywords, keypoints, theme, city, status) — 政策去重, 标题/关键词/要点/主题匹配产业, 城市, 有效状态
- dwd_org_heis_info(org_id, external_id, name_cn, city) — 高校对链上机构, 城市
- dwd_research_institute_base_info(org_id, external_id, name_cn, city) — 科研机构对链上机构, 城市
- dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh) — 学者去重, 所属机构
- dwd_scholar_education_background(scholar_id, degree_zh, degree_en) — 硕博识别

## 待建字段

- 无

## 参考文献

[1]深圳优势评分｜深圳市统计局｜深圳市2025年国民经济和社会发展统计公报[EB/OL]. (2026-02-28)[2026-08-21]. https://www.sz.gov.cn/cn/xxgk/zfxxgj/tjsj/tjgb/content/post_12805133.html.

[2]深圳优势评分｜国家市场监督管理总局，国家标准化管理委员会｜企业竞争力评价规范：GB/T 40957-2021[S/OL]. (2021-11-26)[2026-08-21]. https://std.samr.gov.cn/gb/search/gbDetailed?id=D1E86BE73A99430EE05397BE0A0A206B.

[3]深圳优势评分｜哈工大（深圳）课题组｜深圳企业高质量发展评价指标体系（2022）白皮书[R/OL]. (2022-11-23)[2026-08-21]. https://www.sznews.com.
