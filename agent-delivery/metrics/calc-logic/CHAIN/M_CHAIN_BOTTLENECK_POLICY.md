# 瓶颈政策指数（M_CHAIN_BOTTLENECK_POLICY）

## 基本信息

- 指标ID: M_CHAIN_BOTTLENECK_POLICY
- 指标名称: 瓶颈政策指数
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 瓶颈堵点识别
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-06

## 口径定义

用于识别政策覆盖、兑现与协同约束的维度指标。

## 计算公式

chain_bottleneck.policy_score。

## 源库表字段

gkxlumenx_ads.chain_bottleneck（8 行；policy_score）

## 待建表字段

政策覆盖率底层指标未单独落到 ADS

## 参考文献 / 依据

五维诊断维度；ADS 有 policy_score。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
