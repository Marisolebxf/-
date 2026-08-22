# 区域服务机构数（M_SVC_PT_REGION_ORG）

## 基本信息

- 指标ID: M_SVC_PT_REGION_ORG
- 指标名称: 区域服务机构数
- 一级模块: 产业服务链分析
- 二级模块: 专题服务
- 三级模块: 服务机构区域分布
- 更新频率: 年度
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-SVCCHAIN-06

## 口径定义

按区域(全球=国家/地区; 全国=省级)聚合的服务机构计数。区域归属口径未定。

## 计算公式

COUNT(org) GROUP BY region。

## 源库表字段

demo_gkxlumenx_ads.svc_region_dist(metric_id, geo_level, region_name, org_count) — 10行, 仅省份和深圳区级粒度

## 待建表字段

全球/国家级区域归属字段(当前只有省份和深圳区级)

## 参考文献 / 依据

需求文档§1.1.1.1.1.1.1.33.3; svc_region_dist有10行但仅province和sz_district两级, 无全球国家粒度

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
