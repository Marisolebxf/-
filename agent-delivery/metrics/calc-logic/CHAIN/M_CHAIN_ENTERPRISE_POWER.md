# 商业力（M_CHAIN_ENTERPRISE_POWER）

## 基本信息

- 指标ID: M_CHAIN_ENTERPRISE_POWER
- 指标名称: 商业力
- 一级模块: 产业链分析
- 二级模块: 区域产业分析
- 三级模块: 区域产业指数评价
- 更新频率: 季度
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-07

## 口径定义

按区域内商业化能力、营收与融资事件等形成的综合得分。

## 计算公式

chain_region_index.enterprise_score。

## 源库表字段

gkxlumenx_ads.chain_region_index（47 行；enterprise_score）

## 待建表字段

商业化能力底层指标未在 ADS 单独落表

## 参考文献 / 依据

区域指数四力之一；ADS 有 enterprise_score。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
