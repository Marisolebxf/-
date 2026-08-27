# 产业阶段判定（M_CHAIN_PHASE_DETERMINATION）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_PHASE_DETERMINATION |
| 指标名称 | 产业阶段判定 |
| 一级模块 | 产业链分析 |
| 二级模块 | 产业周期分析 |
| 三级模块 | 周期阶段判定 |
| 更新频率 | 年 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q053+QC03 |


## 口径定义

指定产业链在统计年度所处的产业发展阶段。先取 `M_CHAIN_STAGE_SCORE`，再按当年全部产业链得分分三档，输出成长期、成熟期、衰退期之一。与 `M_CHAIN_CYCLE_STAGE` 不是同一套算法。无得分的链不参与分档。

## 计算逻辑说明

先按 `M_CHAIN_STAGE_SCORE` 算出各链分数（增速、份额变化、利润率四维，国内年报，不含海外）。再把当年有得分的产业链按分数从高到低分三档：前 1/3 为成长期，后 1/3 为衰退期，其余为成熟期。链数不能被 3 整除时，高档与低档向下取整，剩余归中档。

底层字段与评分指标相同，不另建算法。

| 一级指标 | 二级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- |
| 产业阶段判定 | 成长期 | 当年 STAGE_SCORE 位于有得分产业链前 1/3 | 见 M_CHAIN_STAGE_SCORE | 无 |
| | 成熟期 | 当年 STAGE_SCORE 位于中间档 | 见 M_CHAIN_STAGE_SCORE | 无 |
| | 衰退期 | 当年 STAGE_SCORE 位于有得分产业链后 1/3 | 见 M_CHAIN_STAGE_SCORE | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 截面全部产业链
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联
- dwd_org_annual_financial_info(external_id, year, employees_number, operating_revenue, total_profit) — 信用代码关联, 年报年度, 从业人数, 营业收入, 利润总额

## 待建字段

- 无

## 参考文献

口径见 M_CHAIN_STAGE_SCORE。

- 产业阶段判定｜南京大学商学院｜范从来, 袁静. 成长性、成熟性和衰退性产业上市公司并购绩效的实证分析[J]. 中国工业经济, 2002(8): 65-72.
- 产业阶段判定｜东南大学经济管理学院｜国家自然科学基金项目（71173116）；教育部哲学社会科学发展报告项目（13JBG004）｜季良玉, 李廉水. 中国制造业产业生命周期研究——基于1993—2014年数据的分析[J]. 河海大学学报(哲学社会科学版), 2016, 18(1): 30-37. DOI: 10.3876/j.issn.1671-4970.2016.01.007.
