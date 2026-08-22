# 链位关系数（M_CHAIN_EDGE_COUNT）

## 基本信息

- 指标ID: M_CHAIN_EDGE_COUNT
- 指标名称: 链位关系数
- 一级模块: 产业链分析
- 二级模块: 产业总览
- 三级模块: 产业链全景
- 更新频率: 日
- 对齐状态判定: 已对齐
- 是否在数据库: 是
- 关联Q编号: Q-CHAIN-02

## 口径定义

统计当前产业链图谱中有效链位环节关系的数量。

## 计算公式

chain_panorama.edge_count WHERE chain_id=:chain_id。

## 源库表字段

gkxlumenx_ads.chain_panorama（8 行）；gkxlumenx_ads.chain_panorama_edges（832 行）

## 待建表字段

无

## 参考文献 / 依据

需求文档 1.1.1.2.4.2.2.1；全景图关系边数。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
