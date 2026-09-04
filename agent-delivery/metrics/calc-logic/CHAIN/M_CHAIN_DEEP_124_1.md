# 产业链关键环节识别模型（M_CHAIN_DEEP_124_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_124_1 |
| 指标名称 | 产业链关键环节识别模型 |
| 一级模块 | 产业链分析 |
| 二级模块 | 产业关键环节识别 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 是 |
| 关联Q编号 | - |

## 口径定义

结合产业创新水平、企业规模和产业附加值等核心维度，对各环节进行量化评分（附加值、技术壁垒、市场集中度、网络中心性），计算高端化指数并识别产业链中具有战略重要性和引领作用的关键环节。对象=产业链环节（节点），不是企业。

## 计算逻辑说明

① 指标计算：附加值（value_added_score，由环节企业利润率/营收派生）、技术壁垒（tech_barrier_score，由环节专利密度/技术复杂度派生）、市场集中度（market_concentration_score，由环节企业规模集中度派生）、网络中心性（degree_centrality/betweenness_centrality，由图谱关系计算）。② 综合：三指标加权得 high_end_index，中心度得 criticality_score，超阈值标 is_key_node。③ 输出关键环节清单与排名 rank。

- 高端化指数 high_end_index = Σ(Wi × {附加值, 技术壁垒, 市场集中度})
- 关键性 criticality_score = Σ(Wj × {度中心度, 介数中心度, 企业密度})
- 关键环节判定 = (high_end_index ≥ 阈值) OR (criticality_score ≥ 阈值)

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 产业链关键环节识别模型 | 附加值维度 | 环节附加值 | 环节的附加值水平评分。 | 归一化(环节企业利润率/营收) | gkxlumenx_ads.chain_key_node(chain_id, chain_name, node_name, value_added_score)；dwd_org_annual_financial_info(org_id, operating_revenue, pure_profit)；dwd_org_industry_tags(industry_link_code, credit_code) | 无 |
| 产业链关键环节识别模型 | 技术壁垒维度 | 技术壁垒得分 | 环节的技术专利密度/复杂度评分。 | 归一化(环节专利数/发明授权占比) | gkxlumenx_ads.chain_key_node(tech_barrier_score)；dwd_org_industry_chain_pat_dtl(chain_code, node_id, node_name, pn, apno)；dwd_patent(pn, kind, granted_number) | 无 |
| 产业链关键环节识别模型 | 市场集中度维度 | 市场集中度得分 | 环节内企业规模集中度评分。 | 归一化(环节内企业营收 HHI/CR4) | gkxlumenx_ads.chain_key_node(market_concentration_score)；dwd_org_annual_financial_info(org_id, operating_revenue)；dwd_org_industry_tags(industry_link_code, credit_code) | 无 |
| 产业链关键环节识别模型 | 网络中心性 | 度数中心度 | 环节在上下游图谱中的连接度数。 | 归一化(环节入度+出度) | gkxlumenx_ads.chain_node_scoring(chain_id, chain_name, node_name, degree_centrality, betweenness_centrality, enterprise_density)；demo_gkxlumenx_dwd.industry_chain_node_rel(source_node_id, target_node_id) | 无 |
|  |  | 介数中心度 | 环节作为上下游桥梁的中介性。 | 经过环节的最短路径占比 | gkxlumenx_ads.chain_node_scoring(betweenness_centrality) | 无 |
| 产业链关键环节识别模型 | 综合判定 | 高端化指数 | 附加值/技术壁垒/集中度加权综合分。 | Σ(Wi × 三维得分) | gkxlumenx_ads.chain_key_node(chain_id, chain_name, node_name, position, enterprise_count, high_end_index, is_key_node, rank) | 无 |
|  |  | 关键环节判定 | 高端化指数/关键性超阈值判定。 | (high_end_index≥阈值) OR (criticality≥阈值) | gkxlumenx_ads.chain_key_node(is_key_node, rank)；chain_node_scoring(criticality_score, rank) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_link_code, industry_link_name, level, node_company_count) — 环节字典
- dwd_org_industry_tags(industry_code, industry_link_code, credit_code, company_name) — 企业-环节挂接
- dwd_org_industry_chain_pat_dtl(chain_code, chain_name, node_id, node_name, apno, pat_name, pn, current_assign) — 专利-环节挂接
- dwd_patent(pn, kind, granted_number, first_applicant_name) — 专利类型（发明授权）
- dwd_org_annual_financial_info(org_id, year, operating_revenue, pure_profit, total_assets) — 财务（附加值/集中度）
- demo_gkxlumenx_dwd.industry_chain_node_rel(relation_id, chain_id, source_node_id, target_node_id, relation_weight) — 上下游关系（中心性）
- gkxlumenx_ads.chain_key_node(chain_id, chain_name, node_name, position, enterprise_count, value_added_score, tech_barrier_score, market_concentration_score, high_end_index, is_key_node, rank) — 关键环节识别结果
- gkxlumenx_ads.chain_node_scoring(chain_id, chain_name, node_name, position, enterprise_count, degree_centrality, betweenness_centrality, enterprise_density, criticality_score, rank) — 节点中心性评分

## 待建字段

- 无（附加值/技术壁垒/集中度底层口径可由财报与专利按环节派生）

## 参考资料

[1] 微笑曲线理论|施振荣（Acer 宏碁），1992 年提出产业价值链附加值分布。

[2] 产业链供应链韧性与「链长制」|工业和信息化部|https://www.miit.gov.cn/

[3] 市场集中度（HHI/CR4）测算方法|国务院反垄断委员会|《关于相关市场界定的指南》|https://www.samr.gov.cn/

[4] 图网络中心度指标|Freeman, L. C. (1978). Centrality in social networks: Conceptual clarification, Social Networks, 1(3), 215-239.
