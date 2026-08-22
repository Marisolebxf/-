# 高价值环节占比（M_CHAIN_HIGH_VALUE_RATIO）

## 基本信息

- 指标ID: M_CHAIN_HIGH_VALUE_RATIO
- 指标名称: 高价值环节占比
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 关键环节识别
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-05

## 口径定义

关键环节中高价值环节数量占有效环节数量的比例。

## 计算公式

COUNT(high_end_index 高于阈值)/COUNT(有效环节)*100。

## 源库表字段

gkxlumenx_ads.chain_key_node（41 行；high_end_index）

## 待建表字段

高价值阈值正式定义

## 参考文献 / 依据

关键环节识别结果；ADS 有 high_end_index。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
