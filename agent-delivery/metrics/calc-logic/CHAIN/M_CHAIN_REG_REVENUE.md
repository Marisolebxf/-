# 营收（M_CHAIN_REG_REVENUE）

## 基本信息

- 指标ID: M_CHAIN_REG_REVENUE
- 指标名称: 营收
- 一级模块: 产业链分析
- 二级模块: 区域产业分析
- 三级模块: 区域产业指数评价
- 更新频率: 季度
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-07

## 口径定义

区域内相关企业营收规模与增长相关口径。

## 计算公式

SUM(enterprise 营收) 后标准化。

## 源库表字段

gkxlumenx_dwd.chain_enterprise（120 行）；gkxlumenx_dwd.chain_enterprise_stat（209 行）

## 待建表字段

企业营收明细与区域映射表待补

## 参考文献 / 依据

区域产业指数预设指标，原型归属商业力。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
