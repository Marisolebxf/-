# 深圳产业分布区域数（M_CHAIN_SZ_REGION_COUNT）

## 基本信息

- 指标ID: M_CHAIN_SZ_REGION_COUNT
- 指标名称: 深圳产业分布区域数
- 一级模块: 产业链分析
- 二级模块: 产业总览
- 三级模块: 深圳产业现状
- 更新频率: 日
- 对齐状态判定: 已对齐
- 是否在数据库: 是
- 关联Q编号: Q-CHAIN-03

## 口径定义

深圳产业链关联企业覆盖的行政区去重数量。

## 计算公式

COUNT(DISTINCT chain_sz_dist.district) WHERE chain_id=:chain_id。

## 源库表字段

gkxlumenx_ads.chain_sz_dist（48 行；district）

## 待建表字段

无

## 参考文献 / 依据

需求文档 1.1.1.1.1.1.1.3；深圳产业分布区域数。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
