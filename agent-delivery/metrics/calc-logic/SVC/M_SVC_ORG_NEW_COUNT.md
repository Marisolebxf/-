# 年度新增服务机构数（M_SVC_ORG_NEW_COUNT）

## 基本信息

- 指标ID: M_SVC_ORG_NEW_COUNT
- 指标名称: 年度新增服务机构数
- 一级模块: 产业服务链分析
- 二级模块: 服务机构分析
- 三级模块: 新增趋势分析
- 更新频率: 年度
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-02

## 口径定义

特定产业领域内当年新增(成立或首次开展服务)的服务机构数量。

## 计算公式

COUNT(org) GROUP BY field_id, founded_year。

## 源库表字段

demo_gkxlumenx_ads.svc_metric_series(metric_id=M_SVC_NEW_CNT) — 43行, 按年度时间序列; gkxlumenx_ods.dwd_org_base_info(incorporation_date) — 20000行

## 待建表字段

首次开展服务口径依赖服务记录源(当前仅工商成立日期)

## 参考文献 / 依据

需求文档§1.1.1.2.4.2.7.2.1; svc_metric_series有43行年度数据, '首次开展服务'口径依赖服务记录源未定

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
