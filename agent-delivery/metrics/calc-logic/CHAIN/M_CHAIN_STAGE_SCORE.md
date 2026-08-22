# 周期阶段得分（M_CHAIN_STAGE_SCORE）

## 基本信息

- 指标ID: M_CHAIN_STAGE_SCORE
- 指标名称: 周期阶段得分
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 产业周期分析
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-04

## 口径定义

按当前周期判断维度计算的阶段综合得分，用于刻画当前阶段强度。

## 计算公式

由 chain_cycle.growth_rate、investment_trend、enterprise_trend 加权形成阶段分。

## 源库表字段

gkxlumenx_ads.chain_cycle（8 行；growth_rate、investment_trend、enterprise_trend）

## 待建表字段

阶段得分的正式权重和归一化基准待定义

## 参考文献 / 依据

产业周期分析；阶段分可在 ADS 增加 stage_score 字段后落地。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
