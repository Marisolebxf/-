# 产业链数量（M_CHAIN_TOTAL_COUNT）

## 基本信息

- 指标ID: M_CHAIN_TOTAL_COUNT
- 指标名称: 产业链数量
- 一级模块: 产业链分析
- 二级模块: 产业总览
- 三级模块: 产业概况
- 更新频率: 日
- 对齐状态判定: 已对齐
- 是否在数据库: 是
- 关联Q编号: Q-CHAIN-02

## 口径定义

统计当前产业领域目录中去重后的产业链对象数量，按 chain_id 去重。

## 计算公式

COUNT(DISTINCT chain_panorama.chain_id)。

## 源库表字段

gkxlumenx_ads.chain_panorama（8 行；chain_id、chain_name）

## 待建表字段

无

## 参考文献 / 依据

需求文档 1.1.1.2.4.2.2.1；chain_panorama 有 8 条产业链。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
