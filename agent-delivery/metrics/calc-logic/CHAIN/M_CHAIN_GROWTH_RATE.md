# 增长率（M_CHAIN_GROWTH_RATE）

## 基本信息

- 指标ID: M_CHAIN_GROWTH_RATE
- 指标名称: 增长率
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 产业周期分析
- 更新频率: 年度
- 对齐状态判定: 已对齐
- 是否在数据库: 是
- 关联Q编号: Q-CHAIN-04

## 口径定义

产业链市场规模或企业规模在观察期的同比增长率，用于刻画产业扩张速度。

## 计算公式

chain_market.growth_rate 或 (本期规模-上期规模)/上期规模*100。

## 源库表字段

gkxlumenx_ads.chain_market（40 行；growth_rate）；gkxlumenx_ads.chain_cycle（8 行；growth_rate）

## 待建表字段

无

## 参考文献 / 依据

产业周期分析输入参数；growth_rate 字段已在 ADS 存在。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
