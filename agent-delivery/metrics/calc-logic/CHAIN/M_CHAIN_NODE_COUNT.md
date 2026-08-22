# 链位环节数（M_CHAIN_NODE_COUNT）

## 基本信息

- 指标ID: M_CHAIN_NODE_COUNT
- 指标名称: 链位环节数
- 一级模块: 产业链分析
- 二级模块: 产业总览
- 三级模块: 产业链全景
- 更新频率: 日
- 对齐状态判定: 已对齐
- 是否在数据库: 是
- 关联Q编号: Q-CHAIN-02

## 口径定义

统计当前产业链图谱中的有效链位环节数量，按节点去重。

## 计算公式

chain_panorama.node_count WHERE chain_id=:chain_id。

## 源库表字段

gkxlumenx_ads.chain_panorama（8 行；node_count、edge_count）；gkxlumenx_ads.chain_panorama_nodes（41 行）

## 待建表字段

无

## 参考文献 / 依据

需求文档 1.1.1.2.4.2.2.1；全景图节点数。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
