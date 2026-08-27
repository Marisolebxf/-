# 痛难点反映企业数（M_ENT_PAINPOINT_COUNT）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_PAINPOINT_COUNT |
| 指标名称 | 痛难点反映企业数 |
| 一级模块 | 企业分析 |
| 二级模块 | 风险洞察 |
| 三级模块 | 发展痛难点 |
| 更新频率 | 月度/季度 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q014 |


## 口径定义

指在特定统计周期内，通过企业发展痛难点识别模型，基于企业经营数据与判断阈值的比对分析，识别出存在至少一个维度痛难点问题的企业数量。

## 计算逻辑说明

通过企业发展痛难点识别模型算法，从经营竞争力、盈利能力、生产效率、人才状况四个维度对目标企业集合内的各企业进行逐项指标与判断阈值的比对分析，将任一维度指标实际值低于判定阈值的企业识别为“存在痛难点”，统计该部分企业的去重数量。

### 痛难点识别维度指标体系

| 维度           | 三级指标             | 指标说明                                                     | 源表字段 |
| :------------- | :------------------- | :----------------------------------------------------------- | -------- |
| **经营竞争力** | 细分行业营业收入排名 | 反映企业在细分市场中的竞争地位，排名越靠后表明市场竞争力越弱(近三年) | gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 近三年营收排名<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 细分行业归属 |
|                | 营业收入增长率       | 反映企业市场扩张能力，增长率低于行业均值表明市场拓展存在困难(近两年) | gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 营收同比计算<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标 |
| **盈利能力**   | 净资产收益率         | 反映资产利用效率，低于行业均值表明盈利能力不足               | gkx.dwd_org_annual_financial_info(org_id, pure_profit, total_assets, total_liabilities, year) — 净利润与平均净资产（净资产=资产总额-负债总额）<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标 |
|                | 成本费用利润率       | 反映投入产出效率，低于行业均值表明成本控制存在短板           | gkx.dwd_org_annual_financial_info(org_id, total_profit, year) — 利润总额<br>现库无成本费用总额字段（待建）— 成本费用利润率=利润总额÷成本费用总额×100% |
| **生产效率**   | 人均营业收入         | 反映劳动产出效率，低于行业均值表明生产效率存在短板           | gkx.dwd_org_annual_financial_info(org_id, operating_revenue, employees_number, year) — 人均营业收入<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标 |
| **人才状况**   | 研发人员数量及占比   | 反映研发人才储备不足，低于行业或认定标准表明人才状况存在短板 | gkx.dwd_org_annual_financial_info(org_id, development_employee, employees_number, year) — 研发人员数量与占比（占比=研发人员数÷从业人数）<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标 |

## 源表字段

gkx.dwd_org_annual_financial_info(org_id, operating_revenue, total_profit, pure_profit, total_assets, total_liabilities, `arch development am`, development_employee, employees_number, year) — 营收排名、增长率、净资产收益率、人均营收、研发人员数量及占比（优先年报，覆盖非上市企业）
gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标与细分行业归属
企业痛难点阈值配置表(各维度判断阈值) — 痛难点识别阈值配置（现库无此表，待建）

注：从经营竞争力、盈利能力、生产效率、人才状况四个维度，将各指标实际值与判断阈值比对，低于阈值的企业计为存在痛难点。

## 待建字段

企业痛难点阈值配置表(各维度判断阈值) — 痛难点识别阈值配置（现库无此表，待建）
