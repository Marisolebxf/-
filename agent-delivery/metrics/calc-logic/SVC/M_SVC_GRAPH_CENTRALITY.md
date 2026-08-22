# 节点度中心性（M_SVC_GRAPH_CENTRALITY）

## 基本信息

- 指标ID: M_SVC_GRAPH_CENTRALITY
- 指标名称: 节点度中心性
- 一级模块: 产业服务链分析
- 二级模块: 服务链分析
- 三级模块: 图谱分析
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-03

## 口径定义

节点在当前可见子网内的连接边数(度); 统计范围随过滤器变化。

## 计算公式

degree(node) = COUNT(edges incident to node)。

## 源库表字段

demo_gkxlumenx_ads.svc_relation_chain(org_id, centrality) — 51行, centrality大多为NULL, 仅少数有值(2.0); demo_gkxlumenx_ads.graph_edge — 405行

## 待建表字段

关系边正式数据源(centrality大多为空)

## 参考文献 / 依据

需求文档§1.1.1.2.4.2.7.5.2; svc_relation_chain有51行但centrality大多NULL, 边数据为演示态

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
