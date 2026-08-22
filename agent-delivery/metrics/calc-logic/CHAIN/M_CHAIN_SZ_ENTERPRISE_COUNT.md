# 深圳产业链企业数（M_CHAIN_SZ_ENTERPRISE_COUNT）

## 基本信息

- 指标ID: M_CHAIN_SZ_ENTERPRISE_COUNT
- 指标名称: 深圳产业链企业数
- 一级模块: 产业链分析
- 二级模块: 产业总览
- 三级模块: 深圳产业现状
- 更新频率: 日
- 对齐状态判定: 已对齐
- 是否在数据库: 是
- 关联Q编号: Q-CHAIN-03

## 口径定义

注册地在深圳且属于目标产业链的企业去重数。

## 计算公式

SUM(chain_sz_dist.enterprise_count) WHERE chain_id=:chain_id；或 chain_sz_elements.enterprise_count。

## 源库表字段

gkxlumenx_ads.chain_sz_dist（48 行）；gkxlumenx_ads.chain_sz_elements（8 行）

## 待建表字段

无

## 参考文献 / 依据

需求文档 1.1.1.1.1.1.1.3；深圳产业现状模块。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
