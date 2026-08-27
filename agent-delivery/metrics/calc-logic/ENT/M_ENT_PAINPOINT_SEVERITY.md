# 痛难点严重度（M_ENT_PAINPOINT_SEVERITY）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_PAINPOINT_SEVERITY |
| 指标名称 | 痛难点严重度 |
| 一级模块 | 企业分析 |
| 二级模块 | 风险洞察 |
| 三级模块 | 发展痛难点 |
| 更新频率 | 月度/季度 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q014 |


## 口径定义

企业发展痛难点严重度指企业各项经营指标实际表现与判断阈值之间的偏离程度。依照需求文档提供的构建方法。

## 计算逻辑说明

计算各指标与阈值偏离度，分维度（经营竞争力/盈利能力/生产效率/人才状况）加权汇总，按偏离度分档（轻度0-20%/中度20-50%/重度>50%）。

## 源表字段

 gkx.dwd_org_annual_financial_info(org_id, operating_revenue, total_profit, pure_profit, total_assets, total_liabilities, `arch development am`, development_employee, employees_number, year) — 营收排名、增长率、净资产收益率、成本费用利润率、人均营收、研发人员数量及占比
 gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标与细分行业归属
 企业痛难点阈值配置表(各维度判断阈值) — 痛难点识别阈值配置（现库无此表，待建）

## 待建字段

企业痛难点阈值配置表(各维度判断阈值) — 痛难点识别阈值配置（现库无此表，待建）
