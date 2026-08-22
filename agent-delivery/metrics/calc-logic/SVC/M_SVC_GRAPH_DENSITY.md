# 服务网络密度（M_SVC_GRAPH_DENSITY）

## 基本信息

- 指标ID: M_SVC_GRAPH_DENSITY
- 指标名称: 服务网络密度
- 一级模块: 产业服务链分析
- 二级模块: 服务链分析
- 三级模块: 图谱分析
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-03

## 口径定义

当前可见子网的无向图密度: 实际边数与最大可能边数之比(标准图论口径)。

## 计算公式

density = 2E / (N × (N-1)), N≥2; N<2不输出。

## 源库表字段

demo_gkxlumenx_ads.svc_relation_chain(org_id, density) — 51行, density值均为0.000453; demo_gkxlumenx_ads.graph_edge(src_key, dst_key) — 405行

## 待建表字段

关系边(投资/合作/竞争/人才流动)正式数据源(当前为演示边数据)

## 参考文献 / 依据

需求文档§1.1.1.2.4.2.7.5.2; svc_relation_chain有51行density值, graph_edge有405行边, 但边数据为演示态

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
