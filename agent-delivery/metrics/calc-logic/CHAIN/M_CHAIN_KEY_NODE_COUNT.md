# 关键环节数（M_CHAIN_KEY_NODE_COUNT）

## 基本信息

- 指标ID: M_CHAIN_KEY_NODE_COUNT
- 指标名称: 关键环节数
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 关键环节识别
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-05

## 口径定义

按当前阈值识别为关键链位环节的数量。

## 计算公式

COUNT WHERE chain_key_node.is_key_node=true。

## 源库表字段

gkxlumenx_ads.chain_key_node（41 行；is_key_node）

## 待建表字段

无；但阈值规则需固化

## 参考文献 / 依据

关键环节识别结果；ADS 有 is_key_node。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
