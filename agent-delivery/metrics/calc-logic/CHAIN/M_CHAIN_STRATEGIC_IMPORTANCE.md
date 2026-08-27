# 战略重要性（M_CHAIN_STRATEGIC_IMPORTANCE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_STRATEGIC_IMPORTANCE |
| 指标名称 | 战略重要性 |
| 一级模块 | 产业链分析 |
| 二级模块 | 产业关键环节识别 |
| 三级模块 | 战略重要性 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q052+QC02 |


## 口径定义

指特定产业链环节在维持产业体系自主可控及提升整体竞争力方面所具有的关键程度。。

## 计算逻辑说明

第一步：各指标标准化

各指标原始数据通过极值归一化法消除量纲，转换为 0—100 之间的标准化得分：
$$
指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij} 为第 i 个评估对象在第 j 个指标上的原始值，\min(x_j) 和 \max(x_j) 分别为该指标在所有评估对象中的最小值和最大值。
$$

第二步：战略重要性综合得分

将三个指标标准化得分加权汇总（可采用等权重，各占 1/3；也可根据评估重点自行制定各指标权重）：
$$
战略重要性得分 = W_1 \times 产值比重得分 + W_2 \times 研发人员占比率得分 + W_3 \times 销售利润率得分
$$

$$
其中，W_1、W_2、W_3 为各指标权重，可采用等权重（各占 1/3），也可根据评估重点自行制定，\sum W = 1。得分越高表明该环节的战略重要性越强。
$$

| 维度             | 指标           | 指标含义                                                     | 源表字段 | 待建字段 |
| :--------------- | :------------- | :----------------------------------------------------------- | -------- | -------- |
| **产业链位置**   | 某环节产值比重 | 该环节产值占产业链总产值的比重，反映其在产业链中的经济规模与影响力 | dwd_org_annual_financial_info(operating_revenue) | 无 |
| **技术创新能力** | 研发人员占比率 | 研发人员占从业人员总数的比重，反映该环节的技术创新投入水平   | dwd_org_annual_financial_info(development_employee, employees_number) | 无 |
| **经济效益**     | 销售利润率     | 利润总额 ÷ 销售收入 × 100%，反映该环节的盈利能力和价值创造能力 | dwd_org_annual_financial_info(total_profit, operating_revenue) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 目标产业链范围, 产业链名称, 环节去重, 环节名称
- dwd_org_industry_tags(industry_code, industry_link_code, credit_code, company_name) — 链上企业筛选, 环节关联, 信用代码关联, 企业名称匹配
- dwd_org_annual_financial_info(external_id, year, operating_revenue, total_profit, employees_number, development_employee) — 企业信用代码关联, 年报年度, 营业收入, 利润总额, 从业人数, 研发人员数量

## 待建字段

- 无

## 参考文献

**战略重要性**｜东北大学工商管理学院｜国家自然科学基金资助项目（71771045）；东北大学“双一流”学科建设资助项目（02050021940101）｜郭伏，李明明，任增根，等. 产业集群中产业链的关键环节识别方法研究[J]. 辽宁工业大学学报（社会科学版）， 2019, 21(3): 34-38. DOI: 10.15916/j.issn1674-327x.2019.03.009.
