# 产业发展潜力综合评估（M_ENT_DS_07_INDUSTRY_POTENTIAL_006）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_DS_07_INDUSTRY_POTENTIAL_006 |
| 指标名称 | 产业发展潜力综合评估 |
| 一级模块 | 企业分析 |
| 二级模块 | 企业评估 |
| 三级模块 | - |
| 更新频率 | 年度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q009 |

## 口径定义

将产业发展潜力的各项指标综合展示，用户自定义指标权重，按权重计算综合得分，输出产业发展潜力的综合评估结果与排名。对象=产业（领域），不是单个企业/机构。禁止 mapped 183/135/186，禁止 mapped 05 seq 151，不 also_in 专题（见 POT-D06）。产业投入、产业产值、科学影响力、技术影响力、技术产品成熟度五维构成潜力综合。

## 计算逻辑说明

五维加权，各维极值归一后按用户权重（默认等权，ΣW=1）加权得综合得分，再排名。

### 第一步：入集

产业→企业/机构→财务/论文/专利映射同上（科学/技术影响力见 004/005）。

### 第二步：五个子项

1. **产业投入**：研发投入强度 = `SUM(arch_development_am)` / `SUM(operating_revenue)`；固定资产投资 = `SUM(fixed_assets)`。
2. **产业产值**：产业总产值 = `SUM(operating_revenue)`；产业利润 = `SUM(total_profit)`。
3. **科学影响力**：论文被引（引用 M_ENT_DS_07_INDUSTRY_POTENTIAL_004）。
4. **技术影响力**：专利被引（引用 M_ENT_DS_07_INDUSTRY_POTENTIAL_005）。
5. **技术产品成熟度**：技术成熟度等级（技术生命周期分析，待建）。

综合：$Score = \sum_k W_k \times Norm(维度得分_k)$，输出产业综合得分与排名。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 产业发展潜力综合评估 | 产业投入 | 研发投入强度 | 研发投入金额 ÷ 营业收入。 | SUM(研发投入)/SUM(营收) | dwd_org_annual_financial_info(org_id, year, arch_development_am, operating_revenue) — 研发投入,营收 | 无 |
|  |  | 固定资产投资 | 产业固定资产总额合计。 | SUM(fixed_assets) | dwd_org_annual_financial_info(org_id, year, fixed_assets) — 固定资产总额 | 无 |
| 产业发展潜力综合评估 | 产业产值 | 产业总产值 | 产业营业收入合计。 | SUM(operating_revenue) | dwd_org_annual_financial_info(org_id, year, operating_revenue) — 营业收入 | 无 |
|  |  | 产业利润 | 产业利润总额合计。 | SUM(total_profit) | dwd_org_annual_financial_info(org_id, year, total_profit) — 利润总额 | 无 |
| 产业发展潜力综合评估 | 科学影响力 | 论文被引 | 引用 004 科学影响力。 | SUM(citation_num) | dwd_zh_paper_citation(id, citation_num) — 中文被引 | 英文论文被引次数字段 |
| 产业发展潜力综合评估 | 技术影响力 | 专利被引 | 引用 005 技术影响力。 | SUM(cited_by_nums) | dwd_patent_cited(pn, cited_by_nums) — 专利被引 | 标准必要专利标签表 |
| 产业发展潜力综合评估 | 技术产品成熟度 | 技术成熟度等级 | 技术生命周期成熟度评分。 | 成熟度评分 | 无 | 技术成熟度标签表 |
|  |  | 权重配置 | 用户自定义维度权重。 | ΣW_k×Norm(维度) | eval_weight(model, dimension, name_zh, weight, description) — 权重配置 | 无 |

## 源表字段

- dwd_org_annual_financial_info(org_id, year, arch_development_am, fixed_assets, operating_revenue, total_profit) — 研发投入/固定资产/产值/利润
- dwd_zh_paper_citation(id, citation_num) — 中文被引（科学影响力）
- dwd_patent_cited(pn, cited_by_nums) — 专利被引（技术影响力）
- eval_weight(model, dimension, name_zh, weight, description) — 维度权重配置（ADS）

## 待建字段

- 技术产品成熟度标签表：技术生命周期/市场渗透分析所需成熟度分级现无表。
- 英文论文被引次数字段、标准必要专利标签表：见 004 / 005 待建。

## 参考资料

[1] 产业发展潜力综合评估 | 需规 SRS《科技创新评估.md》序号151 | 自定义权重加权综合得分与排名 | 关联 Q009。

[2] 产业投入分析/技术产品成熟度评估/产业产值分析 | 需规 SRS《科技创新评估.md》序号146/147/148 | 产业发展潜力指标展示维度来源。
