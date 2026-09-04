# 产业瓶颈堵点识别模型（M_CHAIN_DEEP_125_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_125_1 |
| 指标名称 | 产业瓶颈堵点识别模型 |
| 一级模块 | 产业链分析 |
| 二级模块 | 产业关键环节识别 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

面向区域与行业发展中的关键制约因素，基于技术、人才、市场需求、资金、政策五大维度构建指标体系与阈值判断机制，计算各维指标值，自动提取并标识产业瓶颈堵点，输出瓶颈成因、影响范围与解决路径。对象=产业运行瓶颈，五维分越低越接近瓶颈。

## 计算逻辑说明

① 五维指标：技术（技术成熟度/环节专利密度）、人才（人才供给量/研发人员占比）、市场需求（需求增长/份额）、资金（融资事件数/金额）、政策（政策覆盖率）。② 各维评分：指标值极值归一后得 tech_score/talent_score/market_score/capital_score/policy_score。③ 瓶颈判定：分低于阈值的维度标记为 bottleneck_dims，综合 overall_score，输出 severity 与 suggestions。

- 技术得分 = 归一化(环节专利密度)
- 人才得分 = 归一化(研发人员占比)
- 市场得分 = 归一化(需求增长率)
- 资金得分 = 归一化(融资事件数/金额)
- 政策得分 = 归一化(政策覆盖率)
- 综合分 overall_score = Σ(Wi × 五维得分)

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 产业瓶颈堵点识别模型 | 技术维度 | 技术成熟度/专利密度 | 环节专利数量与技术储备水平。 | 归一化(环节专利数/发明授权) | dwd_org_industry_chain_pat_dtl(chain_code, node_id, pn, apdt)；dwd_patent(pn, kind, granted_number) | 技术成熟度指标表 |
| 产业瓶颈堵点识别模型 | 人才维度 | 人才供给量/研发人员占比 | 产业研发人员占从业人员比重。 | SUM(development_employee) ÷ SUM(employees_number) | dwd_org_annual_financial_info(org_id, year, development_employee, employees_number)；dwd_org_industry_tags(credit_code) | 人才供给量指标表（按环节） |
| 产业瓶颈堵点识别模型 | 市场需求维度 | 市场需求增长 | 产业营收/企业规模增速。 | 增长率 | chain_market(chain_id, chain_name, stat_year, total_revenue, growth_rate)；chain_enterprise_stat(growth_rate) | 无 |
| 产业瓶颈堵点识别模型 | 资金维度 | 融资事件数/金额 | 产业投融资活跃度。 | COUNT(融资事件)/SUM(金额) | dwd_org_financing_info(org_id, funding_round, funding_amount, completion_date)；chain_investment(chain_id, chain_name, investment_id, amount, invest_date) | 无 |
| 产业瓶颈堵点识别模型 | 政策维度 | 政策覆盖率 | 产业相关有效政策覆盖环节/类型比例。 | 覆盖环节数 ÷ 环节总数 | dwd_policy_base(id, title, publish_year, rank, type, theme, status, province, city) | 政策覆盖率指标表（政策-环节匹配） |
| 产业瓶颈堵点识别模型 | 综合判定 | 瓶颈综合分 | 五维得分加权综合分。 | Σ(Wi × 五维得分) | gkxlumenx_ads.chain_bottleneck(chain_id, chain_name, tech_score, talent_score, market_score, capital_score, policy_score, overall_score, bottleneck_dims, bottleneck_detail, severity, suggestions) | 五维权重与阈值参数表 |

## 源表字段

- dwd_org_industry_chain_pat_dtl(chain_code, chain_name, node_id, node_name, apno, apdt, pn, current_assign) — 专利-环节挂接（技术维度）
- dwd_patent(pn, kind, granted_number) — 专利类型
- dwd_org_annual_financial_info(org_id, year, development_employee, employees_number, arch_development_am) — 研发人员（人才维度）
- dwd_org_financing_info(org_id, name_cn, funding_round, funding_amount, completion_date) — 融资（资金维度）
- chain_investment(chain_id, chain_name, investment_id, amount, invest_date) — 投融资明细
- chain_market(chain_id, chain_name, stat_year, total_revenue, enterprise_count, growth_rate) — 市场需求
- chain_enterprise_stat(chain_id, chain_name, stat_year, enterprise_count, growth_rate) — 企业增长
- dwd_policy_base(id, title, publish_year, rank, type, theme, status, province, city) — 政策（政策维度）
- dwd_org_industry_tags(industry_code, industry_link_code, credit_code) — 企业-产业挂接
- gkxlumenx_ads.chain_bottleneck(chain_id, chain_name, tech_score, talent_score, market_score, capital_score, policy_score, overall_score, bottleneck_dims, bottleneck_detail, severity, suggestions) — 瓶颈识别结果

## 待建字段

- 技术成熟度指标表（技术等级/成熟度评级）
- 人才供给量指标表（人才按环节归集）
- 政策覆盖率指标表（政策-环节类型匹配关系）
- 五维权重与阈值参数表

## 参考资料

[1] 产业链供应链韧性与安全（「卡脖子」环节识别）|工业和信息化部|https://www.miit.gov.cn/

[2] 高新技术企业认定管理办法（国科发火〔2016〕32号）|科技部、财政部、税务总局|https://www.gov.cn/gongbao/content/2016/content_5076985.htm

[3] 区域创新能力监测指标体系|科学技术部|https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/t20131129_110674.html
