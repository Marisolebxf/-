# 生态影响力评分（M_SVC_GRAPH_INFLUENCE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SVC-seed.yaml。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SVC_GRAPH_INFLUENCE |
| 指标名称 | 生态影响力评分 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 产业服务链分析 |
| 三级模块 | 服务链图谱分析 |
| 更新频率 | 按需 |
| 对齐状态判定 | 待甲方Q-SVCCHAIN-03；边表已对extract |
| 是否在数据库 | 否 |
| 关联Q编号 | Q-SVCCHAIN-03 |

## 口径定义

选定服务机构在当前可见服务关系子网中的生态影响力综合评分，从度中心性、介数中心性、接近中心性三个维度评定，取值 0—100。

## 计算逻辑说明

第一步：构建服务链网络图谱

将服务链中的各类服务机构作为节点，将机构之间的业务往来、合作关系、资源共享等作为边，构建一个无向或有向的网络图 G = (V, E)。其中 V为节点集合（服务机构），E 为边集合（机构间关系）。

第二步：计算各节点的中心性指标

1.度中心性

度中心性衡量节点的直接连接数量，反映节点在网络中的局部影响力。对于节点 v，其归一化度中心性为：
$$
DC(v) = \frac{deg(v)}{N - 1}
$$
其中，deg(v)$为节点 v的直接连接数，N为网络中的节点总数。

2.介数中心性

介数中心性衡量节点作为其他节点之间最短路径“桥梁”的次数，反映节点在网络中的中介控制力：
$$
BC(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}
$$

$$
其中，\sigma_{st}为节点 s 到节点 t 的最短路径总数，\sigma_{st}(v) 为这些最短路径中经过节点 v的数量。常用归一化版本为：
$$

$$
BC_{norm}(v) = \frac{2 \times BC(v)}{(N-1)(N-2)}
$$

3.接近中心性

接近中心性衡量节点到网络中所有其他节点的平均距离，反映节点在网络中的信息传播效率：
$$
CC(v) = \frac{N - 1}{\sum_{u \neq v} d(v, u)}
$$
其中，d(v, u) 为节点 v到节点 u的最短路径距离。

三、生态影响力评分合成

由于三个中心性指标的量纲和取值范围不同（DC 和 CC 取值在 0-1 之间，BC 取值可能很大），需先进行标准化处理：
$$
指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij} 为节点 i 在第 j个中心性指标上的原始值，\min(x_j) 和 \max(x_j)分别为该指标在所有节点中的最小值和最大值。
$$

将三个中心性指标的标准化得分进行加权汇总：
$$
生态影响力评分 = W_1 \times 度中心性得分 + W_2 \times 介数中心性得分 + W_3 \times 接近中心性得分
$$

$$
其中，W_1、W_2、W_3 可采用等权重（各占 1/3），也可根据评估重点自行制定，\sum W = 1。评分越高，表明该机构在服务链网络中的生态影响力越强。
$$



| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 生态影响力评分 | 度中心性 | 从节点连接数评估局部枢纽程度。 | degree(v)；可复用 M_SVC_GRAPH_CENTRALITY | demo_gkxlumenx_ods.svc_org_card(org_id) — 网络节点；dwd_org_invest_info(org_id, inv_org_id) — 投资边；dwd_org_shareholder_info(org_id, inv_org_id, owners_type) — 机构股东边 | 无 |
| 生态影响力评分 | 介数中心性 | 从最短路径经过该点的比例评估桥接影响力。 | betweenness(v) | demo_gkxlumenx_ods.svc_org_card(org_id) — 网络节点；dwd_org_invest_info(org_id, inv_org_id) — 投资边；dwd_org_shareholder_info(org_id, inv_org_id, owners_type) — 机构股东边 | 无 |
| 生态影响力评分 | 接近中心性 | 从到其余节点最短距离评估可达影响力。 | closeness(v)=1/平均最短距离 | demo_gkxlumenx_ods.svc_org_card(org_id) — 网络节点；dwd_org_invest_info(org_id, inv_org_id) — 投资边；dwd_org_shareholder_info(org_id, inv_org_id, owners_type) — 机构股东边 | 无 |

## 源表字段

- demo_gkxlumenx_ads.svc_org_card(org_id, name_cn) — 服务机构清单,网络节点
- dwd_org_invest_info(org_id, inv_org_id) — 投资边
- dwd_org_shareholder_info(org_id, inv_org_id, owners_type) — 机构股东边

## 待建字段

- svc_coop_edge-合作关系边
- svc_talent_flow_edge-人才流动边

## 参考资料

[1]生态影响力评分｜中国传媒大学｜徐杰，王菊韵，张海云. 基于复杂网络的社交网络用户影响力研究[J]. 中国传媒大学学报(自然科学版), 2017, 24(2): 67-73. DOI: 10.16196/j.cnki.issn.1673-4793.2017.02.013.｜
