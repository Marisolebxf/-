# [新增] 技术点影响力（M_ENT_DS_02_ENTITY_004）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_DS_02_ENTITY_004 |
| 指标名称 | [新增] 技术点影响力 |
| 一级模块 | 企业分析 |
| 二级模块 | 企业评估 |
| 三级模块 | - |
| 更新频率 | 月度 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q009 |

## 口径定义

在产业全要素图谱中，对某一技术点（技术实体）所关联的企业、科研机构、人才、专利、论文等实体，按关联规模与关联实体的影响力计算技术点综合影响力，并对关联实体做优先级排序输出。对象=技术点及其关联实体，粒度=技术点。禁止用 PATH 中心度/关键节点或 `M_SVC_GRAPH_INFLUENCE` 顶替（见 ENT-D04 / ENT-B03）。

## 计算逻辑说明

技术点影响力 = 关联规模 × 关联实体影响力 的加权综合，分两维。

### 第一步：入集

技术点 = 图谱节点中 `node_type` 为技术实体的节点（`graph_node`）；关联实体 = 与技术点有边的实体（`graph_edge` / `enterprise_graph_rel`）。技术点—企业/机构关联可经 `dwd_org_base_info_patent_rel` 映射。

### 第二步：两个子项

1. **关联规模**：`COUNT(DISTINCT 关联实体)`，按实体类型（企业/机构/人才/专利/论文）分列。
2. **关联实体影响力**：关联企业技术力均值 `AVG(tech_power_index)`，或关联实体网络中心性（`enterprise_centrality.pagerank_score` / `centrality_norm`）。

综合：$Influence_{tech} = w_1 \cdot Norm(规模) + w_2 \cdot Norm(影响力)$，输出关联实体按影响力降序。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 技术点影响力 | 技术点关联规模 | 关联企业/机构数 | 技术点关联的企业/科研机构去重数。 | COUNT(DISTINCT 实体) | graph_node(node_id, node_type, ref_id, name, props) — 技术点节点；graph_edge(edge_id, src_id, dst_id, edge_type, weight, event_date, props) — 技术点-实体边；enterprise_graph_rel(src_type, src_id, dst_type, dst_id, rel_type, valid_from, valid_to) — 企业图谱关系 | 技术实体专有节点类型及技术点-实体关系表 |
|  |  | 关联专利/论文数 | 技术点关联的专利、论文去重数。 | COUNT(DISTINCT 专利/论文) | dwd_org_base_info_patent_rel(org_id, base_external_id, patent_id, publication_number) — 机构-专利关联 | 技术点-专利/论文关联表 |
| 技术点影响力 | 技术点关联实体影响力 | 关联企业技术力均值 | 技术点关联企业技术力指数均值。 | AVG(tech_power_index) | tech_power(org_id, tech_power_index) — 关联企业技术力 | 无 |
|  |  | 关联实体网络中心性 | 关联实体在图谱中的 PageRank/中心性。 | AVG(pagerank_score)/centrality_norm | enterprise_centrality(org_id, enterprise_name, pagerank_score, centrality_norm, degree, is_key_node) — 实体中心性 | 技术点级中心性字段 |

## 源表字段

- graph_node(node_id, node_type, ref_id, name, props) — 技术点节点（图谱节点）
- graph_edge(edge_id, src_id, dst_id, edge_type, weight, event_date, props) — 技术点-实体边（图谱边）
- enterprise_graph_rel(src_type, src_id, dst_type, dst_id, rel_type, valid_from, valid_to) — 企业图谱关系
- dwd_org_base_info_patent_rel(org_id, base_external_id, patent_id, publication_number) — 机构-专利关联
- tech_power(org_id, tech_power_index) — 关联企业技术力（ADS）
- enterprise_centrality(org_id, enterprise_name, pagerank_score, centrality_norm, degree, is_key_node) — 实体中心性（ADS）

## 待建字段

- 技术实体专有节点/关系表：图谱 `graph_node` 可承载技术点，但「技术实体」作为独立实体类型及「技术点—实体」专属关系表现无落库，需在产业全要素图谱中先建立技术实体节点。
- 技术点—专利/论文关联表：现仅有机构-专利关联，缺技术点粒度关联。

## 参考资料

[1] 技术实体识别构建/技术实体关系抽取 | 算法库 §1.1.1.1.1.1.1.2.3 / §1.1.1.1.1.1.1.2.4 | 技术实体与关联实体的识别与关系建模 | 关联 Q009。

[2] 网络指标计算 API | 算法库 §1.1.1.1.1.1.1.2.15 | 网络密度、中心度等网络指标 | 关联 Q009。
