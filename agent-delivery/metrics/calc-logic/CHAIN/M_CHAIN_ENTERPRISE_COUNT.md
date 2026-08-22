# 关联企业数（M_CHAIN_ENTERPRISE_COUNT）

## 基本信息

- 指标ID: M_CHAIN_ENTERPRISE_COUNT
- 指标名称: 关联企业数
- 一级模块: 产业链分析
- 二级模块: 产业总览
- 三级模块: 产业概况
- 更新频率: 日
- 对齐状态判定: 已对齐
- 是否在数据库: 是
- 关联Q编号: Q-CHAIN-02

## 口径定义

统计指定产业链范围内去重后的关联企业数量，按企业代码去重。

## 计算公式

SUM(chain_enterprise_stat.enterprise_count) WHERE chain_id=:chain_id AND stat_year=最新年份。

## 源库表字段

gkxlumenx_ads.chain_enterprise_stat（40 行；chain_id、stat_year、enterprise_count、high_tech_count）

## 待建表字段

无

## 参考文献 / 依据

需求文档 1.1.1.1.1.1.1.3 企业机构数量；ADS 有企业规模。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
