# 深圳机遇分析模型（M_CHAIN_DEEP_128_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_128_1 |
| 指标名称 | 深圳机遇分析模型 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

基于深圳产业优势与问题分析，结合专家知识与多源区域数据（经济统计、人口、重点产业分布），识别核心优势产业与关键制约因素，生成面向产业发展、政策优化和创新方向的机遇推荐结果。对象=深圳产业机遇，机遇指数越高越值得布局。

## 计算逻辑说明

① 优势+问题综合：复用优势识别（advantages/weaknesses）与问题识别（problems）结果。② 机遇打分：趋势得分（trend_score，结合周期阶段 cycle_stage 与 growth_rate）、政策得分（policy_score，政策支持强度）、市场得分（market_score，市场规模潜力）。③ 综合：三维加权得 opportunity_index，输出机遇清单、发展建议与 rank_overall。

- 趋势得分 = 归一化(周期阶段×增长率)
- 政策得分 = 归一化(政策支持强度)
- 市场得分 = 归一化(市场规模潜力)
- 机遇指数 opportunity_index = Σ(Wi × 三维得分)

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 深圳机遇分析模型 | 优势与问题综合 | 优势项 | 深圳产业优势维度清单。 | 复用优势识别 advantages | chain_sz_advantage(chain_id, chain_name, advantages, weaknesses, advantage_index) | 无 |
|  |  | 问题项 | 深圳产业短板维度清单。 | 复用问题识别 weaknesses/problems | chain_sz_problem(chain_id, chain_name, problems, causes, suggestions) | 无 |
| 深圳机遇分析模型 | 趋势与政策 | 趋势得分 | 结合周期阶段与增长率的趋势评分。 | 归一化(cycle_stage × growth_rate) | gkxlumenx_ads.chain_sz_opportunity(chain_id, chain_name, cycle_stage, growth_rate, trend_score)；chain_cycle(chain_id, chain_name, cycle_stage, growth_rate, trend) | 无 |
|  |  | 政策得分 | 深圳/国家政策支持强度评分。 | 归一化(政策数量/级别) | dwd_policy_base(id, title, publish_year, rank, type, theme, status, province, city)；chain_sz_opportunity(policy_score) | 无 |
|  |  | 市场得分 | 市场规模与潜力评分。 | 归一化(市场规模/增长率) | chain_market(chain_id, chain_name, stat_year, total_revenue, growth_rate)；chain_sz_opportunity(market_score) | 无 |
| 深圳机遇分析模型 | 机遇判定 | 机遇指数 | 三维加权综合机遇分。 | Σ(Wi × 三维得分) | gkxlumenx_ads.chain_sz_opportunity(chain_id, chain_name, opportunity_index, advantages, weaknesses, suggestions, rank_overall) | 专家策略与权重参数表 |
|  |  | 机遇排名 | 深圳产业机遇按指数的名次。 | RANK() OVER (ORDER BY opportunity_index DESC) | gkxlumenx_ads.chain_sz_opportunity(opportunity_index, rank_overall) | 无 |

## 源表字段

- chain_sz_advantage(chain_id, chain_name, advantages, weaknesses, advantage_index) — 优势识别结果
- chain_sz_problem(chain_id, chain_name, problems, causes, suggestions, problem_count) — 问题识别结果
- chain_cycle(chain_id, chain_name, growth_rate, cycle_stage, trend) — 周期阶段
- chain_market(chain_id, chain_name, stat_year, total_revenue, enterprise_count, growth_rate) — 市场规模
- dwd_policy_base(id, title, publish_year, rank, type, theme, status, province, city) — 政策
- dwd_macro_index_data(index_code, occur_period, area_code, index_value, unit_use) — 宏观经济指标
- gkxlumenx_ads.chain_sz_opportunity(chain_id, chain_name, cycle_stage, growth_rate, trend_score, policy_score, market_score, opportunity_index, advantages, weaknesses, suggestions, rank_overall) — 机遇分析结果

## 待建字段

- 年度经济统计源表（GDP、产业增加值等宏观事实按产业拆解）
- 人口普查源表（人口结构/人才流动）
- 专家策略配置表（策略规则、权重、评估规则）

## 参考资料

[1] SWOT 分析法|Andrews, K. R. (1971). The Concept of Corporate Strategy.

[2] 国家竞争优势「钻石模型」|Michael E. Porter, The Competitive Advantage of Nations, 1990.

[3] 深圳市国民经济和社会发展统计公报|深圳市统计局|https://tjj.sz.gov.cn/

[4] 区域创新能力监测指标体系|科学技术部|https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/t20131129_110674.html
