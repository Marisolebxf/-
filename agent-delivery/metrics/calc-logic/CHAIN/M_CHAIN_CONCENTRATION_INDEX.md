# 市场集中度（M_CHAIN_CONCENTRATION_INDEX）

## 基本信息

- 指标ID: M_CHAIN_CONCENTRATION_INDEX
- 指标名称: 市场集中度
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 关键环节识别
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-05

## 口径定义

表达当前环节代表主体集中程度的演示分级结果。

## 计算公式

由 chain_key_node.market_concentration_score 映射为中高、中低。

## 源库表字段

gkxlumenx_ads.chain_key_node（41 行；market_concentration_score）

## 待建表字段

集中度分级阈值正式定义

## 参考文献 / 依据

与 M_CHAIN_MARKET_CONCENTRATION 同源，页面分级结果。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
