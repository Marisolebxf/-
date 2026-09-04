# 产业阶段分析模型（M_CHAIN_DEEP_123_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_123_1 |
| 指标名称 | 产业阶段分析模型 |
| 一级模块 | 产业链分析 |
| 二级模块 | 产业周期分析 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

结合产业周期分析模型，依据生产能力、销售规模、市场份额、利润率等关键指标值判断产业所处发展阶段（成长期、成熟期或衰退期），为产业发展战略与资源配置提供量化参考。对象=产业的具体发展阶段（比周期模型更细的 sub_stage）。

## 计算逻辑说明

① 指标采集：生产能力/销售规模（`dwd_org_annual_financial_info` 营收与资产，`enterprise_industry_summary.revenue_total`）、市场份额（`chain_national_dist.ratio`）、利润率（纯利÷营收）。② 加权判定：按各指标权重加权得分，结合周期模型映射 cycle_stage 与 sub_stage，辅以高技术占比（high_tech_ratio）与投资强度（investment_intensity）。③ 输出阶段标识与分析报告。

- 销售规模 = SUM(operating_revenue)
- 生产能力 ≈ SUM(total_assets)（以资产总额近似）
- 市场份额 = 产业营收 ÷ 全产业营收
- 利润率 = SUM(pure_profit) ÷ SUM(operating_revenue)
- 高技术占比 = 高企数 ÷ 企业数
- 投资强度 = 投融资额 ÷ 营收

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 产业阶段分析模型 | 生产与销售 | 生产能力 | 产业内企业资产总额合计（近似生产规模）。 | SUM(total_assets) | dwd_org_annual_financial_info(org_id, year, total_assets, operating_revenue)；dwd_org_industry_tags(credit_code) | 生产能力指标表 |
|  |  | 销售规模 | 产业内企业营业收入合计。 | SUM(operating_revenue) | dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue)；enterprise_industry_summary(chain_code, chain_name, stat_year, revenue_total) | 无 |
| 产业阶段分析模型 | 市场与盈利 | 市场份额 | 产业营收/企业占全产业比重。 | 产业营收 ÷ 全产业营收合计 | chain_national_dist(chain_id, chain_name, province, enterprise_count, ratio)；chain_market(chain_id, chain_name, total_revenue, enterprise_count, growth_rate) | 市场份额指标表 |
|  |  | 利润率 | 产业净利润率。 | SUM(pure_profit) ÷ SUM(operating_revenue) | dwd_org_annual_financial_info(org_id, year, operating_revenue, total_profit, pure_profit) | 利润率指标表 |
| 产业阶段分析模型 | 阶段判定 | 发展阶段 | 判定成长期/成熟期/衰退期（含 sub_stage）。 | 指标加权 + 周期模型映射 | gkxlumenx_ads.chain_stage(chain_id, chain_name, cycle_stage, sub_stage, high_tech_ratio, investment_intensity, growth_rate) | 阶段指标权重与阈值参数表 |
|  |  | 高技术占比 | 高新技术企业占企业总数比重。 | 高企数 ÷ 企业总数 | chain_enterprise_stat(chain_id, chain_name, enterprise_count, high_tech_count)；dwd_org_tech_tag(org_id, org_tag) | 无 |
|  |  | 投资强度 | 产业投融资额与营收比值。 | 投融资额 ÷ 营收 | chain_investment(amount)；chain_market(total_revenue) | 无 |

## 源表字段

- dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, total_assets, total_profit, pure_profit, employees_number) — 财务指标
- enterprise_industry_summary(chain_code, chain_name, stat_year, enterprise_count, high_tech_count, research_staff_total, patent_total, revenue_total) — 产业汇总
- chain_national_dist(chain_id, chain_name, province, enterprise_count, institution_count, ratio) — 区域分布（市场份额）
- chain_market(chain_id, chain_name, stat_year, total_revenue, enterprise_count, growth_rate) — 市场规模
- chain_enterprise_stat(chain_id, chain_name, stat_year, enterprise_count, high_tech_count, growth_rate) — 企业数量与高企数
- chain_investment(chain_id, chain_name, investment_id, amount, invest_date) — 投融资
- dwd_org_tech_tag(org_id, org_tag) — 高新技术企业标签
- dwd_org_industry_tags(industry_code, industry_link_code, credit_code) — 企业-产业挂接
- gkxlumenx_ads.chain_stage(chain_id, chain_name, cycle_stage, sub_stage, high_tech_ratio, investment_intensity, growth_rate) — 阶段判定结果

## 待建字段

- 生产能力指标表（产能、产量等，当前以资产总额近似）
- 市场份额指标表（全产业分母口径）
- 利润率指标表（按产业归集）
- 阶段判定指标权重与阈值参数表

## 参考资料

[1] 产业生命周期理论|Gort, M. & Klepper, S. (1982). Time Paths in the Diffusion of Product Innovations, The Economic Journal, 92(367), 630-653.

[2] 高新技术企业认定管理办法（国科发火〔2016〕32号）|科技部、财政部、税务总局|https://www.gov.cn/gongbao/content/2016/content_5076985.htm

[3] 研究与试验发展（R&D）投入统计规范（试行）|国家统计局|https://www.gov.cn/zhengce/zhengceku/2019-09/19/content_5426634.htm
