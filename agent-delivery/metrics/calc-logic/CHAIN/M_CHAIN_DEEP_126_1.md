# 区域产业指数模型（M_CHAIN_DEEP_126_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_126_1 |
| 指标名称 | 区域产业指数模型 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业指数评价 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

量化评估特定区域（省/市）产业发展水平与竞争力，从企业能力竞争力、学术生态竞争力、配套生态竞争力三大维度加权，计算区域产业指数，反映产业生态成熟度与潜力。对象=区域产业生态，不是单个企业。

## 计算逻辑说明

① 三维指标：企业能力（企业数量、高企占比、营收）、学术生态（科研机构数、论文/专利产出）、配套生态（服务机构数、融资活跃度）。② 各维评分：指标值极值归一后加权得 enterprise_score/academic_score/ecosystem_score。③ 综合：三维加权得 region_index，输出区域排名 rank_in_chain。

- 企业能力得分 = 归一化(企业数, 高企占比, 营收)
- 学术生态得分 = 归一化(科研机构数, 专利/论文产出)
- 配套生态得分 = 归一化(服务机构数, 融资额)
- 区域产业指数 region_index = Σ(Wi × 三维得分)

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 区域产业指数模型 | 企业能力竞争力 | 企业数量 | 区域内该产业去重企业数。 | COUNT(DISTINCT org_id/credit_code) | chain_national_dist(chain_id, chain_name, province, enterprise_count)；dwd_org_base_info(org_id, external_id, province, city) | 无 |
|  |  | 高新技术企业占比 | 高企数占企业总数比重。 | 高企数 ÷ 企业总数 | chain_enterprise_stat(chain_id, enterprise_count, high_tech_count)；dwd_org_tech_tag(org_id, org_tag) | 无 |
|  |  | 企业营收 | 区域企业营业收入合计。 | SUM(operating_revenue) | dwd_org_annual_financial_info(org_id, year, operating_revenue)；dwd_org_base_info(province, city) | 无 |
| 区域产业指数模型 | 学术生态竞争力 | 科研机构数 | 区域内科研机构去重数。 | COUNT(DISTINCT org_id) | dwd_research_institute_base_info(org_id, name_cn, province, city, org_type)；chain_national_dist(province, institution_count) | 无 |
|  |  | 论文/专利产出 | 区域论文与专利产出量。 | COUNT(DISTINCT 论文) + COUNT(DISTINCT 专利) | dwd_patent(pn, first_applicant_name)；dwd_zh_paper(id)；dwd_en_paper(id)；dwd_org_base_info(name_cn) | 无 |
| 区域产业指数模型 | 配套生态竞争力 | 服务机构数 | 区域产业服务机构去重数。 | COUNT(DISTINCT org_id) | demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, service_type_candidate)；dwd_org_base_info(province, city) | 无 |
|  |  | 融资活跃度 | 区域产业投融资额。 | SUM(amount) | dwd_org_financing_info(org_id, funding_amount, completion_date)；dwd_org_base_info(province, city) | 无 |
| 区域产业指数模型 | 综合评分 | 区域产业指数 | 三维加权综合指数。 | Σ(Wi × 三维得分) | gkxlumenx_ads.chain_region_index(chain_id, chain_name, province, enterprise_score, academic_score, ecosystem_score, region_index, enterprise_count, rank_in_chain)；gkxlumenx_ads.chain_competitiveness(chain_id, chain_name, province, index_score, growth_score, innovation_score, competitiveness_index, rank_in_chain) | 三维权重参数表 |

## 源表字段

- chain_national_dist(chain_id, chain_name, province, enterprise_count, institution_count, ratio) — 区域分省分布
- chain_region_dist(region_id, chain_id, chain_name, level, region_name, parent_region, enterprise_count, institution_count) — 区域分布
- chain_enterprise_stat(chain_id, chain_name, stat_year, enterprise_count, high_tech_count, growth_rate) — 企业数量与高企
- dwd_org_base_info(org_id, name_cn, external_id, province, city, org_type, listing_status) — 企业地域属性
- dwd_org_tech_tag(org_id, org_tag) — 高新技术标签
- dwd_research_institute_base_info(org_id, name_cn, province, city, org_type) — 科研机构
- dwd_org_annual_financial_info(org_id, year, operating_revenue) — 企业营收
- dwd_patent(pn, first_applicant_name) / dwd_zh_paper(id) / dwd_en_paper(id) — 论文/专利产出
- dwd_org_financing_info(org_id, funding_amount, completion_date) — 融资
- demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, service_type_candidate) — 服务机构
- gkxlumenx_ads.chain_region_index(chain_id, chain_name, province, enterprise_score, academic_score, ecosystem_score, region_index, enterprise_count, rank_in_chain) — 区域产业指数结果
- gkxlumenx_ads.chain_competitiveness(chain_id, chain_name, province, index_score, growth_score, innovation_score, competitiveness_index, rank_in_chain) — 区域竞争力结果

## 待建字段

- 学术生态与配套生态底层指标口径表（论文/服务机构/融资按区域归集）
- 三维权重与阈值参数表

## 参考资料

[1] 区域创新能力监测指标体系|科学技术部|https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/t20131129_110674.html

[2] 中国创新指数指标体系|国家统计局社科文司|https://www.stats.gov.cn/sj/zxfb/202302/t20230203_1900165.html

[3] 国家竞争优势「钻石模型」|Michael E. Porter, The Competitive Advantage of Nations, 1990.
