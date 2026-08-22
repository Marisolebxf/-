# 技术壁垒指数（M_CHAIN_TECH_BARRIER_INDEX）

## 基本信息

- 指标ID: M_CHAIN_TECH_BARRIER_INDEX
- 指标名称: 技术壁垒指数
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 关键环节识别
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-05

## 口径定义

评估链位环节关键技术、工艺和知识资产壁垒与替代难度的综合指数。

## 计算公式

chain_key_node.tech_barrier_score 或专利密度/工艺复杂度/替代难度加权。

## 源库表字段

gkxlumenx_ads.chain_key_node（41 行；tech_barrier_score）

## 待建表字段

专利密度、替代难度底层指标未单独落到 ADS

## 参考文献 / 依据

关键环节识别因子；ADS 有评分，底层指标待补。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
