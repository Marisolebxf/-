# 产业周期分析模型（M_CHAIN_DEEP_122_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_122_1 |
| 指标名称 | 产业周期分析模型 |
| 一级模块 | 产业链分析 |
| 二级模块 | 产业周期分析 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

基于历史与实时产业数据，构建产业周期阶段划分体系（起始期、成长期、成熟期、衰退期），依据市场规模、行业增长率、利润率、投融资趋势、企业数量趋势等指标值计算并判定产业所处周期阶段，预测未来趋势。对象=产业的整体生命周期阶段。

## 计算逻辑说明

① 数据采集：市场规模（`chain_market.total_revenue`）、行业增长率（`chain_market.growth_rate`）、投融资趋势（`chain_investment` 金额/数量增速）、企业趋势（`chain_enterprise_stat.growth_rate`）、利润率（由 `dwd_org_annual_financial_info` 汇总 pure_profit/operating_revenue）。② 阶段判定：按周期阶段评价指标与阈值（起始期=低规模高增速、成长期=高增速、成熟期=增速放缓、衰退期=负增长）映射 cycle_stage。③ 趋势预测：结合机器学习/统计模型输出 trend。

- 市场规模 = SUM(total_revenue)
- 行业增长率 = (本期规模 − 上期规模) ÷ 上期规模
- 利润率 = SUM(pure_profit) ÷ SUM(operating_revenue)
- 投融资趋势 = 当期投融资额增速
- 周期阶段 = 阈值映射(增长率, 投资趋势, 企业趋势)

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 产业周期分析模型 | 规模与增长 | 市场规模(营收) | 产业内企业营收合计。 | SUM(total_revenue) | chain_market(chain_id, chain_name, stat_year, total_revenue, enterprise_count, growth_rate)；enterprise_industry_summary(chain_code, chain_name, stat_year, revenue_total) | 无 |
|  |  | 行业增长率 | 产业规模同比增速。 | (本期 − 上期) ÷ 上期 | chain_market(growth_rate)；chain_enterprise_stat(growth_rate) | 无 |
| 产业周期分析模型 | 盈利与资本 | 利润率 | 产业整体净利润率。 | SUM(pure_profit) ÷ SUM(operating_revenue) | dwd_org_annual_financial_info(org_id, year, operating_revenue, total_profit, pure_profit)；dwd_org_industry_tags(credit_code) | 利润率汇总表（按产业归集） |
|  |  | 投融资趋势 | 产业投融资额/数量增速。 | 当期投融资额增速 | chain_investment(chain_id, chain_name, investment_id, amount, invest_date)；gkxlumenx_ads.chain_investment(chain_id, chain_name, stat_year, investment_count, total_amount, amount_growth_rate, count_growth_rate) | 无 |
| 产业周期分析模型 | 主体动态 | 企业数量趋势 | 产业内企业数量增速。 | (本期企业数 − 上期) ÷ 上期 | chain_enterprise_stat(chain_id, chain_name, stat_year, enterprise_count, growth_rate)；enterprise_industry_summary(enterprise_count) | 无 |
| 产业周期分析模型 | 阶段判定 | 周期阶段 | 判定起始期/成长期/成熟期/衰退期。 | 阈值映射(增长率, 投资趋势, 企业趋势) | gkxlumenx_ads.chain_cycle(chain_id, chain_name, growth_rate, investment_trend, enterprise_trend, cycle_stage, trend) | 周期阶段评价指标与阈值设定表 |

## 源表字段

- chain_market(chain_id, chain_name, stat_year, total_revenue, enterprise_count, growth_rate) — 市场规模与增长率
- enterprise_industry_summary(chain_code, chain_name, stat_year, enterprise_count, high_tech_count, research_staff_total, patent_total, revenue_total) — 产业汇总
- chain_investment(investment_id, chain_id, chain_name, enterprise_id, enterprise_name, round, amount, investor, invest_date, data_year) — 投融资明细
- chain_enterprise_stat(chain_id, chain_name, stat_year, enterprise_count, high_tech_count, growth_rate) — 企业数量与增长
- dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, total_profit, pure_profit, total_assets) — 财务（利润率）
- dwd_org_industry_tags(industry_code, industry_link_code, credit_code) — 企业-产业挂接
- gkxlumenx_ads.chain_investment(chain_id, chain_name, stat_year, investment_count, total_amount, amount_growth_rate, count_growth_rate) — 投融资年度汇总
- gkxlumenx_ads.chain_cycle(chain_id, chain_name, growth_rate, investment_trend, enterprise_trend, cycle_stage, trend) — 周期判定结果

## 待建字段

- 利润率按产业归集汇总表（当前需由企业财报按产业挂接二次汇总）
- 周期阶段评价指标与阈值设定表（各阶段指标区间与判定阈值）

## 参考资料

[1] 产业生命周期理论|Gort, M. & Klepper, S. (1982). Time Paths in the Diffusion of Product Innovations, The Economic Journal, 92(367), 630-653.

[2] 产品生命周期阶段划分|Vernon, R. (1966). International Investment and International Trade in the Product Cycle, The Quarterly Journal of Economics, 80(2), 190-207.

[3] 研究与试验发展（R&D）投入统计规范（试行）|国家统计局（国统字〔2019〕47号）|https://www.gov.cn/zhengce/zhengceku/2019-09/19/content_5426634.htm
