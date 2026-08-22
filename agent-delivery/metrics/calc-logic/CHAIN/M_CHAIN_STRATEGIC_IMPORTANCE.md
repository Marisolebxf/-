# 战略重要度（M_CHAIN_STRATEGIC_IMPORTANCE）

## 基本信息

- 指标ID: M_CHAIN_STRATEGIC_IMPORTANCE
- 指标名称: 战略重要度
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 关键环节识别
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-05

## 口径定义

按当前维度对链位环节战略重要性形成的分级结果。

## 计算公式

由 chain_key_node 的关键性/排名映射为高、中、低。

## 源库表字段

gkxlumenx_ads.chain_key_node（41 行；rank、is_key_node）

## 待建表字段

战略重要度分级阈值正式定义

## 参考文献 / 依据

关键环节识别；ADS 有 rank/is_key_node。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
