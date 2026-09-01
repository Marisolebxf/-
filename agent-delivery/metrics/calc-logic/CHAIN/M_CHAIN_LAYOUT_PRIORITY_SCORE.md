# 布局优先级评分（M_CHAIN_LAYOUT_PRIORITY_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_LAYOUT_PRIORITY_SCORE |
| 指标名称 | 布局优先级评分 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | 优先级评分 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q059+QC09 |


## 口径定义

指基于深圳产业数据与全国产业数据对比分析，从产业增长和产业竞争力两个维度，对深圳各产业的布局优先程度进行综合量化评估的得分。

## 计算逻辑说明

第一步：各指标标准化

各指标原始数据通过极值归一化法消除量纲，转换为 0—100 之间的标准化得分：
$$
指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij} 为产业 i 在第 j 个指标上的原始值，\min(x_j) 和 \max(x_j) 分别为该指标在所有产业中的最小值和最大值。
$$

第二步：各维度得分计算

产业增长维度得分 =（行业增长率得分 + 市场占有率得分）÷ 2（等权重各 50%）

产业竞争力维度得分 =（技术创新能力得分 + 产业规模得分）÷ 2（等权重各 50%）

第三步：布局优先级评分综合得分

将两个维度得分加权汇总（可采用等权重，各维度权重 = 1/2；也可根据评估重点自行制定各维度权重）：
$$
布局优先级评分 = W_1 \times 产业增长维度得分 + W_2 \times 产业竞争力维度得分
$$
其中，$W_1$、$W_2$ 为各维度权重，可采用等权重（各占 50%），也可根据评估重点自行制定，$\sum W = 1$。最终得分越高，表明该产业在深圳的竞争优势越明显，越应优先布局。

| 维度           | 指标         | 指标说明                           | 测度方式                                 | 源表字段 | 待建字段 |
| :------------- | :----------- | :--------------------------------- | :--------------------------------------- | -------- | -------- |
| **产业增长**   | 行业增长率   | 产业产值增速                       | （本期产值 − 上期产值）÷ 上期产值 × 100% | dwd_org_annual_financial_info(operating_revenue, year) | 无 |
|                | 市场占有率   | 深圳产业产值占全国该产业产值的比重 | 深圳该产业产值 ÷ 全国该产业产值 × 100%   | dwd_org_annual_financial_info(operating_revenue, year); dwd_org_base_info(city) | 无 |
| **产业竞争力** | 技术创新能力 | 研发投入强度                       | 研发经费支出 ÷ 产业产值 × 100%           | dwd_org_stock_finance_info(research_development_amount); dwd_org_annual_financial_info(operating_revenue) | 无 |
|                | 产业规模     | 深圳该产业年度总产值               | 直接取自经济指标库                       | dwd_org_annual_financial_info(operating_revenue, year); dwd_org_base_info(city) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配
- dwd_org_base_info(external_id, city) — 企业信用代码关联, 城市筛选
- dwd_org_annual_financial_info(external_id, year, operating_revenue) — 企业信用代码关联, 年报年度, 营业收入
- dwd_org_stock_finance_info(external_id, occur_period, operating_revenue, research_development_amount) — 上市企业信用代码关联, 数据期, 营业收入, 研发投入金额

## 待建字段

- 无
