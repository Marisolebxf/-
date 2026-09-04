# 投融资总额（M_CHAIN_INVEST_TOTAL）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_INVEST_TOTAL |
| 指标名称 | 投融资总额 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | QC07 |

## 口径定义

指定产业链在统计窗内相关投融资事件的总金额（单位：万元），按融资事件金额合计，并可派生环比增长率。对象=产业链投融资资金规模。口径对应 QC07，待甲方冻结。

## 计算逻辑说明

算法库「产业链基础指标模型构建 · （4）产业投融资规模」（约 61–67 行）要求「根据提取的投融资金额等指标，综合计算该产业链的投融资规模指标，并通过环比计算增长率」。以 `chain_investment` 为真源聚合金额。

### 计算步骤

1. 按 `chain_id` 定链，取 `chain_investment`（dwd 明细：`investment_id`/`amount`；ads 汇总：`total_amount`）。
2. 融资事件金额合计：`SUM(amount)`（dwd 明细）或直接取 ads `total_amount`。
3. 环比增长率：`(本期金额 − 上期金额) / 上期金额 × 100%`。

$$
投融资总额 = \sum 融资事件金额（万元）
$$
$$
投融资增长率 = \frac{本期投融资总额 − 上期投融资总额}{上期投融资总额} \times 100\%
$$

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 投融资总额 | 融资总额 | 融资事件金额合计 | 链上融资事件金额合计（万元） | SUM(amount) | chain_investment(investment_id, chain_id, enterprise_id, round, amount, invest_date) — 融资明细；chain_investment(chain_id, stat_year, investment_count, total_amount) — 融资汇总 | 无 |
|  | 投融资增长率 | 金额环比增长率 | 本期较上期投融资金额环比增速 | (本期-上期)/上期×100% | chain_investment(chain_id, stat_year, total_amount, amount_growth_rate) — 已有增长率 | 无 |

## 源表字段

- chain_investment(investment_id, chain_id, chain_name, enterprise_id, enterprise_name, round, amount, investor, invest_date, data_year) — 投融资明细（gkxlumenx_dwd / demo_gkxlumenx_dwd）
- chain_investment(chain_id, chain_name, stat_year, investment_count, total_amount, amount_growth_rate, count_growth_rate) — 投融资汇总（gkxlumenx_ads / demo_gkxlumenx_ads）
- industry_chain_investment_event(event_id, chain_id, node_id, investment_type, financing_round, amount, currency, event_date) — 投融资事件（demo_gkxlumenx_dwd，含币种/轮次）
- dwd_org_invest_info(org_id, name_cn, inv_name, investment_amount, investment_ratio) — 企业投资明细

## 待建字段

- 币种统一字段（`industry_chain_investment_event.currency` 与 `chain_investment.amount` 口径需对齐为万元）
- 区域级投融资映射字段（QC07 待甲方确认）

## 参考资料

[1] 产业链基础指标模型构建 · 产业投融资规模｜科技专题服务算法库 1.2.1.1.1.1.4.1.1（4）（投融资总额、环比增长率）。

[2] 产业投融资统计｜清科/投中产业投融资数据口径（融资事件金额合计，单位万元）。
