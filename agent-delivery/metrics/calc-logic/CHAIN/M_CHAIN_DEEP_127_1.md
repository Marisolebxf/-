# 深圳问题识别模型（M_CHAIN_DEEP_127_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_127_1 |
| 指标名称 | 深圳问题识别模型 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业情况分析对比 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

通过深圳与全国多领域数据对比，设定企业亏损率、环保违规次数、行业不合格率等负面评价指标，结合深圳与全国同类指标对比，识别深圳产业薄弱环节与突出问题，生成问题清单与优先级排序。对象=深圳产业短板与风险，指标越高问题越突出。

## 计算逻辑说明

① 负面指标：企业亏损率（`dwd_org_annual_financial_info` 净利润<0 企业占比）、企业增长率（`chain_enterprise_stat`）、环保违规次数、行业不合格率。② 深圳 vs 全国对比：深圳值相对全国基线的偏离度。③ 问题判定：负面指标超阈值维度标记为 problems，按 tech/talent/market/capital/policy 五维归因，输出 causes/suggestions 与 problem_count。

- 企业亏损率 = 净利润<0 企业数 ÷ 企业总数
- 问题对比偏离度 = (深圳指标 − 全国指标) ÷ 全国指标
- 问题清单 = 偏离度超阈值的负面指标项

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 深圳问题识别模型 | 经营维度 | 企业亏损率 | 深圳产业内亏损企业占比。 | COUNT(净利润<0) ÷ COUNT(企业) | dwd_org_annual_financial_info(org_id, year, pure_profit, total_profit, operating_revenue)；dwd_org_base_info(city, province) | 企业亏损率口径表 |
|  |  | 企业增长率 | 深圳产业企业数量增速（相对全国）。 | 深圳增速 − 全国增速 | chain_enterprise_stat(chain_id, enterprise_count, growth_rate)；enterprise_industry_distribution(region_code, enterprise_count, ratio) | 无 |
| 深圳问题识别模型 | 合规维度 | 环保违规次数 | 深圳产业企业环保违规事件数。 | COUNT(环保违规记录) | 现库无环保违规专用表 | 环保违规记录表 |
|  |  | 行业不合格率 | 深圳产业产品/服务不合格率。 | 不合格批次 ÷ 检验批次 | 现库无质检不合格专用表 | 行业不合格率表 |
| 深圳问题识别模型 | 综合判定 | 问题清单 | 负面指标超阈值的维度归因。 | 阈值判定 + 五维归因 | gkxlumenx_ads.chain_sz_problem(chain_id, chain_name, tech_score, talent_score, market_score, capital_score, policy_score, problems, causes, suggestions, problem_count) | 负面评价指标权重与阈值参数表 |
|  |  | 问题数量 | 识别出的问题项数量。 | COUNT(问题项) | gkxlumenx_ads.chain_sz_problem(problem_count) | 无 |

## 源表字段

- dwd_org_annual_financial_info(org_id, year, operating_revenue, total_profit, pure_profit) — 财务（亏损率）
- dwd_org_base_info(org_id, name_cn, external_id, province, city, reg_status) — 企业地域与存续
- chain_enterprise_stat(chain_id, chain_name, stat_year, enterprise_count, growth_rate) — 企业数量与增长
- enterprise_industry_distribution(region_code, chain_code, chain_name, enterprise_count, ratio, stat_date) — 区域企业分布
- chain_national_dist(chain_id, chain_name, province, enterprise_count, ratio) — 全国基线
- chain_sz_advantage(chain_id, chain_name, sz_enterprise_count, sz_share, growth_rate, advantages, weaknesses) — 深圳优势/短板
- gkxlumenx_ads.chain_sz_problem(chain_id, chain_name, tech_score, talent_score, market_score, capital_score, policy_score, problems, causes, suggestions, problem_count) — 问题识别结果

## 待建字段

- 环保违规记录表（企业环保处罚/违规事件）
- 行业不合格率表（质检/抽检不合格数据）
- 企业亏损率口径表（按产业归集）
- 负面评价指标权重与阈值参数表

## 参考资料

[1] 产业安全与负面评价指标|工业和信息化部|产业链供应链韧性与安全相关|https://www.miit.gov.cn/

[2] 环境违法与环保处罚信息公开|生态环境部|https://www.mee.gov.cn/

[3] 产品质量监督抽查管理暂行办法|市场监管总局|https://www.samr.gov.cn/
