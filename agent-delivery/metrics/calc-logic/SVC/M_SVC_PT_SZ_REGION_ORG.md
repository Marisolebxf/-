# 深圳机构区域分布（M_SVC_PT_SZ_REGION_ORG）

## 基本信息

- 指标ID: M_SVC_PT_SZ_REGION_ORG
- 指标名称: 深圳机构区域分布
- 一级模块: 产业服务链分析
- 二级模块: 专题服务
- 三级模块: 深圳产业服务
- 更新频率: 年度
- 对齐状态判定: 已对齐
- 是否在数据库: 是
- 关联Q编号: Q-SVCCHAIN-06

## 口径定义

深圳产业服务机构按行政区(十区字典全集)的分类计数。

## 计算公式

COUNT(org) WHERE city=深圳 GROUP BY district。

## 源库表字段

demo_gkxlumenx_ads.svc_region_dist(metric_id=M_SVC_SZ_DISTRICT, geo_level=sz_district) — 10行, 十区全覆盖; demo_gkxlumenx_ads.svc_org_card(area字段) — 3525行

## 待建表字段

无

## 参考文献 / 依据

需求文档§1.1.1.1.1.1.1.33.5; svc_region_dist有深圳十区全覆盖数据, svc_org_card.area有区级字段

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
