# 深圳产业优势识别模型（M_CHAIN_DEEP_121_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_121_1 |
| 指标名称 | 深圳产业优势识别模型 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

通过对比深圳与全国各产业数据，从行业增长率、市场占有率、技术创新能力等维度构建评价体系，识别深圳具有竞争力与发展优势的产业领域，生成优势产业清单与优势评分。对象=深圳产业相对全国的优势，不是绝对规模。

## 计算逻辑说明

① 数据采集：深圳产业数据（`chain_sz_dist`/`chain_sz_elements`）、全国产业数据（`chain_national_dist`）。② 指标计算：市场占有率=深圳企业数÷全国企业数（sz_share），行业增长率（growth_rate），技术创新能力=深圳专利数（`dwd_patent` 按深圳申请人）。③ 优势评分：份额分（share_score）+ 排名分（rank_score）+ 增长分（growth_score）加权得 advantage_index，输出 advantages/weaknesses/suggestions 与 rank_overall。

- 市场占有率 sz_share = 深圳企业数 ÷ 全国企业数 × 100%
- 行业增长率 growth_rate = (本期规模 − 上期规模) ÷ 上期规模
- 技术创新能力 = COUNT(DISTINCT pn) WHERE 深圳申请人
- 优势指数 advantage_index = Σ(Wi × 子评分)

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 深圳产业优势识别模型 | 市场维度 | 深圳企业占比(市场占有率) | 深圳企业数占全国同产业企业数比重。 | 深圳企业数 ÷ 全国企业数 × 100% | chain_national_dist(chain_id, chain_name, province, enterprise_count, institution_count, ratio)；chain_sz_dist(chain_id, chain_name, district, enterprise_count)；enterprise_industry_distribution(region_code, chain_code, chain_name, enterprise_count, ratio, stat_date) | 无 |
|  |  | 行业增长率 | 深圳该产业企业/营收同比增速。 | (本期 − 上期) ÷ 上期 | chain_enterprise_stat(chain_id, chain_name, stat_year, enterprise_count, growth_rate)；chain_market(chain_id, chain_name, stat_year, total_revenue, growth_rate) | 无 |
| 深圳产业优势识别模型 | 创新维度 | 技术创新能力(专利数) | 深圳申请人的专利授权去重数。 | COUNT(DISTINCT pn) WHERE 深圳申请人 | dwd_patent(pn, kind, granted_number, first_applicant_name, applicants, pbdt_year, apdt_year)；dwd_org_base_info(org_id, name_cn, city, external_id) | 无 |
| 深圳产业优势识别模型 | 综合评分 | 优势指数 | 份额/排名/增长三子分加权的优势综合分。 | Σ(Wi × 子评分) | gkxlumenx_ads.chain_sz_advantage(chain_id, chain_name, sz_enterprise_count, sz_share, sz_rank, growth_rate, share_score, rank_score, growth_score, advantage_index, advantages, weaknesses, suggestions, rank_overall) | 优势评分权重与阈值参数表 |
|  |  | 优势产业排名 | 深圳优势产业按优势指数的名次。 | RANK() OVER (ORDER BY advantage_index DESC) | gkxlumenx_ads.chain_sz_advantage(advantage_index, rank_overall) | 无 |

## 源表字段

- chain_national_dist(chain_id, chain_name, province, enterprise_count, institution_count, ratio) — 全国分省分布（分母）
- chain_sz_dist(chain_id, chain_name, district, enterprise_count, institution_count) — 深圳分区分布（分子）
- chain_sz_elements(chain_id, chain_name, enterprise_count, institution_count, talent_count, total_revenue) — 深圳产业要素
- enterprise_industry_distribution(region_code, chain_code, chain_name, enterprise_count, ratio, stat_date) — 区域-产业企业分布
- chain_enterprise_stat(chain_id, chain_name, stat_year, enterprise_count, high_tech_count, growth_rate) — 企业数量与增长
- chain_market(chain_id, chain_name, stat_year, total_revenue, enterprise_count, growth_rate) — 市场规模与增长
- dwd_patent(pn, kind, granted_number, first_applicant_name, applicants, pbdt_year, apdt_year) — 专利（技术创新能力）
- dwd_org_base_info(org_id, name_cn, external_id, city, province, reg_status) — 企业地域
- dwd_org_industry_tags(industry_code, industry_link_code, credit_code, company_name) — 企业-产业挂接
- gkxlumenx_ads.chain_sz_advantage(chain_id, chain_name, sz_enterprise_count, sz_share, sz_rank, growth_rate, share_score, rank_score, growth_score, advantage_index, advantages, weaknesses, suggestions, rank_overall) — 优势识别结果

## 待建字段

- 市场占有率统一口径表（深圳/全国分子分母标准化）
- 行业增长率分子分母口径表
- 优势评分权重与阈值参数表

## 参考资料

[1] 比较优势理论|David Ricardo, On the Principles of Political Economy and Taxation, 1817.

[2] 国家竞争优势「钻石模型」|Michael E. Porter, The Competitive Advantage of Nations, 1990.

[3] 深圳市「20+8」产业集群行动方案|深圳市人民政府|https://gxj.sz.gov.cn/

[4] 区域创新能力监测指标体系|科学技术部|https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/t20131129_110674.html
