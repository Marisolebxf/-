# 附加值率（M_CHAIN_ADDED_VALUE_RATE）

## 基本信息

- 指标ID: M_CHAIN_ADDED_VALUE_RATE
- 指标名称: 附加值率
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 关键环节识别
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-05

## 口径定义

衡量链位环节价值创造与高端化水平，按产值结构与技术含量加权。

## 计算公式

chain_key_node.value_added_score 或环节产值/总投入标准化。

## 源库表字段

gkxlumenx_ads.chain_key_node（41 行；value_added_score）

## 待建表字段

正式附加值率的分母、口径和阈值待定义

## 参考文献 / 依据

关键环节识别因子；ADS 有 value_added_score，正式口径待闭合。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
