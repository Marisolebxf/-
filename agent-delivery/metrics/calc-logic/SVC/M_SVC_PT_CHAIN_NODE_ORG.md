# 产业链节点服务机构数（M_SVC_PT_CHAIN_NODE_ORG）

## 基本信息

- 指标ID: M_SVC_PT_CHAIN_NODE_ORG
- 指标名称: 产业链节点服务机构数
- 一级模块: 产业服务链分析
- 二级模块: 专题服务
- 三级模块: 服务机构产业分布
- 更新频率: 季度
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-06

## 口径定义

选定产业领域内，在指定服务链环节(六环节字典)有服务供给的机构计数。

## 计算公式

COUNT(org) GROUP BY field_id, stage_id。

## 源库表字段

demo_gkxlumenx_ads.svc_metric_dist(metric_id=M_SVC_INDUSTRY_LAYOUT, category, value) — 97行; demo_gkxlumenx_dwd.svc_org_circle(hit_fields含industry_l1-l4_name) — 3525行

## 待建表字段

产业链节点归属映射表(需专家知识库定义环节归属规则)

## 参考文献 / 依据

需求文档§1.1.1.1.1.1.1.33.2; 六类服务类型有数据但产业链节点归属依赖专家知识库未建

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
