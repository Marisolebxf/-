# 产业周期阶段（M_CHAIN_CYCLE_STAGE）

## 基本信息

- 指标ID: M_CHAIN_CYCLE_STAGE
- 指标名称: 产业周期阶段
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 产业周期分析
- 更新频率: 按需
- 对齐状态判定: 已对齐
- 是否在数据库: 是
- 关联Q编号: Q-CHAIN-04

## 口径定义

产业链当前所处生命周期阶段，如导入期、成长期、成熟期或衰退期。

## 计算公式

chain_cycle.cycle_stage WHERE chain_id=:chain_id。

## 源库表字段

gkxlumenx_ads.chain_cycle（8 行；cycle_stage）

## 待建表字段

无

## 参考文献 / 依据

产业周期分析结果；ADS 已存 cycle_stage。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
