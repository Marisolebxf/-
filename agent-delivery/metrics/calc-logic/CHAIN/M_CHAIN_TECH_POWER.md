# 技术力（M_CHAIN_TECH_POWER）

## 基本信息

- 指标ID: M_CHAIN_TECH_POWER
- 指标名称: 技术力
- 一级模块: 产业链分析
- 二级模块: 区域产业分析
- 三级模块: 区域产业指数评价
- 更新频率: 季度
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-07

## 口径定义

按区域内专利、技术成熟度与技术壁垒等形成的综合得分。

## 计算公式

由专利、技术成熟度和技术壁垒标准化后加权；当前 region_index 无独立 tech_score。

## 源库表字段

gkxlumenx_ads.chain_region_index（47 行；enterprise_score、academic_score、ecosystem_score）

## 待建表字段

技术力独立字段 tech_score 尚未落到 ADS

## 参考文献 / 依据

区域指数四力之一；tech_score 待补字段。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
