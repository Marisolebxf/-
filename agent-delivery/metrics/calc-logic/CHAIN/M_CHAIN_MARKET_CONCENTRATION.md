# 市场集中度（M_CHAIN_MARKET_CONCENTRATION）

## 基本信息

- 指标ID: M_CHAIN_MARKET_CONCENTRATION
- 指标名称: 市场集中度
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 关键环节识别
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-05

## 口径定义

衡量链位环节市场结构与头部主体集中程度。

## 计算公式

chain_key_node.market_concentration_score 或 CRn/头部企业份额。

## 源库表字段

gkxlumenx_ads.chain_key_node（41 行；market_concentration_score）

## 待建表字段

CRn 正式定义和头部企业排名规则待定义

## 参考文献 / 依据

关键环节识别因子；ADS 有评分，CRn 口径待闭合。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
