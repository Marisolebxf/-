# 环节健康度（M_CHAIN_LINK_HEALTH）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_LINK_HEALTH |
| 指标名称 | 环节健康度 |
| 一级模块 | 产业链分析 |
| 二级模块 | 产业关键环节识别 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

指定产业链各环节在统计窗内的健康度综合评分，从技术成熟度、人才供给、市场容量、融资资本、政策覆盖五维正向评定，取值 0—100。分数越高表示环节越健康、越不构成瓶颈。对象=环节（节点）健康状态。算法库瓶颈叶仅做五维堵点识别，无独立「环节健康度」叶子，本口径为学术补定义。

## 计算逻辑说明

SRS 需规「多维度瓶颈综合分析」（序号 33）明确要求「整合技术成熟度、人才供给量、融资事件、政策覆盖率等指标，对每个产业环节进行健康度评分」。算法库「产业瓶颈堵点识别模型」只输出五维堵点评分（负向），本指标将五维堵点评分正向化为健康度。五维：技术成熟度 / 人才供给 / 市场容量 / 融资资本 / 政策覆盖，默认等权（ΣW=1）。

### 第一步：五维取值（环节/节点级）

- **技术成熟度**：环节专利密度与高企标签，TRL 思想近似（`dwd_org_industry_chain_pat_dtl` 专利数、`dwd_org_tech_tag` 高企）。
- **人才供给**：环节企业研发人员数（`dwd_org_annual_financial_info.development_employee`）或学者关联数。
- **市场容量**：环节企业营收（`dwd_org_annual_financial_info.operating_revenue` 聚合）。
- **融资资本**：环节融资事件金额（`chain_investment.amount`）。
- **政策覆盖**：环节相关有效政策数（`dwd_policy_base` 命中环节/产业标签）。

### 第二步：健康度评分

各维 min-max 归一到 0—100，等权求和：
$$
环节健康度 = \frac{1}{5}(技术成熟度 + 人才供给 + 市场容量 + 融资资本 + 政策覆盖)
$$

（注：若采用 `chain_bottleneck` 五维堵点分，则健康度 = 100 − 堵点综合分，作负向转正向处理。）

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 环节健康度 | 技术成熟度 | 环节专利密度 | 环节专利数/企业数归一 | min-max(环节专利数/环节企业数) | dwd_org_industry_chain_pat_dtl(chain_code, node_id, pn) — 环节专利；chain_enterprise(chain_id, enterprise_id) — 环节企业 | 环节级技术成熟度字段 |
|  | 人才供给 | 环节研发人员数 | 环节企业研发人员合计归一 | min-max(Σ development_employee) | dwd_org_annual_financial_info(org_id, year, development_employee) — 研发人员；chain_enterprise(chain_id, enterprise_id) — 环节企业 | 环节级人才供给字段 |
|  | 市场容量 | 环节企业营收 | 环节企业营业收入合计归一 | min-max(Σ operating_revenue) | dwd_org_annual_financial_info(org_id, year, operating_revenue) — 营收；chain_enterprise(chain_id, enterprise_id) — 环节企业 | 环节级市场容量字段 |
|  | 融资资本 | 环节融资额 | 环节融资事件金额合计归一 | min-max(Σ amount) | chain_investment(chain_id, enterprise_id, amount, round) — 融资明细；chain_enterprise(chain_id, enterprise_id) — 环节企业 | 环节级融资字段 |
|  | 政策覆盖 | 环节政策覆盖数 | 命中环节/产业标签的有效政策数归一 | min-max(COUNT 有效政策) | dwd_policy_base(id, title, keywords, keypoints, theme, status) — 政策标签；dwd_industry_chain_info(industry_code, industry_link_code, industry_link_name) — 环节标签 | 环节级政策覆盖字段 |

## 源表字段

- chain_bottleneck(chain_id, chain_name, tech_score, talent_score, market_score, capital_score, policy_score, overall_score, bottleneck_dims) — 五维堵点评分（gkxlumenx_ads / demo_gkxlumenx_ads，负向，可转健康度）
- chain_node_scoring(chain_id, chain_name, node_name, degree_centrality, betweenness_centrality, enterprise_density, criticality_score) — 环节评分
- dwd_org_industry_chain_pat_dtl(chain_code, node_id, pn) — 技术成熟度
- dwd_org_annual_financial_info(org_id, year, operating_revenue, development_employee) — 市场容量/人才供给
- chain_investment(investment_id, chain_id, enterprise_id, amount, round) — 融资资本
- dwd_policy_base(id, title, keywords, keypoints, theme, status) — 政策覆盖
- chain_enterprise(chain_id, enterprise_id, enterprise_name) — 环节企业入集

## 待建字段

- 环节级（节点级）五维基础字段（现 `chain_bottleneck` 为产业链粒度，非节点粒度）
- 环节健康度正向评分公式与阈值（学术补定义，待甲方确认）
- 技术成熟度等级（TRL）标注字段

## 参考资料

[1] 多维度瓶颈综合分析｜科技专题服务系统 SRS 产业链分析 序号 33（技术成熟度/人才供给/融资/政策覆盖等环节健康度评分）。

[2] 技术成熟度 TRL｜NASA｜Technology Readiness Level 分级体系（技术成熟度评估）。

[3] 产业链现代化水平评估｜中国电子信息产业发展研究院（赛迪）｜产业链环节健康度五维评估（技术/人才/市场/资本/政策）。
