# 深圳产业链完整度（M_CHAIN_SZ_COMPLETENESS）

## 基本信息

- 指标ID: M_CHAIN_SZ_COMPLETENESS
- 指标名称: 深圳产业链完整度
- 一级模块: 产业链分析
- 二级模块: 深圳产业分析
- 三级模块: 深圳产业情况对比
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-09

## 口径定义

按当前链位覆盖情况形成的深圳产业链完整度结果。

## 计算公式

covered_nodes/total_nodes；当前 chain_sz_panorama 有 node_count。

## 源库表字段

gkxlumenx_ads.chain_sz_panorama（8 行；node_count、nodes、edges）

## 待建表字段

完整度计算公式和阈值待固化

## 参考文献 / 依据

深圳产业分析与发展方案指标。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
