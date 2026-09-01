# 成长潜力（M_ENT_GROWTH_POTENTIAL）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_GROWTH_POTENTIAL |
| 指标名称 | 成长潜力 |
| 一级模块 | 企业分析 |
| 二级模块 | 引育推荐 |
| 三级模块 | 招引推荐 |
| 更新频率 | 年度/季度 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 是 |
| 关联Q编号 | Q015 |


## 口径定义

指企业未来持续发展和规模扩张的潜力，反映企业内生增长动能和可持续发展能力。

## 计算逻辑说明

参考工信部《中小企业专精特新发展评价指标体系》中“成长性”指标的定义，从市场扩张能力**、**盈利提升能力和资产积累能力三个维度综合衡量。各维度与行业均值进行比较，数据取自企业最近两个完整自然年度。三个维度采用等权重加权汇总，得出成长潜力综合得分。

### 成长性指标

| 维度       | 二级指标 | 计算方式                                                 | 源表字段                                                     |
| :--------- | :------- | :------------------------------------------------------- | ------------------------------------------------------------ |
| **成长性** | 市场扩张 | 营业收入增长率超出行业均值情况                           | gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 营收同比计算<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标 |
|            | 盈利提升 | 利润增长率超出行业均值情况                               | gkx.dwd_org_annual_financial_info(org_id, total_profit, year) — 利润同比计算<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标 |
|            | 资产积累 | 净资产增长率超出行业均值情况（净资产=资产总额-负债总额） | gkx.dwd_org_annual_financial_info(org_id, total_assets, total_liabilities, year) — 净资产同比计算（净资产=资产总额-负债总额）<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标 |

## 源表字段

gkx.dwd_org_annual_financial_info(org_id, operating_revenue, total_profit, total_assets, total_liabilities, year) — 营收/利润/净资产同比计算（净资产=资产总额-负债总额）
gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标
