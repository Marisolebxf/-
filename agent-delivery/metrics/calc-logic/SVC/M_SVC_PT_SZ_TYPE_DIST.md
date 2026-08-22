# 深圳机构类型统计（M_SVC_PT_SZ_TYPE_DIST）

## 基本信息

- 指标ID: M_SVC_PT_SZ_TYPE_DIST
- 指标名称: 深圳机构类型统计
- 一级模块: 产业服务链分析
- 二级模块: 专题服务
- 三级模块: 深圳产业服务
- 更新频率: 年度
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-06

## 口径定义

深圳产业服务机构按类型的分类计数。

## 计算公式

COUNT(org) WHERE city=深圳 GROUP BY org_type。

## 源库表字段

demo_gkxlumenx_dwd.svc_org_circle(service_type_candidate字段) — 3525行, 含6类: INNOV/FINANCE/IP/HR/MARKET/CONSULT; demo_gkxlumenx_ads.svc_metric_dist — 97行

## 待建表字段

深圳机构与svc_org_circle的关联确认(需city过滤逻辑)

## 参考文献 / 依据

需求文档§1.1.1.1.1.1.1.33.5; 六类服务类型有数据但需确认深圳过滤逻辑

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
