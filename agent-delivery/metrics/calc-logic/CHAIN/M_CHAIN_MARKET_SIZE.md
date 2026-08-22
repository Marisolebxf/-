# 产业链市场规模（M_CHAIN_MARKET_SIZE）

## 基本信息

- 指标ID: M_CHAIN_MARKET_SIZE
- 指标名称: 产业链市场规模
- 一级模块: 产业链分析
- 二级模块: 产业总览
- 三级模块: 产业概况
- 更新频率: 年度
- 对齐状态判定: 已对齐
- 是否在数据库: 是
- 关联Q编号: Q-CHAIN-01

## 口径定义

统计指定产业链范围内全部关联企业的年度营收合计，单位为亿元；只统计企业主体，不重复计入机构和人才。

## 计算公式

SUM(chain_market.total_revenue) WHERE chain_id=:chain_id AND stat_year=:stat_year。

## 源库表字段

gkxlumenx_ads.chain_market（40 行；chain_id、chain_name、stat_year、total_revenue、enterprise_count、growth_rate）

## 待建表字段

无；若需要跨年规模口径，须补齐 history 维度。

## 参考文献 / 依据

需求文档 1.1.1.2.4.2.2.1 产业链全景节点下钻市场规模；ADS 已有 total_revenue。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
