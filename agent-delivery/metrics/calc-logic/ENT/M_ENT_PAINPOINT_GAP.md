# 痛难点改进差距（M_ENT_PAINPOINT_GAP）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_PAINPOINT_GAP |
| 指标名称 | 痛难点改进差距 |
| 一级模块 | 企业分析 |
| 二级模块 | 风险洞察 |
| 三级模块 | - |
| 更新频率 | 月度/季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q009 / Q018 |

## 口径定义

沿用企业诊断 A3 的产业链分组与 P25/P75 基线，计算企业各项经营指标值与同产业链分组基线的原始差值，展示改进差距，不设硬阈值。对象=企业相对其产业链分组的偏离程度，粒度=企业。基线口径 Q018 临时默认闭合（2026-08-11）。

## 计算逻辑说明

按痛难点识别模型 §.5.3 四维（经营竞争力/盈利能力/生产效率/人才状况）计算企业值与分组 P25/P75 的差值。

### 第一步：分组基线

产业链分组以 `industry_l1_code` 或 `dwd_org_industry_tags.industry_code` 分组；组内计算各指标 P25/P75 分位数作基线。

### 第二步：差值

$$ Gap_k = x_k - Baseline_k(P25 / P75) $$

- 低于 P25：处于组内劣势（负差距）；
- 高于 P75：处于组内优势（正差距）；
- 不设硬阈值，输出原始差值。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 痛难点改进差距 | 经营竞争力差距 | 营业收入增长率 vs 分组基线 | 企业营收增长率与分组 P25/P75 差值。 | x_营收增长率 − Baseline | enterprise_finance_history(org_id, data_year, revenue_growth_rate) — 营收增长率；dwd_org_annual_financial_info(org_id, year, operating_revenue) — 营收 | 分组 P25/P75 基线配置表 |
|  |  | 主营业务收入 vs 分组基线 | 企业主营业务收入与分组基线差值。 | x_主营收入 − Baseline | dwd_org_annual_financial_info(org_id, year, main_business_revenue) — 主营业务收入 | 分组 P25/P75 基线配置表 |
| 痛难点改进差距 | 盈利能力差距 | 净利润率 vs 分组基线 | 企业净利润率与分组 P25/P75 差值。 | x_净利润率 − Baseline | enterprise_finance_history(org_id, data_year, profit_margin, net_profit) — 净利润率；dwd_org_annual_financial_info(org_id, year, pure_profit) — 净利润 | 分组 P25/P75 基线配置表 |
|  |  | 净资产收益率 vs 分组基线 | 企业 ROE 与分组基线差值。 | x_ROE − Baseline | dwd_org_annual_financial_info(org_id, year, pure_profit, owners_equity) — 净利润,所有者权益 | 分组 P25/P75 基线配置表 |
| 痛难点改进差距 | 生产效率差距 | 人均产值 vs 分组基线 | 企业人均营收与分组 P25/P75 差值。 | x_人均营收 − Baseline | dwd_org_annual_financial_info(org_id, year, operating_revenue, employees_number) — 营收,从业人数 | 分组 P25/P75 基线配置表 |
| 痛难点改进差距 | 人才状况差距 | 研发人员占比 vs 分组基线 | 企业研发人员占比与分组 P25/P75 差值。 | x_研发占比 − Baseline | dwd_org_annual_financial_info(org_id, year, development_employee, employees_number) — 研发人员,从业人数 | 分组 P25/P75 基线配置表 |

## 源表字段

- dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue, pure_profit, owners_equity, employees_number, development_employee) — 经营/盈利/效率/人才指标
- enterprise_finance_history(org_id, data_year, revenue_growth_rate, profit_margin, net_profit) — 增长率/利润率（DWD）
- dwd_org_base_info(org_id, industry_l1_code) — 产业链分组（行业归属）
- dwd_org_industry_tags(credit_code, industry_code) — 产业链分组

## 待建字段

- 分组 P25/P75 基线配置表：现库无「产业链分组 × 指标 × P25/P75」基线表，需按组内分位数在线计算或落配置表。
- 分组口径（产业链 vs 行业）待 Q018 正式闭合。

## 参考资料

[1] 企业发展痛难点识别模型 | 算法库 §1.1.1.1.1.1.1.5.3 | 需求ID ALGO-ENT-DEEP-143 | 经营/盈利/效率/人才四维 | 关联 Q009 / Q018。

[2] 痛难点严重度 | 王惠已入库指标 M_ENT_PAINPOINT_SEVERITY（四维加权偏离口径对齐，本条为差值版）。
