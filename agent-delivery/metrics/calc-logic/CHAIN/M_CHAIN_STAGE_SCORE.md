# 产业阶段评分（M_CHAIN_STAGE_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_STAGE_SCORE |
| 指标名称 | 产业阶段评分 |
| 一级模块 | 产业链分析 |
| 二级模块 | 产业周期分析 |
| 三级模块 | 周期阶段判定 |
| 更新频率 | 年 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q053+QC03 |


## 口径定义

指定产业链在统计年度的产业阶段综合评分，从生产能力、销售规模、市场份额、利润率维度评定，取值 0—100。分数越高越偏向扩张/成长，越低越偏向收缩/衰退。

## 计算逻辑说明

从 `dwd_industry_chain_info` 取全部 `industry_code` 为对比截面。各链经 `dwd_org_industry_tags` 取企业，`credit_code` 关联 `dwd_org_annual_financial_info.external_id`，按 `year` 取年报。同一企业挂多条链时，人数、营收、利润全额分别计入各链，不做拆分。

四维等权。先算各链各维原始值，再在同一统计年对全部产业链做截面 min-max 到 [0,1]，算术平均后乘 100。某维全部链取值相同，或某链该维缺失，则该维得分取 0.5。

可比集合：相邻两年同一字段都有效的同一批 `credit_code`。不可比企业不进同比。

1.生产能力（从业人数可比同比）

两年 `employees_number` 均 \(>0\) 的企业集合$ C^{emp}_t$：
$$
g^{emp}_t = \frac{\sum_{i\in C^{emp}_t} employees\_number_{i,t}}{\sum_{i\in C^{emp}_t} employees\_number_{i,t-1}} - 1
$$
集合为空或分母为 0 则该维缺失。库无实物产量，只用从业人数增速代理生产能力扩张，不用人数合计。

2.销售规模（营收可比同比）

两年 `operating_revenue` 均 \(>0\) 的企业集合$ C^{rev}_t$：
$$
g^{rev}_t = \frac{\sum_{i\in C^{rev}_t} operating\_revenue_{i,t}}{\sum_{i\in C^{rev}_t} operating\_revenue_{i,t-1}} - 1
$$
集合为空或分母为 0 则该维缺失。

3.市场份额（链间份额变化）

当年有效营收合计$ S_{c,t}=\sum operating\_revenue$（营收 \(>0\)）。全部建模链 \(C\)：
$$
share_{c,t} = \frac{S_{c,t}}{\sum_{c'\in C} S_{c',t}}
$$
$$
\Delta share_{c,t} = share_{c,t} - share_{c,t-1}
$$
分母为 0 或缺上年份额则该维缺失。这是本链在建模产业链营收合计中的权重变化，不是互斥产品市场占有率；多链挂接会使 \(\sum S\) 重复计数，但份额之和仍为 1。不用当年份额水平（那会回到“链越大分越高”）。

4.利润率

统计年有效营收企业：`total_profit` 空值按 0。
$$
m_t = \frac{\sum total\_profit}{\sum operating\_revenue}
$$
分母为 0 则该维缺失。

合成：
$$
产业阶段评分_c = 100 \times \frac{1}{4}\sum_{j=1}^{4} z_{c,j}
$$
$z_{c,j} $为该维 min-max 得分。四维都缺失则本指标不输出。

| 一级指标 | 二级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- |
| 产业阶段评分 | 生产能力 | 可比从业人数同比 | dwd_org_annual_financial_info(employees_number, year) | 无 |
| | 销售规模 | 可比营业收入同比 | dwd_org_annual_financial_info(operating_revenue, year) | 无 |
| | 市场份额 | 本链营收占全部建模链合计的份额较上年增减 | dwd_org_annual_financial_info(operating_revenue, year) | 无 |
| | 利润率 | 统计年利润总额合计 / 营业收入合计 | dwd_org_annual_financial_info(total_profit, operating_revenue, year) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 截面全部产业链
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联
- dwd_org_annual_financial_info(external_id, year, employees_number, operating_revenue, total_profit) — 信用代码关联, 年报年度, 从业人数, 营业收入, 利润总额

## 待建字段

- 无

## 参考文献

- 产业阶段评分｜东南大学经济管理学院｜国家自然科学基金项目（71173116）；教育部哲学社会科学发展报告项目（13JBG004）｜季良玉, 李廉水. 中国制造业产业生命周期研究——基于1993—2014年数据的分析[J]. 河海大学学报(哲学社会科学版), 2016, 18(1): 30-37. DOI: 10.3876/j.issn.1671-4970.2016.01.007.
