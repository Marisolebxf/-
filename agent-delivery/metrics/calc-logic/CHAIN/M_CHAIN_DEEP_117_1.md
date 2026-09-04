# 产业链全景模型构建（M_CHAIN_DEEP_117_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_117_1 |
| 指标名称 | 产业链全景模型构建 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 是 |
| 关联Q编号 | - |

## 口径定义

针对选定产业链（industry_code），以产业链环节为节点、上下游关系为边，构建全景关系图谱；统计环节节点数、上下游关系边数及各环节关联主体（企业、技术/专利、科研机构、人才、服务机构）的数量与结构，形成产业链「结构—主体—关系」全貌。对象=产业链整体结构，不是单家企业或单个环节的孤立指标。

## 计算逻辑说明

三步：① 入集：按 `industry_code` 圈定产业链，节点取 `industry_chain_node.node_id`（或 `dwd_industry_chain_info.industry_link_code`），边取 `industry_chain_node_rel`（source_node_id→target_node_id）。② 主体挂接：企业用 `dwd_org_industry_tags`（credit_code→industry_link_code），技术/专利用 `dwd_org_industry_chain_pat_dtl`（pn→node_id），科研机构/人才/服务机构用 `industry_chain_entity_rel.entity_type` 分类挂接。③ 统计：环节节点数、关系边数、各环节主体数，输出全景图谱与环节属性统计。

- 环节节点数 = COUNT(DISTINCT node_id)
- 上下游关系边数 = COUNT(DISTINCT relation_id)
- 环节关联企业数 = COUNT(DISTINCT credit_code) 按环节分组
- 环节关联技术(专利)数 = COUNT(DISTINCT pn) 按环节分组
- 环节平均关联度 = 关系边数 ÷ 环节节点数

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 产业链全景模型构建 | 环节结构 | 环节节点数 | 产业链内去重环节节点数量。 | COUNT(DISTINCT node_id) | dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name, level, parent_code, parent_name, node_company_count)；demo_gkxlumenx_dwd.industry_chain_node(node_id, chain_id, node_code, node_name, parent_node_id, node_level, stage_code, node_type) | 无 |
|  |  | 上下游层级数 | 产业链环节树的最大层级深度。 | MAX(node_level) | dwd_industry_chain_info(level, parent_code, industry_link_code)；demo_gkxlumenx_dwd.industry_chain_node(node_level, parent_node_id) | 无 |
| 产业链全景模型构建 | 环节关联关系 | 上下游关系边数 | 环节间上下游/支撑关系数量。 | COUNT(DISTINCT relation_id) | demo_gkxlumenx_dwd.industry_chain_node_rel(relation_id, chain_id, source_node_id, target_node_id, relation_type, relation_direction, relation_weight)；gkxlumenx_ads.chain_panorama_edges(src_id, dst_id, chain_id, edge_type, weight) | 无 |
|  |  | 环节平均关联度 | 平均每个环节的关联关系数。 | 关系边数 ÷ 环节节点数 | demo_gkxlumenx_dwd.industry_chain_node_rel(relation_id, source_node_id, target_node_id)；demo_gkxlumenx_dwd.industry_chain_node(node_id) | 无 |
| 产业链全景模型构建 | 主体要素分布 | 环节关联企业数 | 各环节挂接的去重企业数量。 | COUNT(DISTINCT credit_code) GROUP BY 环节 | dwd_org_industry_tags(industry_code, industry_link_code, company_name, credit_code)；dwd_org_base_info(org_id, name_cn, external_id, province, city, area, reg_status, org_type) | 无 |
|  |  | 环节关联技术(专利)数 | 各环节挂接的去重专利数量。 | COUNT(DISTINCT pn) GROUP BY 环节 | dwd_org_industry_chain_pat_dtl(chain_code, chain_name, node_id, node_name, apno, apdt, pat_name, pn, current_assign) | 无 |
|  |  | 环节关联科研机构/人才/服务机构数 | 按实体类型分类的各环节主体数量。 | COUNT(DISTINCT entity_id) GROUP BY node_id, entity_type | demo_gkxlumenx_dwd.industry_chain_entity_rel(relation_id, chain_id, node_id, entity_type, entity_id, relation_type, role_type) | 环节-人才/科研机构精确挂接明细（若 entity_rel 未全量覆盖） |
| 产业链全景模型构建 |  | 全景图谱要素汇总 | 图谱节点数、边数、企业数的汇总结果。 | node_count/edge_count/enterprise_count 读取 | gkxlumenx_ads.chain_panorama(chain_id, chain_name, node_count, edge_count, enterprise_count, nodes, edges, model_version)；gkxlumenx_ads.chain_panorama_nodes(node_id, chain_id, node_name, node_type, position, enterprise_count, centrality) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name, level, parent_code, parent_name, node_company_count) — 环节/节点字典与层级
- dwd_org_industry_tags(industry_code, industry_link_code, company_name, credit_code) — 企业到环节挂接
- dwd_org_industry_chain_pat_dtl(chain_code, chain_name, node_id, node_name, apno, apdt, pat_name, pn, current_assign) — 专利到环节挂接
- dwd_org_base_info(org_id, name_cn, external_id, province, city, area, reg_status, org_type) — 企业主体属性
- demo_gkxlumenx_dwd.industry_chain_node(node_id, chain_id, node_code, node_name, parent_node_id, node_level, stage_code, node_type) — 归一化环节节点
- demo_gkxlumenx_dwd.industry_chain_node_rel(relation_id, chain_id, source_node_id, target_node_id, relation_type, relation_direction, relation_weight) — 归一化环节关系
- demo_gkxlumenx_dwd.industry_chain_entity_rel(relation_id, chain_id, node_id, entity_type, entity_id, relation_type, role_type) — 环节-主体关系
- gkxlumenx_ads.chain_panorama(chain_id, chain_name, node_count, edge_count, enterprise_count, nodes, edges, model_version) — 全景图谱汇总结果
- gkxlumenx_ads.chain_panorama_nodes(node_id, chain_id, node_name, node_type, position, enterprise_count, centrality) — 全景节点属性
- gkxlumenx_ads.chain_panorama_edges(src_id, dst_id, chain_id, edge_type, weight) — 全景关系边

## 待建字段

- 环节-人才/科研机构/服务机构精确挂接明细（若 `industry_chain_entity_rel` 未全量覆盖五类主体，需补建环节-主体挂接表）

## 参考资料

[1] 产业链供应链韧性与「链长制」|工业和信息化部|《关于开展产业链供应链稳定性和竞争力提升行动的意见》等产业链政策|https://www.miit.gov.cn/

[2] 产业结构调整指导目录（2024年本）|国家发展改革委|产业结构与产业链环节划分依据|https://www.ndrc.gov.cn/

[3] 国民经济行业分类 GB/T 4754—2017|国家统计局|产业与环节编码依据|https://www.stats.gov.cn/
