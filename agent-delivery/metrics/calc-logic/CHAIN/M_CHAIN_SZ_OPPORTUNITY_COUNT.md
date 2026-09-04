# 深圳产业机遇数（M_CHAIN_SZ_OPPORTUNITY_COUNT）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SZ_OPPORTUNITY_COUNT |
| 指标名称 | 深圳产业机遇数 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 周 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

深圳在指定产业链上可把握的机遇清单去重数，按产业发展方向机遇、政策优化机遇、创新方向机遇三类归类。对象=深圳产业机遇清单，不是普通建议条目。机遇识别口径与阈值待甲方确认。

## 计算逻辑说明

算法库「深圳机遇分析模型」（1.1.1.1.1.1.1.3.12，约 564–575 行）输出「区域机遇推荐清单、产业发展建议报告、政策优化方案、创新方向分析图表」。据此将机遇按三类归类去重计数。

### 计算步骤

1. 按 `chain_id` 定链，取 `chain_sz_opportunity`（ads）记录。
2. 从 `advantages`/`weaknesses`/`suggestions` 文本中结构化抽取机遇条目。
3. 按三类（产业发展方向 / 政策优化 / 创新方向）去重计数汇总。

$$
深圳产业机遇数 = \sum_{类型} COUNT(DISTINCT 机遇条目 \mid 机遇类型)
$$

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 深圳产业机遇数 | 产业发展方向 | 产业发展方向机遇数 | 产业发展方向类机遇去重数 | COUNT(DISTINCT 机遇 WHERE 类型=产业发展方向) | chain_sz_opportunity(chain_id, advantages, suggestions) — 机遇清单文本 | 机遇结构化条目字段 |
|  | 政策优化 | 政策优化机遇数 | 政策优化类机遇去重数 | COUNT(DISTINCT 机遇 WHERE 类型=政策优化) | chain_sz_opportunity(chain_id, suggestions) — 政策建议文本 | 机遇结构化条目字段 |
|  | 创新方向 | 创新方向机遇数 | 创新重点方向类机遇去重数 | COUNT(DISTINCT 机遇 WHERE 类型=创新方向) | chain_sz_opportunity(chain_id, suggestions) — 创新方向文本 | 机遇结构化条目字段 |

## 源表字段

- chain_sz_opportunity(chain_id, chain_name, cycle_stage, growth_rate, trend_score, policy_score, market_score, opportunity_index, advantages, weaknesses, suggestions, rank_overall) — 深圳机遇结果（gkxlumenx_ads / demo_gkxlumenx_ads）
- chain_sz_advantage(chain_id, chain_name, advantage_index, advantages, weaknesses, suggestions) — 深圳优势（机遇输入）
- chain_sz_problem(chain_id, chain_name, problems, causes, suggestions) — 深圳问题（机遇输入）

## 待建字段

- 机遇清单结构化条目字段（现机遇以 `suggestions`/`advantages` 文本存，需结构化抽取）
- 机遇类型三分类枚举（产业发展方向/政策优化/创新方向）
- 机遇识别口径与阈值（待甲方确认）

## 参考资料

[1] 深圳机遇分析模型｜科技专题服务算法库 1.1.1.1.1.1.1.3.12（区域机遇推荐清单、产业发展建议、政策优化方案、创新方向）。

[2] 区域产业机遇识别｜深圳市人民政府｜深圳产业发展规划（产业发展方向/政策优化/创新方向三维机遇）。
