# 技术成熟度（M_CHAIN_TECH_MATURITY_SCORE）

## 基本信息

- 指标ID: M_CHAIN_TECH_MATURITY_SCORE
- 指标名称: 技术成熟度
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 产业周期分析
- 更新频率: 季度
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-04

## 口径定义

按关键技术成熟度维度计算的综合得分，0-100，得分越高代表技术越成熟。

## 计算公式

chain_cycle 技术成熟度综合分；当前可用 chain_cycle.cycle_stage 或新增 maturity_score。

## 源库表字段

gkxlumenx_ads.chain_cycle（8 行；cycle_stage）

## 待建表字段

技术成熟度评分字段 maturity_score 尚未独立落到 ADS

## 参考文献 / 依据

产业周期分析输入参数；cycle_stage 有值，但独立成熟度得分需补字段。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
