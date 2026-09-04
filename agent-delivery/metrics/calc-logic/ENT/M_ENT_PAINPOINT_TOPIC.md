# 发展痛难点诊断（M_ENT_PAINPOINT_TOPIC）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_PAINPOINT_TOPIC |
| 指标名称 | 发展痛难点诊断 |
| 一级模块 | 企业分析 |
| 二级模块 | 风险洞察 |
| 三级模块 | - |
| 更新频率 | 月度/季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q009 / Q018 / Q080 |

## 口径定义

输出企业发展痛难点的问题/瓶颈清单及建议报告（描述、成因、行业最佳实践、解决方案）。诊断维度按 §.5.3 经营/盈利/效率/人才四维（Q-MO-ENT-09），不复用 Q018 四维的 `M_ENT_PAINPOINT_COUNT`。对象=企业诊断报告，粒度=企业。

## 计算逻辑说明

四维诊断：各维指标与分组基线比较，识别偏离方向，输出问题清单 + 建议。

### 第一步：四维判定

1. **经营竞争力**：营收增长率低于分组 P25 判定经营竞争力不足。
2. **盈利能力**：净利润率/ROE 低于分组 P25 判定盈利短板。
3. **生产效率**：人均产值低于分组 P25 判定生产效率低。
4. **人才状况**：研发人员占比低于分组 P25 或人才流失判定人才短板。

### 第二步：报告生成

$$ Report = \{ 问题描述, 成因分析, 行业最佳实践, 解决方案 \} $$

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 发展痛难点诊断 | 经营竞争力诊断 | 营收增长异常识别 | 营收增长率低于分组基线判定。 | revenue_growth_rate < P25 | enterprise_finance_history(org_id, data_year, revenue_growth_rate) — 营收增长率 | 诊断阈值/规则配置表 |
| 发展痛难点诊断 | 盈利能力诊断 | 净利润率异常识别 | 净利润率低于分组基线判定。 | profit_margin < P25 | enterprise_finance_history(org_id, data_year, profit_margin, net_profit) — 净利润率 | 诊断阈值/规则配置表 |
| 发展痛难点诊断 | 生产效率诊断 | 人均产值异常识别 | 人均营收低于分组基线判定。 | 营收/从业人数 < P25 | dwd_org_annual_financial_info(org_id, year, operating_revenue, employees_number) — 营收,从业人数 | 诊断阈值/规则配置表 |
| 发展痛难点诊断 | 人才状况诊断 | 研发人员占比异常识别 | 研发人员占比低于分组基线判定。 | 研发/从业人数 < P25 | dwd_org_annual_financial_info(org_id, year, development_employee, employees_number) — 研发人员,从业人数 | 诊断阈值/规则配置表 |
| 发展痛难点诊断 | 诊断结果 | 问题清单与建议报告 | 描述/成因/实践/方案报告输出。 | 四维汇总 | enterprise_diagnosis(org_id, enterprise_name, weaknesses, suggestions, diag_level) — 诊断结果（ADS） | 无 |

## 源表字段

- dwd_org_annual_financial_info(org_id, year, operating_revenue, pure_profit, employees_number, development_employee) — 经营/盈利/效率/人才指标
- enterprise_finance_history(org_id, data_year, revenue_growth_rate, profit_margin, net_profit) — 增长率/利润率（DWD）
- dwd_org_base_info(org_id, industry_l1_code) — 产业链分组
- dwd_org_industry_tags(credit_code, industry_code) — 产业链分组
- enterprise_diagnosis(org_id, enterprise_name, weaknesses, suggestions, diag_level) — 诊断结果（ADS）

## 待建字段

- 诊断阈值/规则配置表：四维判定阈值与分组基线现无配置，需按组内分位数或专家阈值落表。
- 行业最佳实践/解决方案知识库：建议报告生成所需实践库现无表。

## 参考资料

[1] 企业发展痛难点识别模型 | 算法库 §1.1.1.1.1.1.1.5.3 | 经营/盈利/效率/人才四维 | 关联 Q009 / Q018 / Q080。

[2] 智能痛难点诊断模型/分析建议报告输出 | 需规 SRS《企业分析.md》序号55/56 | 问题识别与建议报告。
