# 综合竞争力分（M_ENT_COMPETITIVENESS_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_COMPETITIVENESS_SCORE |
| 指标名称 | 综合竞争力分 |
| 一级模块 | 企业分析 |
| 二级模块 | 企业评估 |
| 三级模块 | 综合竞争力评估 |
| 更新频率 | 年度/模型版本发布时 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q014 |


## 口径定义

企业综合竞争力评估的综合得分，满分0-100分，综合反映企业在企业规模、财务状况、人力资源、市场表现四个维度的综合水平。

## 计算逻辑说明

第一步：数据标准化处理

各指标原始数据通过极值归一化法消除量纲，将每个指标的实际值转换为0—100之间的标准化得分：
$$
正向指标：指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
负向指标：指标得分_{ij} = \frac{\max(x_j) - x_{ij}}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij} 为企业 i 在第 j个指标上的原始值，\min(x_j) 和 \max(x_j)分别为该指标在所有企业中的最小值和最大值。
$$

第二步：计算各维度得分

将各二级指标下的三级指标标准化得分，按照对应的指标分值进行加权汇总，得到企业规模、财务状况、人力资源、市场表现四个维度的综合得分：
$$
维度得分_i = \sum_{j=1}^{n} w_j \times 指标得分_{ij}
$$

$$
其中，w_j 为第 j 个三级指标的权重（指标分值/100），n为该维度下三级指标的总数。
$$

第三步：计算综合竞争力得分

将五个维度的得分与一级指标权重加权汇总，得到企业综合竞争力最终得分：
$$
综合竞争力得分 = \sum_{k=1}^{4} W_k \times 维度得分_{ik}
$$
其中，W_k 为第 k个一级指标的权重（需要确定权重或者使用熵值法），i为企业编号。最终得分越高，表明企业综合竞争力越强。

### 企业综合竞争力评价指标体系

| 一级维度     | 三级指标               | 指标说明                                   | 源表字段 |
| :----------- | :--------------------- | :----------------------------------------- | -------- |
| **企业规模** | 资产总额        | 企业期末资产总额                           | gkx.dwd_org_annual_financial_info(org_id, total_assets, year) — 期末资产总额 |
|              | 从业人员数             | 企业期末员工总数                           | gkx.dwd_org_annual_financial_info(org_id, employees_number, year) — 期末员工总数 |
| **财务状况** | 营业收入利润率         | 利润总额 ÷ 营业收入 × 100%                 | gkx.dwd_org_annual_financial_info(org_id, total_profit, operating_revenue, year) — 营业收入利润率=利润总额÷营业收入×100% |
|              | 资产负债率             | 负债总额 ÷ 资产总额 × 100%                 | gkx.dwd_org_annual_financial_info(org_id, total_liabilities, total_assets, year) — 资产负债率=负债总额÷资产总额×100% |
|              | 总资产周转率           | 营业收入 ÷ 平均资产总额 × 100%             | gkx.dwd_org_annual_financial_info(org_id, operating_revenue, total_assets, year) — 总资产周转率=营业收入÷平均资产总额×100% |
| **人力资源** | 本科及以上学历员工占比 | 本科及以上学历人数 ÷ 员工总数 × 100%       | gkx.dwd_org_annual_financial_info(org_id, employees_number, year) — 员工总数（分母）<br>gkx 现库无学历结构字段（待建）— 本科及以上学历人数 |
|              | 研发人员占比     | 研发人员人数 ÷ 员工总数 × 100%        | gkx.dwd_org_annual_financial_info(org_id, development_employee, employees_number, year) — 研发人员占比=研发人员数÷员工总数×100% |
| **市场表现** | 市场占有率             | 企业产品销售量 ÷ 市场同类产品销售量 × 100% | gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 企业营业收入<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业归属，需行业营收汇总 |
|              | 销售收入               | 与所有者投入资本无关的经济利益总流入       | gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 营业收入 |

## 源表字段

gkx.dwd_org_annual_financial_info(org_id, operating_revenue, total_profit, total_assets, total_liabilities, development_employee, employees_number, year) — 企业规模（资产总额、从业人员数）、财务状况（营业收入利润率、资产负债率、总资产周转率）、人力资源（研发人员占比）、市场表现（市场占有率、销售收入），优先年报，覆盖非上市企业
gkx.dwd_org_base_info(org_id, industry_l1_code) — 市场占有率维度的行业归属与行业营收汇总
本科及以上学历人数字段 — 现库无学历结构字段，待建
目标结果表 ads_ent_competitiveness_score(score, peer_group, batch_id, 待建) — 综合竞争力得分

## 待建字段

本科及以上学历人数字段 — 现库无学历结构字段，待建
目标结果表 ads_ent_competitiveness_score(score, peer_group, batch_id, 待建) — 综合竞争力得分
