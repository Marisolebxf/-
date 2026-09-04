# 深圳产业机遇评分（M_CHAIN_SZ_OPPORTUNITY_SCORE）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SZ_OPPORTUNITY_SCORE |
| 指标名称 | 深圳产业机遇评分 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 周 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

深圳在指定产业链上的机遇综合评分，从趋势机遇、政策机遇、市场机遇三维加权评定，取值 0—100。分数越高表示深圳在该产业链的机遇越强。评分维度与权重待甲方确认。

## 计算逻辑说明

采用加权平均。三维：趋势机遇 / 政策机遇 / 市场机遇。算法库「深圳机遇分析模型」（1.1.1.1.1.1.1.3.12）要求「融合优势识别结果与问题分析结果，运用机器学习方法进行区域机遇的预测与推荐」，输出机遇综合评估。`chain_sz_opportunity` 已含 trend_score / policy_score / market_score / opportunity_index，默认等权（ΣW=1）。

### 计算步骤

1. 按 `chain_id` 定链，取 `chain_sz_opportunity`。
2. 三维取值：`trend_score`（趋势）、`policy_score`（政策）、`market_score`（市场）。
3. 综合分：
$$
深圳产业机遇评分 = \frac{1}{3}(趋势机遇得分 + 政策机遇得分 + 市场机遇得分)
$$
（可直接取 `opportunity_index` 作为综合分，若其口径与三维等权一致。）

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 深圳产业机遇评分 | 趋势机遇 | 趋势机遇得分 | 产业发展趋势机遇评分 | trend_score | chain_sz_opportunity(chain_id, trend_score, cycle_stage, growth_rate) — 趋势分 | 无 |
|  | 政策机遇 | 政策机遇得分 | 政策环境机遇评分 | policy_score | chain_sz_opportunity(chain_id, policy_score) — 政策分 | 无 |
|  | 市场机遇 | 市场机遇得分 | 市场空间机遇评分 | market_score | chain_sz_opportunity(chain_id, market_score) — 市场分 | 无 |

## 源表字段

- chain_sz_opportunity(chain_id, chain_name, cycle_stage, growth_rate, trend_score, policy_score, market_score, opportunity_index, advantages, weaknesses, suggestions, rank_overall) — 深圳机遇综合分（gkxlumenx_ads / demo_gkxlumenx_ads）
- chain_sz_advantage(chain_id, chain_name, advantage_index, growth_rate) — 深圳优势（机遇输入）
- chain_sz_problem(chain_id, chain_name, problems, causes) — 深圳问题（机遇输入）

## 待建字段

- 三维权重（待甲方确认；seed 公式为「产业缺口×w1+深圳匹配度×w2+政策机遇×w3」，与 ads 三维 trend/policy/market 需对齐）
- 机遇评分公式与 opportunity_index 口径一致性确认

## 参考资料

[1] 深圳机遇分析模型｜科技专题服务算法库 1.1.1.1.1.1.1.3.12（机遇预测与推荐、综合评估）。

[2] 区域产业机遇评估｜深圳市人民政府｜深圳产业发展规划（趋势/政策/市场三维机遇评估）。
