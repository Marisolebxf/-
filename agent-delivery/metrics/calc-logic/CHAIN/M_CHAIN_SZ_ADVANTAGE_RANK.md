# 深圳优势排名（M_CHAIN_SZ_ADVANTAGE_RANK）

## 基本信息

- 指标ID: M_CHAIN_SZ_ADVANTAGE_RANK
- 指标名称: 深圳优势排名
- 一级模块: 产业链分析
- 二级模块: 深圳产业分析
- 三级模块: 深圳产业情况对比
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-09

## 口径定义

深圳在当前对标集合中的产业优势排序。

## 计算公式

RANK() OVER ORDER BY advantage_index DESC。

## 源库表字段

gkxlumenx_ads.chain_sz_advantage（8 行；sz_rank、rank_overall）

## 待建表字段

无

## 参考文献 / 依据

深圳产业分析与发展方案指标。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
