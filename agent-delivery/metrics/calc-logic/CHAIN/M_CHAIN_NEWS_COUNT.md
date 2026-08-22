# 产业资讯数（M_CHAIN_NEWS_COUNT）

## 基本信息

- 指标ID: M_CHAIN_NEWS_COUNT
- 指标名称: 产业资讯数
- 一级模块: 产业链分析
- 二级模块: 产业总览
- 三级模块: 产业概况
- 更新频率: 日
- 对齐状态判定: 已对齐
- 是否在数据库: 是
- 关联Q编号: Q-CHAIN-02

## 口径定义

统计指定产业链范围内符合公开条件的产业资讯数量，按资讯标识去重。

## 计算公式

SUM(chain_news_stat.news_count) WHERE chain_id=:chain_id AND stat_month=最新月份。

## 源库表字段

gkxlumenx_ads.chain_news_stat（126 行；chain_id、stat_month、news_count、hot_count）

## 待建表字段

无

## 参考文献 / 依据

需求文档 1.1.1.1.1.1.1.2 产业资讯；ADS 有月度资讯计数。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
